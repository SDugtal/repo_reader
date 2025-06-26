from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
from pathlib import Path
from github_fetcher import GitHubFetcher
from summarizer import CodeSummarizer
from writer import ReportWriter
from datetime import datetime
from utils.token_tracker import token_tracker

# Load .env from same directory as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

print("🚀 Starting GitHub Repo Reader...")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'

# Initialize components
github_fetcher = GitHubFetcher()
code_summarizer = CodeSummarizer()
report_writer = ReportWriter()

def parse_github_url(github_url: str) -> tuple:
    """Parse GitHub URL to extract owner and repo"""
    try:
        url = github_url.strip()
        for prefix in ['https://github.com/', 'http://github.com/', 'github.com/']:
            if url.startswith(prefix):
                url = url.replace(prefix, '')
        url = url.rstrip('/')
        if url.endswith('.git'):
            url = url[:-4]
        parts = url.split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
        raise ValueError("Invalid GitHub URL format")
    except Exception as e:
        raise ValueError(f"Invalid GitHub URL: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')  # Optional if using a frontend

@app.route('/analyze', methods=['POST'])
def analyze_repo():
    try:
        data = request.get_json()
        github_url = data.get('github_url')
        if not github_url:
            return jsonify({'error': 'GitHub URL is required'}), 400

        try:
            owner, repo = parse_github_url(github_url)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Track token usage
        token_usage = {
            'github_api_calls': 0,
            'github_rate_limit_remaining': 0,
            'github_rate_limit_reset': None,
            'huggingface_api_calls': 0,
            'huggingface_tokens_used': 0,
            'total_cost_estimate': 0.0
        }

        # Repo info
        repo_data = github_fetcher.get_repo_info(owner, repo)
        token_usage['github_api_calls'] += 1
        if not repo_data:
            limit = github_fetcher.get_rate_limit_info()
            if limit and limit['remaining'] == 0:
                return jsonify({'error': 'GitHub rate limit exceeded'}), 429
            return jsonify({'error': f'Repo {owner}/{repo} not found or is private'}), 404

        # File structure
        files_data = github_fetcher.get_repo_files(owner, repo)
        token_usage['github_api_calls'] += 1

        # Analyze files
        analysis_results = []
        for file_info in files_data[:10]:
            if file_info['type'] == 'file' and code_summarizer.is_code_file(file_info['name']):
                content = github_fetcher.get_file_content(owner, repo, file_info['path'])
                token_usage['github_api_calls'] += 1
                if content:
                    summary, usage = code_summarizer.summarize_code(content, file_info['name'])
                    token_usage['huggingface_api_calls'] += usage.get('api_calls', 0)
                    token_usage['huggingface_tokens_used'] += usage.get('tokens_used', 0)
                    analysis_results.append({
                        'file': file_info['name'],
                        'path': file_info['path'],
                        'summary': summary,
                        'size': file_info.get('size', 0),
                        'tokens_used': usage.get('tokens_used', 0)
                    })

        # Commits and contributors
        commits = github_fetcher.get_recent_commits(owner, repo, limit=5)
        token_usage['github_api_calls'] += 1
        contributors = github_fetcher.get_contributors(owner, repo)
        token_usage['github_api_calls'] += 1

        # Rate limit
        rate = github_fetcher.get_rate_limit_info()
        if rate:
            token_usage['github_rate_limit_remaining'] = rate.get('remaining', 0)
            token_usage['github_rate_limit_reset'] = rate.get('reset_time')

        # Cost estimation
        token_usage['total_cost_estimate'] = calculate_cost_estimate(token_usage)

        # Track usage
        token_tracker.record_usage(token_usage)

        # Final result
        return jsonify({
            'repo_info': repo_data,
            'file_analysis': analysis_results,
            'commits': commits,
            'contributors': contributors,
            'total_files_analyzed': len(analysis_results),
            'token_usage': token_usage
        })

    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

def calculate_cost_estimate(usage):
    """Rough cost: HF = $0.0002 / 1K tokens"""
    return (usage['huggingface_tokens_used'] / 1000) * 0.0002

if __name__ == '__main__':
    print("🌐 Server starting on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

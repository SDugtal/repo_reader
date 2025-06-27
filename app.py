
from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
from github_fetcher import GitHubFetcher
from summarizer import CodeSummarizer
from writer import ReportWriter
import tempfile
import zipfile
from datetime import datetime
from utils.token_tracker import token_tracker
from utils.token_validator_quiet import QuietTokenValidator

# Load environment variables
load_dotenv()

# Quick silent token validation
print("🚀 Starting GitHub Repo Reader...")
token_validator = QuietTokenValidator()
token_validator.print_simple_status()

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
        
        if url.startswith('https://github.com/'):
            url = url.replace('https://github.com/', '')
        elif url.startswith('http://github.com/'):
            url = url.replace('http://github.com/', '')
        elif url.startswith('github.com/'):
            url = url.replace('github.com/', '')
        
        url = url.rstrip('/')
        if url.endswith('.git'):
            url = url[:-4]
        
        parts = url.split('/')
        
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1]
            
            if not owner or not repo:
                raise ValueError("Owner or repository name is empty")
            
            return owner, repo
        else:
            raise ValueError(f"Invalid URL format. Expected: owner/repo, got: {url}")
            
    except Exception as e:
        raise ValueError(f"Invalid GitHub URL format: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

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
        
        # Initialize token usage tracking
        token_usage = {
            'github_api_calls': 0,
            'github_rate_limit_remaining': 0,
            'github_rate_limit_reset': None,
            'huggingface_api_calls': 0,
            'huggingface_tokens_used': 0,
            'total_cost_estimate': 0.0
        }
        
        # Fetch repository data
        repo_data = github_fetcher.get_repo_info(owner, repo)
        token_usage['github_api_calls'] += 1
        
        if not repo_data:
            rate_limit_info = github_fetcher.get_rate_limit_info()
            if rate_limit_info and rate_limit_info['remaining'] == 0:
                return jsonify({
                    'error': 'GitHub API rate limit exceeded. Please try again later or add a GitHub token for higher limits.'
                }), 429
            else:
                return jsonify({
                    'error': f'Repository "{owner}/{repo}" not found or is private. Please check the URL and ensure the repository is public.'
                }), 404
        
        # Get file structure and content
        files_data = github_fetcher.get_repo_files(owner, repo)
        token_usage['github_api_calls'] += 1
        
        # Analyze code files
        analysis_results = []
        analyzed_count = 0
        
        for file_info in files_data[:10]:
            if file_info['type'] == 'file' and code_summarizer.is_code_file(file_info['name']):
                content = github_fetcher.get_file_content(owner, repo, file_info['path'])
                token_usage['github_api_calls'] += 1
                
                if content:
                    summary, ai_usage = code_summarizer.summarize_code(content, file_info['name'])
                    token_usage['huggingface_api_calls'] += ai_usage.get('api_calls', 0)
                    token_usage['huggingface_tokens_used'] += ai_usage.get('tokens_used', 0)
                    
                    analysis_results.append({
                        'file': file_info['name'],
                        'path': file_info['path'],
                        'summary': summary,
                        'size': file_info.get('size', 0),
                        'tokens_used': ai_usage.get('tokens_used', 0)
                    })
                    analyzed_count += 1
        
        # Get commit history
        commits = github_fetcher.get_recent_commits(owner, repo, limit=5)
        token_usage['github_api_calls'] += 1
        
        # Get contributors
        contributors = github_fetcher.get_contributors(owner, repo)
        token_usage['github_api_calls'] += 1
        
        # Get GitHub rate limit info
        rate_limit_info = github_fetcher.get_rate_limit_info()
        if rate_limit_info:
            token_usage['github_rate_limit_remaining'] = rate_limit_info.get('remaining', 0)
            token_usage['github_rate_limit_reset'] = rate_limit_info.get('reset_time', None)
        
        # Calculate estimated costs
        token_usage['total_cost_estimate'] = calculate_cost_estimate(token_usage)
        
        # Record usage in tracker
        token_tracker.record_usage(token_usage)
        
        # Get usage summary for display
        usage_summary = token_tracker.get_usage_summary()
        
        # Get rate limit status
        rate_limit_status = token_tracker.get_rate_limit_status(
            token_usage['github_rate_limit_remaining'],
            5000 if github_fetcher.headers.get('Authorization') else 60
        )
        
        result = {
            'repo_info': repo_data,
            'file_analysis': analysis_results,
            'commits': commits,
            'contributors': contributors,
            'total_files_analyzed': len(analysis_results),
            'token_usage': token_usage,
            'usage_summary': usage_summary,
            'rate_limit_status': rate_limit_status
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

def calculate_cost_estimate(usage):
    """Calculate estimated API costs"""
    github_cost = 0.0
    hf_cost = (usage['huggingface_tokens_used'] / 1000) * 0.0002
    return github_cost + hf_cost

@app.route('/export/<format>')
def export_report(format):
    try:
        sample_data = {
            'repo_name': 'sample-repo',
            'description': 'A sample repository for demonstration',
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'files': [
                {'name': 'main.py', 'summary': 'Main application entry point'},
                {'name': 'utils.py', 'summary': 'Utility functions for data processing'}
            ]
        }
        
        if format == 'docx':
            file_path = report_writer.create_docx_report(sample_data)
            return send_file(file_path, as_attachment=True, download_name='repo_analysis.docx')
        elif format == 'md':
            file_path = report_writer.create_markdown_report(sample_data)
            return send_file(file_path, as_attachment=True, download_name='repo_analysis.md')
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/usage-stats')
def usage_stats():
    try:
        usage_summary = token_tracker.get_usage_summary()
        return jsonify(usage_summary)
    except Exception as e:
        return jsonify({'error': f'Failed to get usage stats: {str(e)}'}), 500

if __name__ == '__main__':
    print("🌐 Server starting on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, send_from_directory
from document_generator import RepoDocumentGenerator
import os

app = Flask(__name__)
app.config['OUTPUT_DIR'] = 'output'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get filters from form
        filters = {
            'language': request.form.get('language'),
            'min_stars': int(request.form.get('min_stars')) if request.form.get('min_stars') else None
        }
        sort_by = request.form.get('sort_by', 'updated')
        
        # Generate report
        generator = RepoDocumentGenerator()
        report = generator.generate_all(output_dir=app.config['OUTPUT_DIR'], 
                                     filters=filters, 
                                     sort_by=sort_by)
        
        return render_template('report.html', 
                            report=report,
                            filters=filters,
                            sort_by=sort_by)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['OUTPUT_DIR'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    app.run(debug=True)


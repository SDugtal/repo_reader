import requests
import base64
from typing import Dict, List, Optional
import os
from datetime import datetime

class GitHubFetcher:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repo-Reader'
        }
        
        # Add GitHub token if available (silently)
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token and github_token != 'your_github_token_here':
            self.headers['Authorization'] = f'token {github_token}'
    
    def get_repo_info(self, owner: str, repo: str) -> Optional[Dict]:
        """Get basic repository information"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data['name'],
                    'full_name': data['full_name'],
                    'description': data.get('description', 'No description available'),
                    'language': data.get('language', 'Unknown'),
                    'stars': data['stargazers_count'],
                    'forks': data['forks_count'],
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at'],
                    'size': data['size'],
                    'default_branch': data['default_branch'],
                    'topics': data.get('topics', []),
                    'license': data.get('license', {}).get('name', 'No license') if data.get('license') else 'No license'
                }
            return None
                
        except Exception as e:
            return None
    
    def get_repo_files(self, owner: str, repo: str, path: str = "") -> List[Dict]:
        """Get repository file structure"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return []
                
        except Exception as e:
            return []
    
    def get_file_content(self, owner: str, repo: str, file_path: str) -> Optional[str]:
        """Get content of a specific file"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('encoding') == 'base64':
                    try:
                        content = base64.b64decode(data['content']).decode('utf-8')
                        return content
                    except UnicodeDecodeError:
                        return None
            return None
        except Exception as e:
            return None
    
    def get_recent_commits(self, owner: str, repo: str, limit: int = 10) -> List[Dict]:
        """Get recent commits"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            params = {'per_page': limit}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                commits = response.json()
                return [
                    {
                        'sha': commit['sha'][:7],
                        'message': commit['commit']['message'].split('\n')[0],
                        'author': commit['commit']['author']['name'],
                        'date': commit['commit']['author']['date'],
                        'url': commit['html_url']
                    }
                    for commit in commits
                ]
            return []
        except Exception as e:
            return []
    
    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        """Get repository contributors"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                contributors = response.json()
                return [
                    {
                        'login': contributor['login'],
                        'contributions': contributor['contributions'],
                        'avatar_url': contributor['avatar_url'],
                        'profile_url': contributor['html_url']
                    }
                    for contributor in contributors[:10]
                ]
            return []
        except Exception as e:
            return []

    def get_rate_limit_info(self) -> Optional[Dict]:
        """Get current GitHub API rate limit information"""
        try:
            url = f"{self.base_url}/rate_limit"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                core_limit = data['resources']['core']
                
                return {
                    'limit': core_limit['limit'],
                    'remaining': core_limit['remaining'],
                    'reset': core_limit['reset'],
                    'reset_time': datetime.fromtimestamp(core_limit['reset']).isoformat()
                }
            return None
        except Exception as e:
            return None

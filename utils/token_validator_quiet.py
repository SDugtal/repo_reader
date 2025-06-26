#!/usr/bin/env python3
"""
Quiet token validation - minimal output
"""
import requests
import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv

class QuietTokenValidator:
    """Silent token validation with minimal output"""
    
    def __init__(self):
        load_dotenv()
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.hf_token = os.environ.get('HUGGING_FACE_TOKEN')
    
    def validate_all_tokens_quiet(self) -> Dict:
        """Validate tokens silently"""
        results = {
            'github': self._validate_github_quiet(),
            'huggingface': self._validate_hf_quiet(),
            'overall_status': 'unknown'
        }
        
        # Determine overall status
        github_ok = results['github']['valid']
        hf_ok = results['huggingface']['valid']
        
        if github_ok and hf_ok:
            results['overall_status'] = 'excellent'
        elif github_ok:
            results['overall_status'] = 'good'
        else:
            results['overall_status'] = 'basic'
        
        return results
    
    def _validate_github_quiet(self) -> Dict:
        """Validate GitHub token silently"""
        if not self.github_token or self.github_token == 'your_github_token_here':
            return {'valid': False, 'rate_limit': {}}
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'valid': True,
                    'rate_limit': {
                        'remaining': data['resources']['core']['remaining'],
                        'limit': data['resources']['core']['limit']
                    }
                }
        except:
            pass
        
        return {'valid': False, 'rate_limit': {}}
    
    def _validate_hf_quiet(self) -> Dict:
        """Validate Hugging Face token silently"""
        if not self.hf_token or self.hf_token == 'your_hugging_face_token_here':
            return {'valid': False}
        
        headers = {'Authorization': f'Bearer {self.hf_token}'}
        
        try:
            response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=5)
            return {'valid': response.status_code == 200}
        except:
            return {'valid': False}
    
    def print_simple_status(self) -> None:
        """Print a simple one-line status"""
        results = self.validate_all_tokens_quiet()
        
        github_status = "✅" if results['github']['valid'] else "❌"
        hf_status = "✅" if results['huggingface']['valid'] else "❌"
        
        if results['github']['valid']:
            remaining = results['github']['rate_limit'].get('remaining', 'Unknown')
            print(f"🔑 Tokens: GitHub {github_status} ({remaining} requests) | AI {hf_status}")
        else:
            print(f"🔑 Tokens: GitHub {github_status} | AI {hf_status}")

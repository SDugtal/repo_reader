#!/usr/bin/env python3
"""
Automatic token validation and testing system
"""
import requests
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
import json

class TokenValidator:
    """Comprehensive token validation and testing system"""
    
    def __init__(self):
        load_dotenv()
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.hf_token = os.environ.get('HUGGING_FACE_TOKEN')
        self.validation_cache = {}
        self.cache_duration = 300  # 5 minutes
        
    def validate_all_tokens(self) -> Dict:
        """Validate all configured tokens"""
        print("🔍 Automatic Token Validation Starting...")
        print("=" * 45)
        
        results = {
            'github': self.validate_github_token(),
            'huggingface': self.validate_huggingface_token(),
            'overall_status': 'unknown',
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Determine overall status
        github_ok = results['github']['valid']
        hf_ok = results['huggingface']['valid']
        
        if github_ok and hf_ok:
            results['overall_status'] = 'excellent'
            results['recommendations'].append("🎉 All tokens are working perfectly!")
        elif github_ok:
            results['overall_status'] = 'good'
            results['recommendations'].append("✅ GitHub token working. Add Hugging Face token for AI features.")
        elif hf_ok:
            results['overall_status'] = 'limited'
            results['recommendations'].append("⚠️ Add GitHub token to avoid rate limits (60 → 5000 requests/hour)")
        else:
            results['overall_status'] = 'basic'
            results['recommendations'].append("🔧 Add tokens for full functionality")
        
        self._print_validation_summary(results)
        return results
    
    def validate_github_token(self) -> Dict:
        """Validate GitHub token with comprehensive testing"""
        result = {
            'valid': False,
            'configured': False,
            'rate_limit': {},
            'permissions': [],
            'user_info': {},
            'errors': [],
            'recommendations': []
        }
        
        print("\n🔍 GitHub Token Validation")
        print("-" * 30)
        
        if not self.github_token or self.github_token == 'your_github_token_here':
            print("❌ No GitHub token configured")
            result['errors'].append("No token configured")
            result['recommendations'].append("Add GITHUB_TOKEN to .env file")
            return result
        
        result['configured'] = True
        print(f"🔑 Token found: {self.github_token[:10]}...")
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repo-Reader-Validator'
        }
        
        try:
            # Test 1: Rate limit check
            print("📊 Testing rate limits...")
            response = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=10)
            
            if response.status_code == 200:
                rate_data = response.json()
                result['rate_limit'] = {
                    'limit': rate_data['resources']['core']['limit'],
                    'remaining': rate_data['resources']['core']['remaining'],
                    'reset': rate_data['resources']['core']['reset'],
                    'reset_time': datetime.fromtimestamp(rate_data['resources']['core']['reset']).isoformat()
                }
                print(f"✅ Rate limit: {result['rate_limit']['remaining']}/{result['rate_limit']['limit']}")
            else:
                result['errors'].append(f"Rate limit check failed: {response.status_code}")
                print(f"❌ Rate limit check failed: {response.status_code}")
            
            # Test 2: User info and permissions
            print("👤 Testing user permissions...")
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                result['user_info'] = {
                    'login': user_data.get('login', 'Unknown'),
                    'name': user_data.get('name', 'Unknown'),
                    'email': user_data.get('email', 'Not provided'),
                    'type': user_data.get('type', 'Unknown')
                }
                print(f"✅ Authenticated as: {result['user_info']['login']}")
            else:
                result['errors'].append(f"User info failed: {response.status_code}")
                print(f"❌ User info failed: {response.status_code}")
            
            # Test 3: Repository access
            print("📁 Testing repository access...")
            test_repo_url = 'https://api.github.com/repos/octocat/Hello-World'
            response = requests.get(test_repo_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Repository access working")
                result['permissions'].append('public_repo')
            else:
                result['errors'].append(f"Repository access failed: {response.status_code}")
                print(f"❌ Repository access failed: {response.status_code}")
            
            # Test 4: Token scopes
            if 'X-OAuth-Scopes' in response.headers:
                scopes = response.headers['X-OAuth-Scopes'].split(', ')
                result['permissions'].extend(scopes)
                print(f"🔐 Token scopes: {', '.join(scopes)}")
            
            # Determine if token is valid
            if not result['errors']:
                result['valid'] = True
                print("🎉 GitHub token is fully functional!")
            else:
                print(f"⚠️ GitHub token has {len(result['errors'])} issues")
            
        except requests.exceptions.Timeout:
            result['errors'].append("Request timeout")
            print("❌ GitHub API timeout")
        except requests.exceptions.ConnectionError:
            result['errors'].append("Connection error")
            print("❌ Cannot connect to GitHub API")
        except Exception as e:
            result['errors'].append(f"Unexpected error: {str(e)}")
            print(f"❌ Unexpected error: {e}")
        
        return result
    
    def validate_huggingface_token(self) -> Dict:
        """Validate Hugging Face token with comprehensive testing"""
        result = {
            'valid': False,
            'configured': False,
            'user_info': {},
            'inference_access': False,
            'model_access': [],
            'errors': [],
            'recommendations': []
        }
        
        print("\n🤗 Hugging Face Token Validation")
        print("-" * 35)
        
        if not self.hf_token or self.hf_token == 'your_hugging_face_token_here':
            print("❌ No Hugging Face token configured")
            result['errors'].append("No token configured")
            result['recommendations'].append("Add HUGGING_FACE_TOKEN to .env file")
            return result
        
        result['configured'] = True
        print(f"🔑 Token found: {self.hf_token[:10]}...")
        
        headers = {'Authorization': f'Bearer {self.hf_token}'}
        
        try:
            # Test 1: User info
            print("👤 Testing user authentication...")
            response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                result['user_info'] = {
                    'name': user_data.get('name', 'Unknown'),
                    'email': user_data.get('email', 'Not provided'),
                    'type': user_data.get('type', 'user')
                }
                print(f"✅ Authenticated as: {result['user_info']['name']}")
            else:
                result['errors'].append(f"Authentication failed: {response.status_code}")
                print(f"❌ Authentication failed: {response.status_code}")
                return result
            
            # Test 2: Inference API access
            print("🧠 Testing Inference API access...")
            models_to_test = [
                'microsoft/codebert-base',
                'facebook/bart-large-cnn',
                'distilbert-base-uncased'
            ]
            
            for model in models_to_test:
                api_url = f"https://api-inference.huggingface.co/models/{model}"
                test_payload = {
                    "inputs": "def hello(): print('test')",
                    "parameters": {"max_length": 50}
                }
                
                response = requests.post(api_url, headers=headers, json=test_payload, timeout=15)
                
                if response.status_code == 200:
                    result['model_access'].append(model)
                    print(f"✅ Model access: {model}")
                    result['inference_access'] = True
                elif response.status_code == 503:
                    result['model_access'].append(f"{model} (loading)")
                    print(f"⏳ Model loading: {model}")
                    result['inference_access'] = True
                else:
                    print(f"⚠️ Model {model}: {response.status_code}")
                
                # Don't overwhelm the API
                time.sleep(1)
            
            # Determine if token is valid
            if result['inference_access']:
                result['valid'] = True
                print("🎉 Hugging Face token is working!")
            else:
                result['errors'].append("No inference API access")
                print("❌ No inference API access")
            
        except requests.exceptions.Timeout:
            result['errors'].append("Request timeout")
            print("❌ Hugging Face API timeout")
        except requests.exceptions.ConnectionError:
            result['errors'].append("Connection error")
            print("❌ Cannot connect to Hugging Face API")
        except Exception as e:
            result['errors'].append(f"Unexpected error: {str(e)}")
            print(f"❌ Unexpected error: {e}")
        
        return result
    
    def test_token_rotation(self) -> Dict:
        """Test token rotation and expiration handling"""
        print("\n🔄 Token Rotation Test")
        print("-" * 25)
        
        results = {
            'github_expiry': None,
            'hf_expiry': None,
            'rotation_needed': False,
            'recommendations': []
        }
        
        # GitHub tokens don't have built-in expiry info in API
        # But we can check if they're classic or fine-grained
        if self.github_token:
            if self.github_token.startswith('ghp_'):
                print("🔑 GitHub: Classic personal access token")
                results['recommendations'].append("Consider setting expiration date for GitHub token")
            elif self.github_token.startswith('github_pat_'):
                print("🔑 GitHub: Fine-grained personal access token")
            else:
                print("⚠️ GitHub: Unknown token format")
        
        # Hugging Face tokens also don't expose expiry via API
        if self.hf_token:
            if self.hf_token.startswith('hf_'):
                print("🔑 Hugging Face: Standard token format")
            else:
                print("⚠️ Hugging Face: Unknown token format")
        
        return results
    
    def continuous_monitoring(self, interval_minutes: int = 30) -> None:
        """Continuous token monitoring (for production use)"""
        print(f"🔄 Starting continuous monitoring (every {interval_minutes} minutes)")
        
        while True:
            try:
                results = self.validate_all_tokens()
                
                # Log results
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_entry = {
                    'timestamp': timestamp,
                    'status': results['overall_status'],
                    'github_valid': results['github']['valid'],
                    'hf_valid': results['huggingface']['valid']
                }
                
                # Save to log file
                with open('token_monitoring.log', 'a') as f:
                    f.write(f"{json.dumps(log_entry)}\n")
                
                # Alert on issues
                if results['overall_status'] in ['limited', 'basic']:
                    print(f"⚠️ [{timestamp}] Token issues detected!")
                    for rec in results['recommendations']:
                        print(f"   {rec}")
                
                # Wait for next check
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def _print_validation_summary(self, results: Dict) -> None:
        """Print a comprehensive validation summary"""
        print("\n" + "=" * 50)
        print("📊 TOKEN VALIDATION SUMMARY")
        print("=" * 50)
        
        status_emoji = {
            'excellent': '🎉',
            'good': '✅',
            'limited': '⚠️',
            'basic': '🔧'
        }
        
        status = results['overall_status']
        print(f"\n{status_emoji.get(status, '❓')} Overall Status: {status.upper()}")
        
        # GitHub summary
        github = results['github']
        if github['valid']:
            rate_limit = github.get('rate_limit', {})
            remaining = rate_limit.get('remaining', 'Unknown')
            limit = rate_limit.get('limit', 'Unknown')
            print(f"✅ GitHub: {remaining}/{limit} requests remaining")
        else:
            print("❌ GitHub: Not working properly")
        
        # Hugging Face summary
        hf = results['huggingface']
        if hf['valid']:
            models = len(hf.get('model_access', []))
            print(f"✅ Hugging Face: {models} models accessible")
        else:
            print("❌ Hugging Face: Not working properly")
        
        # Recommendations
        if results['recommendations']:
            print("\n💡 Recommendations:")
            for rec in results['recommendations']:
                print(f"   {rec}")
        
        print(f"\n🕒 Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main validation function"""
    validator = TokenValidator()
    results = validator.validate_all_tokens()
    
    # Test token rotation
    rotation_results = validator.test_token_rotation()
    
    # Save results
    with open('token_validation_results.json', 'w') as f:
        json.dump({
            'validation': results,
            'rotation': rotation_results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: token_validation_results.json")
    
    # Offer continuous monitoring
    if results['overall_status'] in ['excellent', 'good']:
        monitor = input("\n🔄 Start continuous monitoring? (y/n): ").lower().strip()
        if monitor == 'y':
            try:
                validator.continuous_monitoring(interval_minutes=30)
            except KeyboardInterrupt:
                print("\n👋 Monitoring stopped")

if __name__ == "__main__":
    main()

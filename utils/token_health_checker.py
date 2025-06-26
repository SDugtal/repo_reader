#!/usr/bin/env python3
"""
Real-time token health monitoring and alerts
"""
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os
from dotenv import load_dotenv

class TokenHealthChecker:
    """Real-time token health monitoring system"""
    
    def __init__(self):
        load_dotenv()
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.hf_token = os.environ.get('HUGGING_FACE_TOKEN')
        self.health_history = []
        self.alert_thresholds = {
            'github_rate_limit_warning': 100,  # Warn when < 100 requests left
            'github_rate_limit_critical': 10,  # Critical when < 10 requests left
            'consecutive_failures': 3,         # Alert after 3 consecutive failures
            'response_time_warning': 5.0       # Warn if response > 5 seconds
        }
    
    def check_github_health(self) -> Dict:
        """Check GitHub API health and performance"""
        start_time = time.time()
        
        health = {
            'service': 'github',
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'response_time': 0,
            'rate_limit': {},
            'errors': [],
            'warnings': []
        }
        
        if not self.github_token or self.github_token == 'your_github_token_here':
            health['status'] = 'not_configured'
            health['errors'].append('No GitHub token configured')
            return health
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=10)
            health['response_time'] = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                core = data['resources']['core']
                
                health['rate_limit'] = {
                    'limit': core['limit'],
                    'remaining': core['remaining'],
                    'reset': core['reset'],
                    'reset_time': datetime.fromtimestamp(core['reset']).isoformat(),
                    'percentage_used': ((core['limit'] - core['remaining']) / core['limit']) * 100
                }
                
                # Determine status based on rate limit
                remaining = core['remaining']
                if remaining == 0:
                    health['status'] = 'rate_limited'
                    health['errors'].append('Rate limit exceeded')
                elif remaining < self.alert_thresholds['github_rate_limit_critical']:
                    health['status'] = 'critical'
                    health['warnings'].append(f'Only {remaining} requests remaining')
                elif remaining < self.alert_thresholds['github_rate_limit_warning']:
                    health['status'] = 'warning'
                    health['warnings'].append(f'Low rate limit: {remaining} requests remaining')
                else:
                    health['status'] = 'healthy'
                
                # Check response time
                if health['response_time'] > self.alert_thresholds['response_time_warning']:
                    health['warnings'].append(f'Slow response time: {health["response_time"]:.2f}s')
                
            else:
                health['status'] = 'error'
                health['errors'].append(f'HTTP {response.status_code}: {response.text[:100]}')
                
        except requests.exceptions.Timeout:
            health['status'] = 'timeout'
            health['errors'].append('Request timeout')
            health['response_time'] = time.time() - start_time
        except requests.exceptions.ConnectionError:
            health['status'] = 'connection_error'
            health['errors'].append('Cannot connect to GitHub API')
        except Exception as e:
            health['status'] = 'error'
            health['errors'].append(f'Unexpected error: {str(e)}')
        
        return health
    
    def check_huggingface_health(self) -> Dict:
        """Check Hugging Face API health and performance"""
        start_time = time.time()
        
        health = {
            'service': 'huggingface',
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'response_time': 0,
            'model_status': {},
            'errors': [],
            'warnings': []
        }
        
        if not self.hf_token or self.hf_token == 'your_hugging_face_token_here':
            health['status'] = 'not_configured'
            health['errors'].append('No Hugging Face token configured')
            return health
        
        headers = {'Authorization': f'Bearer {self.hf_token}'}
        
        try:
            # Test authentication
            response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
            auth_time = time.time() - start_time
            
            if response.status_code == 200:
                # Test inference API with a quick model
                inference_start = time.time()
                api_url = "https://api-inference.huggingface.co/models/microsoft/codebert-base"
                test_payload = {"inputs": "test", "parameters": {"max_length": 10}}
                
                inference_response = requests.post(api_url, headers=headers, json=test_payload, timeout=15)
                inference_time = time.time() - inference_start
                
                health['response_time'] = auth_time + inference_time
                
                if inference_response.status_code == 200:
                    health['status'] = 'healthy'
                    health['model_status']['codebert'] = 'available'
                elif inference_response.status_code == 503:
                    health['status'] = 'model_loading'
                    health['model_status']['codebert'] = 'loading'
                    health['warnings'].append('Model is loading, may take longer')
                else:
                    health['status'] = 'inference_error'
                    health['errors'].append(f'Inference API error: {inference_response.status_code}')
                
                # Check response time
                if health['response_time'] > self.alert_thresholds['response_time_warning']:
                    health['warnings'].append(f'Slow response time: {health["response_time"]:.2f}s')
                
            else:
                health['status'] = 'auth_error'
                health['errors'].append(f'Authentication failed: {response.status_code}')
                health['response_time'] = auth_time
                
        except requests.exceptions.Timeout:
            health['status'] = 'timeout'
            health['errors'].append('Request timeout')
            health['response_time'] = time.time() - start_time
        except requests.exceptions.ConnectionError:
            health['status'] = 'connection_error'
            health['errors'].append('Cannot connect to Hugging Face API')
        except Exception as e:
            health['status'] = 'error'
            health['errors'].append(f'Unexpected error: {str(e)}')
        
        return health
    
    def comprehensive_health_check(self) -> Dict:
        """Perform comprehensive health check of all services"""
        print("🏥 Comprehensive Token Health Check")
        print("=" * 40)
        
        github_health = self.check_github_health()
        hf_health = self.check_huggingface_health()
        
        overall_health = {
            'timestamp': datetime.now().isoformat(),
            'github': github_health,
            'huggingface': hf_health,
            'overall_status': 'unknown',
            'summary': {},
            'alerts': []
        }
        
        # Determine overall status
        github_status = github_health['status']
        hf_status = hf_health['status']
        
        if github_status == 'healthy' and hf_status == 'healthy':
            overall_health['overall_status'] = 'excellent'
        elif github_status in ['healthy', 'warning'] and hf_status in ['healthy', 'model_loading', 'not_configured']:
            overall_health['overall_status'] = 'good'
        elif github_status in ['healthy', 'warning']:
            overall_health['overall_status'] = 'limited'
        else:
            overall_health['overall_status'] = 'poor'
        
        # Generate summary
        overall_health['summary'] = {
            'github_requests_remaining': github_health.get('rate_limit', {}).get('remaining', 'N/A'),
            'github_response_time': f"{github_health['response_time']:.2f}s",
            'hf_response_time': f"{hf_health['response_time']:.2f}s",
            'total_errors': len(github_health['errors']) + len(hf_health['errors']),
            'total_warnings': len(github_health['warnings']) + len(hf_health['warnings'])
        }
        
        # Generate alerts
        all_errors = github_health['errors'] + hf_health['errors']
        all_warnings = github_health['warnings'] + hf_health['warnings']
        
        for error in all_errors:
            overall_health['alerts'].append({'type': 'error', 'message': error})
        
        for warning in all_warnings:
            overall_health['alerts'].append({'type': 'warning', 'message': warning})
        
        # Store in history
        self.health_history.append(overall_health)
        
        # Keep only last 100 checks
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]
        
        self._print_health_summary(overall_health)
        return overall_health
    
    def _print_health_summary(self, health: Dict) -> None:
        """Print health check summary"""
        status_emoji = {
            'excellent': '🎉',
            'good': '✅',
            'limited': '⚠️',
            'poor': '❌'
        }
        
        status = health['overall_status']
        print(f"\n{status_emoji.get(status, '❓')} Overall Health: {status.upper()}")
        
        # GitHub status
        github = health['github']
        github_emoji = '✅' if github['status'] == 'healthy' else '❌'
        print(f"{github_emoji} GitHub API: {github['status']}")
        if github.get('rate_limit'):
            remaining = github['rate_limit']['remaining']
            print(f"   📊 Rate limit: {remaining} requests remaining")
        print(f"   ⏱️  Response time: {github['response_time']:.2f}s")
        
        # Hugging Face status
        hf = health['huggingface']
        hf_emoji = '✅' if hf['status'] in ['healthy', 'model_loading'] else '❌'
        print(f"{hf_emoji} Hugging Face API: {hf['status']}")
        print(f"   ⏱️  Response time: {hf['response_time']:.2f}s")
        
        # Alerts
        if health['alerts']:
            print(f"\n🚨 Alerts ({len(health['alerts'])}):")
            for alert in health['alerts']:
                emoji = '❌' if alert['type'] == 'error' else '⚠️'
                print(f"   {emoji} {alert['message']}")
        
        print(f"\n🕒 Check completed: {datetime.now().strftime('%H:%M:%S')}")
    
    def start_monitoring(self, interval_seconds: int = 300) -> None:
        """Start continuous health monitoring"""
        print(f"🔄 Starting health monitoring (every {interval_seconds//60} minutes)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                health = self.comprehensive_health_check()
                
                # Save to log file
                log_entry = {
                    'timestamp': health['timestamp'],
                    'overall_status': health['overall_status'],
                    'github_status': health['github']['status'],
                    'hf_status': health['huggingface']['status'],
                    'alerts_count': len(health['alerts'])
                }
                
                with open('token_health.log', 'a') as f:
                    f.write(f"{json.dumps(log_entry)}\n")
                
                # Wait for next check
                print(f"\n⏳ Next check in {interval_seconds//60} minutes...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n🛑 Health monitoring stopped")
    
    def get_health_report(self) -> Dict:
        """Generate detailed health report"""
        if not self.health_history:
            return {'error': 'No health data available'}
        
        recent_checks = self.health_history[-10:]  # Last 10 checks
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_checks': len(self.health_history),
            'recent_status': recent_checks[-1]['overall_status'],
            'github_stats': {
                'avg_response_time': 0,
                'error_rate': 0,
                'uptime_percentage': 0
            },
            'hf_stats': {
                'avg_response_time': 0,
                'error_rate': 0,
                'uptime_percentage': 0
            },
            'trends': []
        }
        
        # Calculate GitHub stats
        github_times = [check['github']['response_time'] for check in recent_checks if check['github']['response_time'] > 0]
        github_errors = [check for check in recent_checks if check['github']['status'] in ['error', 'timeout', 'connection_error']]
        
        if github_times:
            report['github_stats']['avg_response_time'] = sum(github_times) / len(github_times)
        report['github_stats']['error_rate'] = (len(github_errors) / len(recent_checks)) * 100
        report['github_stats']['uptime_percentage'] = ((len(recent_checks) - len(github_errors)) / len(recent_checks)) * 100
        
        # Calculate Hugging Face stats
        hf_times = [check['huggingface']['response_time'] for check in recent_checks if check['huggingface']['response_time'] > 0]
        hf_errors = [check for check in recent_checks if check['huggingface']['status'] in ['error', 'timeout', 'connection_error']]
        
        if hf_times:
            report['hf_stats']['avg_response_time'] = sum(hf_times) / len(hf_times)
        report['hf_stats']['error_rate'] = (len(hf_errors) / len(recent_checks)) * 100
        report['hf_stats']['uptime_percentage'] = ((len(recent_checks) - len(hf_errors)) / len(recent_checks)) * 100
        
        return report

def main():
    """Main health checker function"""
    checker = TokenHealthChecker()
    
    print("🏥 Token Health Checker")
    print("=" * 25)
    
    # Perform initial health check
    health = checker.comprehensive_health_check()
    
    # Save results
    with open('token_health_results.json', 'w') as f:
        json.dump(health, f, indent=2)
    
    print(f"\n💾 Results saved to: token_health_results.json")
    
    # Offer continuous monitoring
    if health['overall_status'] in ['excellent', 'good']:
        monitor = input("\n🔄 Start continuous health monitoring? (y/n): ").lower().strip()
        if monitor == 'y':
            interval = input("Check interval in minutes (default 5): ").strip()
            try:
                interval_minutes = int(interval) if interval else 5
                checker.start_monitoring(interval_seconds=interval_minutes * 60)
            except ValueError:
                print("Invalid interval, using 5 minutes")
                checker.start_monitoring(interval_seconds=300)
            except KeyboardInterrupt:
                print("\n👋 Monitoring stopped")

if __name__ == "__main__":
    main()

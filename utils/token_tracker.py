from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

class TokenTracker:
    """Track API token usage across sessions"""
    
    def __init__(self, storage_file='token_usage.json'):
        self.storage_file = storage_file
        self.usage_data = self._load_usage_data()
    
    def _load_usage_data(self) -> Dict:
        """Load usage data from storage"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'daily_usage': {},
            'monthly_usage': {},
            'total_usage': {
                'github_api_calls': 0,
                'huggingface_api_calls': 0,
                'huggingface_tokens_used': 0,
                'total_cost': 0.0
            }
        }
    
    def _save_usage_data(self):
        """Save usage data to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            print(f"Error saving usage data: {e}")
    
    def record_usage(self, usage_info: Dict):
        """Record API usage"""
        today = datetime.now().strftime('%Y-%m-%d')
        month = datetime.now().strftime('%Y-%m')
        
        # Initialize daily usage if not exists
        if today not in self.usage_data['daily_usage']:
            self.usage_data['daily_usage'][today] = {
                'github_api_calls': 0,
                'huggingface_api_calls': 0,
                'huggingface_tokens_used': 0,
                'total_cost': 0.0
            }
        
        # Initialize monthly usage if not exists
        if month not in self.usage_data['monthly_usage']:
            self.usage_data['monthly_usage'][month] = {
                'github_api_calls': 0,
                'huggingface_api_calls': 0,
                'huggingface_tokens_used': 0,
                'total_cost': 0.0
            }
        
        # Update usage counters
        for key in ['github_api_calls', 'huggingface_api_calls', 'huggingface_tokens_used', 'total_cost_estimate']:
            if key in usage_info:
                value = usage_info[key]
                storage_key = key.replace('_estimate', '')
                
                self.usage_data['daily_usage'][today][storage_key] += value
                self.usage_data['monthly_usage'][month][storage_key] += value
                self.usage_data['total_usage'][storage_key] += value
        
        # Clean old daily data (keep last 30 days)
        self._cleanup_old_data()
        
        # Save updated data
        self._save_usage_data()
    
    def _cleanup_old_data(self):
        """Remove usage data older than 30 days"""
        cutoff_date = datetime.now() - timedelta(days=30)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')
        
        # Remove old daily data
        old_dates = [date for date in self.usage_data['daily_usage'].keys() if date < cutoff_str]
        for date in old_dates:
            del self.usage_data['daily_usage'][date]
    
    def get_usage_summary(self) -> Dict:
        """Get usage summary for display"""
        today = datetime.now().strftime('%Y-%m-%d')
        month = datetime.now().strftime('%Y-%m')
        
        return {
            'today': self.usage_data['daily_usage'].get(today, {}),
            'this_month': self.usage_data['monthly_usage'].get(month, {}),
            'total': self.usage_data['total_usage'],
            'daily_history': dict(list(self.usage_data['daily_usage'].items())[-7:])  # Last 7 days
        }
    
    def get_rate_limit_status(self, github_remaining: int, github_limit: int) -> Dict:
        """Get rate limit status and recommendations"""
        usage_percentage = ((github_limit - github_remaining) / github_limit) * 100
        
        status = {
            'percentage_used': usage_percentage,
            'remaining': github_remaining,
            'limit': github_limit,
            'status': 'good'
        }
        
        if usage_percentage > 80:
            status['status'] = 'warning'
            status['message'] = 'Approaching rate limit. Consider adding a GitHub token.'
        elif usage_percentage > 95:
            status['status'] = 'critical'
            status['message'] = 'Rate limit almost exceeded. Add a GitHub token immediately.'
        
        return status

# Global token tracker instance
token_tracker = TokenTracker()

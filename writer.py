import tempfile
import os
from datetime import datetime
from typing import Dict, List

class ReportWriter:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def create_markdown_report(self, data: Dict) -> str:
        """Create a markdown report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"repo_analysis_{timestamp}.md"
        filepath = os.path.join(self.temp_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Repository Analysis Report\n\n")
            f.write(f"**Repository:** {data.get('repo_name', 'Unknown')}\n")
            f.write(f"**Analysis Date:** {data.get('analysis_date', 'Unknown')}\n")
            f.write(f"**Description:** {data.get('description', 'No description available')}\n\n")
            
            f.write("## Repository Overview\n\n")
            repo_info = data.get('repo_info', {})
            if repo_info:
                f.write(f"- **Language:** {repo_info.get('language', 'Unknown')}\n")
                f.write(f"- **Stars:** {repo_info.get('stars', 0)}\n")
                f.write(f"- **Forks:** {repo_info.get('forks', 0)}\n")
                f.write(f"- **Size:** {repo_info.get('size', 0)} KB\n")
                f.write(f"- **License:** {repo_info.get('license', 'No license')}\n\n")
            
            f.write("## File Analysis\n\n")
            files = data.get('files', [])
            for file_info in files:
                f.write(f"### {file_info['name']}\n")
                f.write(f"{file_info['summary']}\n\n")
            
            f.write("## Recent Commits\n\n")
            commits = data.get('commits', [])
            for commit in commits:
                f.write(f"- **{commit['sha']}** - {commit['message']} by {commit['author']}\n")
            
            f.write("\n## Contributors\n\n")
            contributors = data.get('contributors', [])
            for contributor in contributors:
                f.write(f"- **{contributor['login']}** - {contributor['contributions']} contributions\n")
            
            f.write(f"\n---\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return filepath
    
    def create_docx_report(self, data: Dict) -> str:
        """Create a DOCX report (simplified version without python-docx dependency)"""
        # For this demo, we'll create a text file instead of DOCX
        # In a real implementation, you'd use python-docx library
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"repo_analysis_{timestamp}.txt"
        filepath = os.path.join(self.temp_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("REPOSITORY ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Repository: {data.get('repo_name', 'Unknown')}\n")
            f.write(f"Analysis Date: {data.get('analysis_date', 'Unknown')}\n")
            f.write(f"Description: {data.get('description', 'No description available')}\n\n")
            
            f.write("REPOSITORY OVERVIEW\n")
            f.write("-" * 20 + "\n")
            repo_info = data.get('repo_info', {})
            if repo_info:
                f.write(f"Language: {repo_info.get('language', 'Unknown')}\n")
                f.write(f"Stars: {repo_info.get('stars', 0)}\n")
                f.write(f"Forks: {repo_info.get('forks', 0)}\n")
                f.write(f"Size: {repo_info.get('size', 0)} KB\n")
                f.write(f"License: {repo_info.get('license', 'No license')}\n\n")
            
            f.write("FILE ANALYSIS\n")
            f.write("-" * 15 + "\n")
            files = data.get('files', [])
            for file_info in files:
                f.write(f"\n{file_info['name']}:\n")
                f.write(f"  {file_info['summary']}\n")
            
            f.write(f"\n\nReport generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return filepath

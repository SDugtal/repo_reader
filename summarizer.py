import google.generativeai as genai
import os
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the same directory
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

class CodeSummarizer:
    def __init__(self):
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        self.model = None
        
        if self.gemini_api_key and self.gemini_api_key != 'your_gemini_api_key_here':
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini API configured successfully.")
            except Exception as e:
                print(f"❌ Failed to configure Gemini API: {e}")
                self.model = None
        else:
            print("❌ Gemini API key missing or invalid.")

    def is_code_file(self, filename: str) -> bool:
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.html', '.css', '.scss', '.less', '.sql', '.sh', '.bash',
            '.yml', '.yaml', '.json', '.xml', '.md', '.dockerfile'
        }
        return any(filename.lower().endswith(ext) for ext in code_extensions)

    def summarize_code(self, code_content: str, filename: str) -> Tuple[str, Dict]:
        usage_info = {
            'api_calls': 0,
            'tokens_used': 0,
            'method_used': 'rule_based',
            'model_used': None
        }

        try:
            if self.model:
                ai_summary, ai_usage = self._ai_summarize(code_content, filename)
                if ai_summary:
                    usage_info.update(ai_usage)
                    usage_info['method_used'] = 'ai'
                    return ai_summary, usage_info

            summary = self._rule_based_summary(code_content, filename)
            return summary, usage_info

        except Exception as e:
            print(f"❌ Error in summarize_code: {e}")
            summary = self._rule_based_summary(code_content, filename)
            return summary, usage_info

    def _ai_summarize(self, code_content: str, filename: str) -> Tuple[Optional[str], Dict]:
        usage_info = {
            'api_calls': 0,
            'tokens_used': 0,
            'model_used': 'gemini-1.5-flash'
        }

        try:
            prompt = self._create_analysis_prompt(code_content, filename)
            
            # Estimate token usage (Gemini counts tokens differently, but this is an approximation)
            usage_info['tokens_used'] = len(prompt) // 4

            print("🔁 Sending request to Gemini...")
            response = self.model.generate_content(prompt)
            usage_info['api_calls'] = 1

            if response and response.text:
                summary = self._clean_summary(response.text.strip())
                if summary:
                    return summary, usage_info
            else:
                print("❌ Gemini API returned empty response")

            return None, usage_info

        except Exception as e:
            print(f"❌ Exception in _ai_summarize: {e}")
            return None, usage_info

    def _create_analysis_prompt(self, code_content: str, filename: str) -> str:
        file_type = self._get_file_type(filename)
        
        # Truncate code if too long to avoid token limits
        if len(code_content) > 8000:
            code_content = code_content[:8000] + "\n... (truncated)"
        
        return f"""Analyze this {file_type} code and provide a concise, technical summary in 1-2 sentences.

File: {filename}
Code:
{code_content}

Please provide a brief summary that describes:
1. What this code does (main purpose/functionality)
2. Key components (classes, functions, modules used)
3. Any notable patterns or complexity

Keep the summary concise and technical, starting directly with the description (no "This code" prefix)."""

    def _clean_summary(self, summary: str) -> str:
        # Remove common prefixes
        for prefix in ["This code", "The code", "Summary:", "This file", "The file", "This script", "The script"]:
            if summary.lower().startswith(prefix.lower()):
                summary = summary[len(prefix):].strip()
                break
        
        # Remove leading colons or dashes
        summary = summary.lstrip(':- ').strip()
        
        # Ensure proper capitalization
        if summary and not summary[0].isupper():
            summary = summary[0].upper() + summary[1:]
        
        # Ensure it ends with a period
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary

    def _rule_based_summary(self, code_content: str, filename: str) -> str:
        lines = code_content.splitlines()
        total_lines = len(lines)
        file_type = self._get_file_type(filename)
        analysis = self._analyze_code_structure(lines, file_type)

        summary = [f"This {file_type} file contains {total_lines} lines of code"]
        
        if analysis['functions']:
            summary.append(f"{analysis['functions']} function(s)")
        if analysis['classes']:
            summary.append(f"{analysis['classes']} class(es)")
        if analysis['imports']:
            summary.append(f"{analysis['imports']} import(s)")
        if analysis['purpose']:
            summary.append(f"Purpose: {analysis['purpose']}")
        if analysis['complexity'] == 'high':
            summary.append("appears to be complex with multiple components")
        elif analysis['complexity'] == 'medium':
            summary.append("has moderate complexity")

        return ". ".join(summary) + '.'

    def _analyze_code_structure(self, lines: list, file_type: str) -> Dict:
        analysis = {'functions': 0, 'classes': 0, 'imports': 0, 'purpose': '', 'complexity': 'low'}
        
        for line in lines:
            s = line.strip()
            if any(p in s for p in ['def ', 'function ', 'func ', 'fn ']):
                analysis['functions'] += 1
            if any(p in s for p in ['class ', 'interface ', 'struct ']):
                analysis['classes'] += 1
            if any(s.startswith(p) for p in ['import ', 'from ', '#include', 'require(', 'use ']):
                analysis['imports'] += 1

        # Look for purpose in comments
        for line in lines[:15]:
            s = line.strip()
            if any(s.startswith(p) for p in ['# ', '// ', '/* ', '* ', '"""', "'''"]):
                comment = s
                for p in ['# ', '// ', '/* ', '* ', '"""', "'''"]:
                    comment = comment.replace(p, '').strip()
                if len(comment) > 20 and not comment.lower().startswith(('todo', 'fixme', 'hack')):
                    analysis['purpose'] = comment[:100] + ('...' if len(comment) > 100 else '')
                    break

        # Determine complexity
        total = analysis['functions'] + analysis['classes']
        if total > 10:
            analysis['complexity'] = 'high'
        elif total > 3:
            analysis['complexity'] = 'medium'

        return analysis

    def get_token_usage_estimate(self, text: str) -> int:
        return max(1, len(text) // 4)

    def _get_file_type(self, filename: str) -> str:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        type_map = {
            'py': 'Python', 'js': 'JavaScript', 'ts': 'TypeScript',
            'jsx': 'React JSX', 'tsx': 'React TSX', 'java': 'Java',
            'cpp': 'C++', 'c': 'C', 'cs': 'C#', 'php': 'PHP',
            'rb': 'Ruby', 'go': 'Go', 'rs': 'Rust', 'swift': 'Swift',
            'kt': 'Kotlin', 'html': 'HTML', 'css': 'CSS',
            'scss': 'SCSS', 'sql': 'SQL', 'sh': 'Shell Script',
            'yml': 'YAML', 'yaml': 'YAML', 'json': 'JSON',
            'xml': 'XML', 'md': 'Markdown'
        }
        return type_map.get(ext, 'Code')

# Example usage
if __name__ == "__main__":
    summarizer = CodeSummarizer()
    
    # Test with a sample code file
    sample_code = '''
def fibonacci(n):
    """Calculate the nth Fibonacci number using recursion."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
    '''
    
    summary, usage = summarizer.summarize_code(sample_code, "fibonacci.py")
    print(f"Summary: {summary}")
    print(f"Usage: {usage}")

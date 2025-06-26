import requests
import os
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the same directory
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

class CodeSummarizer:
    def __init__(self):
        self.hf_token = os.environ.get('HUGGING_FACE_TOKEN')
        self.headers = {}

        if self.hf_token and self.hf_token != 'your_hugging_face_token_here':
            self.headers['Authorization'] = f'Bearer {self.hf_token}'
            print("✅ Authorization header set.")
        else:
            print("❌ Hugging Face token missing or invalid.")

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
            if self.hf_token:
                ai_summary, ai_usage = self._ai_summarize(code_content, filename)
                if ai_summary:
                    usage_info.update(ai_usage)
                    usage_info['method_used'] = 'ai'
                    return ai_summary, usage_info

            summary = self._rule_based_summary(code_content, filename)
            return summary, usage_info

        except Exception:
            summary = self._rule_based_summary(code_content, filename)
            return summary, usage_info

    def _ai_summarize(self, code_content: str, filename: str) -> Tuple[Optional[str], Dict]:
        usage_info = {
            'api_calls': 0,
            'tokens_used': 0,
            'model_used': 'bigcode/starcoder'
        }

        try:
            model_url = self._get_best_model_for_file(filename)
            prompt = self._create_analysis_prompt(code_content, filename)

            code_content = code_content[:1000] + "..." if len(code_content) > 1000 else code_content
            usage_info['tokens_used'] = len(code_content) // 4

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "min_length": 30,
                    "do_sample": False,
                    "temperature": 0.1
                }
            }

            print("🔁 Sending request to Hugging Face...")
            response = requests.post(model_url, headers=self.headers, json=payload, timeout=10)
            usage_info['api_calls'] = 1

            if response.status_code == 200:
                result = response.json()
                summary = self._extract_summary_from_response(result)
                if summary:
                    return summary, usage_info
            else:
                print(f"❌ Hugging Face API returned status {response.status_code}: {response.text}")

            return None, usage_info

        except Exception as e:
            print("❌ Exception in _ai_summarize:", e)
            return None, usage_info
        def _get_best_model_for_file(self, filename: str) -> str:
            return "https://api-inference.huggingface.co/models/bigcode/santacoder"



    def _create_analysis_prompt(self, code_content: str, filename: str) -> str:
        file_type = self._get_file_type(filename)
        return f"""Analyze this {file_type} code and provide a concise summary:

File: {filename}
Code:
{code_content}

Summary: This code"""

    def _extract_summary_from_response(self, response_data) -> Optional[str]:
        try:
            if isinstance(response_data, list) and response_data:
                first = response_data[0]
                for key in ['summary_text', 'generated_text', 'text']:
                    if key in first:
                        return self._clean_summary(first[key].strip())
            return None
        except Exception:
            return None

    def _clean_summary(self, summary: str) -> str:
        for prefix in ["This code", "The code", "Summary:", "This file", "The file"]:
            if summary.startswith(prefix):
                summary = summary[len(prefix):].strip()
        if summary and not summary[0].isupper():
            summary = summary[0].upper() + summary[1:]
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

        for line in lines[:15]:
            s = line.strip()
            if any(s.startswith(p) for p in ['# ', '// ', '/* ', '* ', '"""', "'''"]):
                comment = s
                for p in ['# ', '// ', '/* ', '* ', '"""', "'''"]:
                    comment = comment.replace(p, '').strip()
                if len(comment) > 20 and not comment.lower().startswith(('todo', 'fixme', 'hack')):
                    analysis['purpose'] = comment[:100] + ('...' if len(comment) > 100 else '')
                    break

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

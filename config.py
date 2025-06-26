import os
from dotenv import load_dotenv

load_dotenv()

# GitHub configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

# AI API configuration (using free options)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Free tier available
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')  # Free tier available
AI_PROVIDER = 'huggingface'  # or 'openai'

# Output configuration
OUTPUT_DIR = 'output'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'repos_summary.md')
# Add to config.py
WKHTMLTOPDF_PATH = os.getenv('WKHTMLTOPDF_PATH')
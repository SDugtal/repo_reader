# GitHub Repository Documenter

An AI-powered tool for generating comprehensive documentation for GitHub repositories.

## Features

- **AI-Powered Analysis**: Leverages AI to analyze repository structure, code, and documentation
- **Multiple Output Formats**: Generate documentation in Markdown, HTML, PDF, and DOCX formats
- **Web Interface**: Clean, user-friendly Flask web application
- **Repository Insights**: Extract key features, technology stack, and statistics
- **Smart Recommendations**: AI-generated suggestions for repository improvements

## Project Structure

```
github_repo_documenter/
│── app.py                  # Flask web interface
│── document_generator.py   # Core functionality (updated with AI)
│── ai_helpers.py           # New AI integration module
│── templates/              
│   ├── index.html
│   └── report.html
│── static/                 
│   ├── css/
│   ├── js/
│   └── charts/
│── config.py               # Updated configuration
│── requirements.txt        # Updated dependencies
│── output/                 
│   ├── repos_summary.md
│   ├── repos_summary.pdf
│   ├── repos_summary.html
│   └── repos_summary.docx
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your API keys
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Navigate to `http://localhost:5000`
2. Enter a GitHub repository URL
3. Select desired output formats
4. Click "Generate Documentation"
5. Download the generated files

## Configuration

Configure the application by setting environment variables in the `.env` file:

- `GITHUB_TOKEN`: GitHub API token for higher rate limits
- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `ANTHROPIC_API_KEY`: Anthropic API key for AI analysis


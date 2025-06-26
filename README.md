<<<<<<< HEAD
# GitHub Repo Reader

A Flask web application that analyzes GitHub repositories using AI-powered code analysis and provides comprehensive insights about the codebase.

## Features

- 📊 **Repository Analysis**: Get detailed information about any public GitHub repository
- 🤖 **AI-Powered Code Summarization**: Uses Hugging Face models to analyze and summarize code files
- 📈 **Commit History**: View recent commits and contributor activity
- 👥 **Contributor Insights**: See top contributors and their contributions
- 📄 **Export Reports**: Download analysis reports in Markdown or text format
- 🎨 **Modern UI**: Clean, responsive interface built with Tailwind CSS

## Installation

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd github-repo-reader
\`\`\`

2. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Set up environment variables:
\`\`\`bash
cp .env.example .env
# Edit .env with your API tokens
\`\`\`

5. Run the application:
\`\`\`bash
python app.py
\`\`\`

The application will be available at \`http://localhost:5000\`

## Environment Variables

- \`GITHUB_TOKEN\`: GitHub personal access token (optional, for higher rate limits)
- \`HUGGING_FACE_TOKEN\`: Hugging Face API token (optional, for AI features)
- \`SECRET_KEY\`: Flask secret key for session management

## API Endpoints

- \`GET /\`: Main application interface
- \`POST /analyze\`: Analyze a GitHub repository
- \`GET /export/<format>\`: Export analysis report (md/docx)
- \`GET /health\`: Health check endpoint

## Usage

1. Enter a GitHub repository URL (e.g., \`https://github.com/username/repo\`)
2. Click "Analyze Repository"
3. View the comprehensive analysis including:
   - Repository metadata and statistics
   - AI-generated code summaries
   - Recent commit history
   - Top contributors
4. Export the results as Markdown or document files

## AI Models Used

- **Hugging Face Inference API**: For code summarization and analysis
- **Fallback Analysis**: Rule-based analysis when AI services are unavailable

## Rate Limits

- GitHub API: 60 requests/hour (unauthenticated), 5000 requests/hour (with token)
- Hugging Face API: Varies by model and account type

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
=======
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

>>>>>>> 54089dd76f0f3700af83b8e07eecec5aebed2144

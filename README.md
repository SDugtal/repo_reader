# GitHub Repo Reader

A Flask web application that analyzes GitHub repositories using AI-powered code analysis and provides comprehensive insights about the codebase.

## Features

- 📊 **Repository Analysis**: Get detailed information about any public GitHub repository
- 🤖 **AI-Powered Code Summarization**: Uses Google's Gemini AI to analyze and summarize code files
- 📈 **Commit History**: View recent commits and contributor activity
- 👥 **Contributor Insights**: See top contributors and their contributions
- 📄 **Export Reports**: Download analysis reports in Markdown or text format
- 🎨 **Modern UI**: Clean, responsive interface built with Tailwind CSS
- 🔄 **Smart Fallback**: Rule-based analysis when AI services are unavailable

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
- \`GEMINI_API_KEY\`: Google Gemini API key (required for AI features)
- \`SECRET_KEY\`: Flask secret key for session management

## Getting API Keys

### GitHub Token (Optional)
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token with \`public_repo\` scope
3. Add it to your \`.env\` file

### Gemini API Key (Required for AI Features)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your \`.env\` file as \`GEMINI_API_KEY\`

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
   - AI-generated code summaries powered by Gemini
   - Recent commit history
   - Top contributors
   - Code complexity analysis
4. Export the results as Markdown or document files

## AI Models Used

- **Google Gemini 1.5 Flash**: Primary model for code summarization and analysis
- **Fallback Analysis**: Rule-based analysis when AI services are unavailable

## Features in Detail

### Code Analysis
- Intelligent code summarization using Gemini AI
- Support for 20+ programming languages
- Function and class detection
- Import and dependency analysis
- Code complexity assessment

### Repository Insights
- Repository statistics and metadata
- Contributor analysis and activity
- Commit history and patterns
- File structure analysis
- Technology stack detection

### Export Options
- Markdown reports for documentation
- Text summaries for quick reference
- Structured data for further processing

## Rate Limits

- **GitHub API**: 60 requests/hour (unauthenticated), 5000 requests/hour (with token)
- **Gemini API**: Varies by usage tier and account type

## Supported File Types

The application can analyze the following file types:
- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h)
- C# (.cs)
- PHP (.php)
- Ruby (.rb)
- Go (.go)
- Rust (.rs)
- Swift (.swift)
- Kotlin (.kt)
- HTML/CSS (.html, .css, .scss)
- SQL (.sql)
- Shell scripts (.sh, .bash)
- Configuration files (.yml, .yaml, .json, .xml)
- Documentation (.md)

## Contributing

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (\`git commit -m 'Add amazing feature'\`)
6. Push to the branch (\`git push origin feature/amazing-feature\`)
7. Submit a pull request


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

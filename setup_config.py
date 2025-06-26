#!/usr/bin/env python3
"""
Quick setup script to configure your GitHub Repo Reader
"""
import os
import secrets
from dotenv import load_dotenv

def generate_secret_key():
    """Generate a cryptographically secure secret key"""
    return secrets.token_hex(32)

def setup_environment():
    """Set up the .env file with proper configuration"""
    print("🔧 Setting up GitHub Repo Reader configuration...")
    
    # Check if .env exists
    env_exists = os.path.exists('.env')
    
    if env_exists:
        print("📄 Found existing .env file")
        load_dotenv()
    else:
        print("📄 Creating new .env file")
    
    # Generate new secret key
    secret_key = generate_secret_key()
    
    # Get current tokens if they exist
    github_token = os.environ.get('GITHUB_TOKEN', '')
    hf_token = os.environ.get('HUGGING_FACE_TOKEN', '')
    
    # Create .env content
    env_content = f"""# GitHub Repo Reader Configuration
# Generated on {os.popen('date').read().strip()}

# Flask Secret Key (KEEP THIS SECRET!)
SECRET_KEY={secret_key}

# GitHub API Token (optional, for higher rate limits)
# Get from: https://github.com/settings/tokens
# Permissions needed: public_repo (read access)
GITHUB_TOKEN={github_token if github_token else 'your_github_token_here'}

# Hugging Face API Token (optional, for AI features)
# Get from: https://huggingface.co/settings/tokens  
# Permissions needed: Read access
HUGGING_FACE_TOKEN={hf_token if hf_token else 'your_hugging_face_token_here'}

# Optional: Set to production for deployment
FLASK_ENV=development
"""
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created/updated successfully!")
    print(f"🔑 Generated new secret key: {secret_key[:16]}...")
    
    return secret_key

def show_token_setup_instructions():
    """Show instructions for setting up API tokens"""
    print("\n" + "="*60)
    print("🔑 API TOKEN SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ GITHUB TOKEN (Recommended for higher rate limits):")
    print("   • Go to: https://github.com/settings/tokens")
    print("   • Click 'Generate new token (classic)'")
    print("   • Select scopes: 'public_repo' (for public repositories)")
    print("   • Copy the token and add to .env file")
    print("   • Without token: 60 requests/hour")
    print("   • With token: 5,000 requests/hour")
    
    print("\n2️⃣ HUGGING FACE TOKEN (For AI-powered analysis):")
    print("   • Go to: https://huggingface.co/settings/tokens")
    print("   • Click 'New token'")
    print("   • Select 'Read' permission")
    print("   • Copy the token and add to .env file")
    print("   • Without token: Rule-based analysis only")
    print("   • With token: AI-powered code summaries")

def check_current_setup():
    """Check current configuration status"""
    print("\n" + "="*60)
    print("📊 CURRENT CONFIGURATION STATUS")
    print("="*60)
    
    load_dotenv()
    
    # Check secret key
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key and secret_key != 'dev-key-change-in-production':
        print("✅ Flask Secret Key: Configured")
    else:
        print("❌ Flask Secret Key: Using default (insecure)")
    
    # Check GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token and github_token != 'your_github_token_here':
        print("✅ GitHub Token: Configured")
        print("   📈 Rate limit: 5,000 requests/hour")
    else:
        print("⚠️  GitHub Token: Not configured")
        print("   📉 Rate limit: 60 requests/hour")
    
    # Check Hugging Face token
    hf_token = os.environ.get('HUGGING_FACE_TOKEN')
    if hf_token and hf_token != 'your_hugging_face_token_here':
        print("✅ Hugging Face Token: Configured")
        print("   🤖 AI Analysis: Enabled")
    else:
        print("⚠️  Hugging Face Token: Not configured")
        print("   🔧 AI Analysis: Rule-based only")

def main():
    print("🚀 GitHub Repo Reader - Configuration Setup")
    print("="*50)
    
    # Setup environment
    secret_key = setup_environment()
    
    # Show current status
    check_current_setup()
    
    # Show setup instructions
    show_token_setup_instructions()
    
    print("\n" + "="*60)
    print("🎯 NEXT STEPS")
    print("="*60)
    print("1. Add your API tokens to the .env file")
    print("2. Restart your Flask app: python app.py")
    print("3. Test with a GitHub repository URL")
    
    print("\n💡 QUICK TEST:")
    print("   • Try: https://github.com/octocat/Hello-World")
    print("   • Or any public GitHub repository")
    
    print("\n🔒 SECURITY NOTE:")
    print("   • Never commit .env file to version control")
    print("   • Keep your tokens secret")
    print("   • Regenerate tokens if compromised")

if __name__ == "__main__":
    main()

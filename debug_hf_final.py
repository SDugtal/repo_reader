#!/usr/bin/env python3
"""
Final Hugging Face debugging - find the exact issue
"""
import requests
import os
from dotenv import load_dotenv
import json

def comprehensive_hf_debug():
    """Complete Hugging Face debugging"""
    print("🔍 COMPREHENSIVE HUGGING FACE DEBUG")
    print("=" * 45)
    
    load_dotenv()
    
    # Step 1: Environment Check
    print("\n1️⃣ ENVIRONMENT CHECK")
    print("-" * 25)
    
    hf_token = os.environ.get('HUGGING_FACE_TOKEN')
    
    if not hf_token:
        print("❌ CRITICAL: No HUGGING_FACE_TOKEN found in environment")
        print("🔧 Check your .env file exists and has the token")
        return False
    
    if hf_token == 'your_hugging_face_token_here':
        print("❌ CRITICAL: Still using placeholder token")
        print("🔧 Replace with your actual Hugging Face token")
        return False
    
    print(f"✅ Token found: {hf_token[:15]}...")
    print(f"📏 Token length: {len(hf_token)} characters")
    
    if not hf_token.startswith('hf_'):
        print("⚠️  WARNING: Token doesn't start with 'hf_'")
        print("💡 Most valid tokens start with 'hf_'")
    
    # Step 2: Basic Authentication Test
    print("\n2️⃣ AUTHENTICATION TEST")
    print("-" * 28)
    
    headers = {'Authorization': f'Bearer {hf_token}'}
    
    try:
        print("🔍 Testing authentication...")
        response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Authentication SUCCESS!")
            print(f"   👤 User: {user_data.get('name', 'Unknown')}")
            print(f"   📧 Email: {user_data.get('email', 'Not provided')}")
            print(f"   🏷️  Type: {user_data.get('type', 'Unknown')}")
        elif response.status_code == 401:
            print("❌ AUTHENTICATION FAILED (401)")
            print(f"📄 Response: {response.text}")
            print("\n🔧 POSSIBLE FIXES:")
            print("   1. Token is invalid/expired")
            print("   2. Token was copied incorrectly")
            print("   3. Token doesn't exist")
            return False
        elif response.status_code == 403:
            print("❌ ACCESS FORBIDDEN (403)")
            print(f"📄 Response: {response.text}")
            print("\n🔧 POSSIBLE FIXES:")
            print("   1. Token doesn't have 'read' permissions")
            print("   2. Account has restrictions")
            return False
        else:
            print(f"❌ UNEXPECTED STATUS: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ REQUEST TIMEOUT")
        print("🔧 Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR")
        print("🔧 Check internet/firewall settings")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False
    
    # Step 3: Inference API Test
    print("\n3️⃣ INFERENCE API TEST")
    print("-" * 26)
    
    models_to_test = [
        'microsoft/codebert-base',
        'distilbert-base-uncased',
        'facebook/bart-large-cnn'
    ]
    
    working_models = []
    
    for model in models_to_test:
        print(f"\n🧠 Testing model: {model}")
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        test_payload = {
            "inputs": "def hello(): print('test')",
            "parameters": {"max_length": 50}
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=test_payload, timeout=20)
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS - Model working!")
                working_models.append(model)
                result = response.json()
                print(f"   📄 Sample response: {str(result)[:100]}...")
            elif response.status_code == 503:
                print("   ⏳ Model loading (this is normal)")
                working_models.append(f"{model} (loading)")
            elif response.status_code == 401:
                print("   ❌ Authentication failed for inference")
                print("   🔧 Token doesn't have inference permissions")
            elif response.status_code == 429:
                print("   ⚠️  Rate limited")
                print("   💡 Too many requests, but token works")
                working_models.append(f"{model} (rate limited)")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"   📄 Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Step 4: Test Your App's Code
    print("\n4️⃣ TESTING YOUR APP'S CODE")
    print("-" * 32)
    
    try:
        print("🔍 Testing your summarizer code...")
        from summarizer import CodeSummarizer
        
        summarizer = CodeSummarizer()
        test_code = "def hello_world():\n    print('Hello, World!')\n    return True"
        
        summary, usage = summarizer.summarize_code(test_code, "test.py")
        
        print(f"✅ Summarizer works!")
        print(f"   📄 Summary: {summary}")
        print(f"   🔧 Method: {usage.get('method_used', 'unknown')}")
        print(f"   🤖 AI calls: {usage.get('api_calls', 0)}")
        print(f"   🎯 Tokens used: {usage.get('tokens_used', 0)}")
        
        if usage.get('api_calls', 0) > 0:
            print("🎉 AI ANALYSIS IS WORKING!")
            return True
        else:
            print("⚠️  Using rule-based analysis only")
            
    except Exception as e:
        print(f"❌ App code error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print(f"\n📊 SUMMARY")
    print("-" * 15)
    print(f"Working models: {len(working_models)}")
    for model in working_models:
        print(f"   ✅ {model}")
    
    return len(working_models) > 0

def show_exact_fix():
    """Show the exact steps to fix the issue"""
    print("\n🔧 EXACT FIX STEPS")
    print("=" * 20)
    
    print("\n1️⃣ Get a FRESH token:")
    print("   🌐 https://huggingface.co/settings/tokens")
    print("   🔘 Click 'New token'")
    print("   📝 Name: 'GitHub Repo Reader'")
    print("   🔘 Type: 'Read' (NOT Write or Fine-grained)")
    print("   📋 Copy the ENTIRE token")
    
    print("\n2️⃣ Update your .env file:")
    print("   📝 Open .env file")
    print("   ✏️  Replace the line:")
    print("   HUGGING_FACE_TOKEN=your_new_token_here")
    
    print("\n3️⃣ Restart everything:")
    print("   🔄 Close your terminal")
    print("   🔄 Open new terminal")
    print("   🚀 Run: python app.py")

def interactive_token_fix():
    """Interactive token replacement"""
    print("\n🔧 INTERACTIVE TOKEN FIX")
    print("=" * 30)
    
    print("Let's fix your token right now!")
    
    # Get new token
    print("\n📝 Get your token from: https://huggingface.co/settings/tokens")
    new_token = input("Paste your NEW Hugging Face token here: ").strip()
    
    if not new_token:
        print("❌ No token provided")
        return False
    
    # Test new token immediately
    print(f"\n🧪 Testing token: {new_token[:15]}...")
    
    headers = {'Authorization': f'Bearer {new_token}'}
    
    try:
        response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Token works! User: {user_data.get('name', 'Unknown')}")
            
            # Save to .env
            print("💾 Saving to .env file...")
            
            # Read current .env
            env_lines = []
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    env_lines = f.readlines()
            
            # Update HF token
            hf_updated = False
            for i, line in enumerate(env_lines):
                if line.startswith('HUGGING_FACE_TOKEN='):
                    env_lines[i] = f'HUGGING_FACE_TOKEN={new_token}\n'
                    hf_updated = True
                    break
            
            if not hf_updated:
                env_lines.append(f'HUGGING_FACE_TOKEN={new_token}\n')
            
            # Write back
            with open('.env', 'w') as f:
                f.writelines(env_lines)
            
            print("✅ Token saved!")
            print("🔄 Now restart your app: python app.py")
            return True
        else:
            print(f"❌ Token test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Token test error: {e}")
        return False

def main():
    """Main debugging function"""
    print("🚨 FINAL HUGGING FACE DEBUG")
    print("=" * 35)
    
    # Run comprehensive debug
    is_working = comprehensive_hf_debug()
    
    if is_working:
        print("\n🎉 HUGGING FACE IS WORKING!")
        print("💡 If your app still shows ❌, restart it:")
        print("   python app.py")
    else:
        print("\n❌ HUGGING FACE NOT WORKING")
        
        # Show fix steps
        show_exact_fix()
        
        # Offer interactive fix
        fix_now = input("\n🔧 Fix the token now? (y/n): ").lower()
        if fix_now == 'y':
            success = interactive_token_fix()
            if success:
                print("\n🎉 FIXED! Restart your app now!")

if __name__ == "__main__":
    main()

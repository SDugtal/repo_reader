import requests
import config
from typing import Optional
import time
import warnings

# Configuration
HF_API_TIMEOUT = 30  # Increased timeout
HF_RETRY_DELAY = 5   # Seconds between retries
MAX_RETRIES = 3      # Max retry attempts

warnings.filterwarnings("ignore")

def _clean_content(text: str) -> str:
    """Prepare repository content for AI processing"""
    return text.replace('```', '').replace('#', '').strip()[:1500]

def _build_prompt(repo_name: str, content: str) -> str:
    """Construct an effective prompt for the AI"""
    return (
        f"Create a professional 2-sentence description for GitHub repository '{repo_name}'.\n"
        "First sentence: State the project's main purpose and technology stack.\n"
        "Second sentence: Highlight 2-3 key features or components.\n"
        "Be specific and technical. Example format:\n"
        "'[Repo] - A [language] application for [purpose] using [technologies]. "
        "Features include [feature1], [feature2], and [feature3].'\n\n"
        f"Repository content:\n{content}"
    )

def _format_output(result: dict, repo_name: str) -> str:
    """Extract and format the AI's response"""
    if isinstance(result, list):
        text = result[0].get('generated_text', '')
    else:
        text = result.get('generated_text', '')
    
    # Clean and format the output
    text = text.replace('\n', ' ').strip()
    if not text.endswith('.'):
        text += '.'
    
    # Ensure repo name is included
    if not text.lower().startswith(repo_name.lower()):
        text = f"{repo_name} - {text}"
    
    return text

def generate_ai_description(repo_name: str, repo_content: str) -> str:
    """Robust AI description generator with enhanced reliability"""
    models = [
        ("facebook/bart-large-cnn", _query_summarization_model),
        ("google/flan-t5-large", _query_text_generation_model),
        ("gpt2", _query_text_generation_model)  # Fallback
    ]
    
    clean_content = _clean_content(repo_content)
    prompt = _build_prompt(repo_name, clean_content)

    for model_name, query_func in models:
        for attempt in range(MAX_RETRIES):
            try:
                result = query_func(model_name, prompt)
                if result:
                    formatted = _format_output(result, repo_name)
                    if len(formatted.split()) > 5:  # Basic quality check
                        return formatted
            except Exception as e:
                print(f"⚠️ [Attempt {attempt+1}/{MAX_RETRIES}] {model_name} failed: {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(HF_RETRY_DELAY)
    
    # Final fallback
    return f"{repo_name} - A professional project repository containing source code and documentation."

def _query_summarization_model(model: str, prompt: str) -> Optional[dict]:
    """Query models specialized for summarization"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 150,
            "min_length": 50,
            "do_sample": True
        }
    }
    return _call_huggingface_api(model, payload)

def _query_text_generation_model(model: str, prompt: str) -> Optional[dict]:
    """Query general text generation models"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }
    return _call_huggingface_api(model, payload)

def _call_huggingface_api(model: str, payload: dict) -> Optional[dict]:
    """Core API call with enhanced error handling"""
    headers = {"Authorization": f"Bearer {config.HUGGINGFACE_API_KEY}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=HF_API_TIMEOUT
        )
        
        # Handle model loading
        if response.status_code == 503:
            wait_time = min(response.json().get('estimated_time', 30), 60)
            print(f"⏳ Model loading, waiting {wait_time}s...")
            time.sleep(wait_time)
            response = requests.post(API_URL, headers=headers, json=payload, timeout=HF_API_TIMEOUT)
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        raise Exception(f"Timeout after {HF_API_TIMEOUT}s")
    except Exception as e:
        raise Exception(f"API error: {str(e)}")
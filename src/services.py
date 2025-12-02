import concurrent.futures
import google.generativeai as genai
from config import settings
import requests

def get_gemini_model():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(settings.MODEL_NAME)

def get_multiline_input():
    """
    Captures multi-line text pasted into the terminal.
    Stops only when the user types 'DONE' on a new line.
    """
    print("\n" + "="*40)
    print("  PASTE JOB DESCRIPTION BELOW.")
    print("  When finished, type 'DONE' on a new line and hit Enter.")
    print("="*40 + "\n")
    
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        # Check for the stop signal
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    
    text = "\n".join(lines)
    print(f"\n  [IO] Captured {len(text)} characters.")
    return text

def get_job_content(user_input):
    """Fetches Job Description via Jina (if URL) or returns raw text."""
    user_input = user_input.strip()
    
    # CASE A: It's a URL
    if user_input.startswith("http"):
        print(f"  [IO] Detected URL. Fetching via Jina Reader...")
        try:
            jina_url = f"https://r.jina.ai/{user_input}"
            response = requests.get(jina_url, timeout=10)
            content = response.text
            
            # Validation: Check for blocks or short content
            block_signals = ["Sign in", "Join LinkedIn", "Authwall", "Security Check"]
            if response.status_code != 200 or any(s in content for s in block_signals) or len(content) < 500:
                print("  [!] Warning: Link blocked. Please paste manual text.")
                return get_multiline_input()
            
            return content
        except Exception as e:
            print(f"  [!] Network Error: {e}")
            return get_multiline_input()
            
    # CASE B: User explicitly wants to paste text (Input was empty or short)
    else:
        return get_multiline_input()
    

def import_json_safe(json_text):
    """
    Robust JSON parser that handles markdown fences and lists.
    """
    try:
        # 1. Strip Markdown fences if the LLM added them
        clean_text = json_text.replace("```json", "").replace("```", "").strip()
        
        # 2. Parse
        data = json.loads(clean_text)
        
        # 3. Handle List vs Dict (The Fix for your error)
        if isinstance(data, list):
            if len(data) > 0:
                return data[0] # Take the first object
            else:
                return {} # Return empty dict if list is empty
        
        return data
    except Exception:
        # Fallback defaults if parsing fails entirely
        return {"company": "Company", "role": "Software Engineer", "address": ""}


def extract_job_metadata(model, job_text):
    """Extracts Company Name and Job Title."""
    print("  [AI] Extracting Job Metadata (Company/Role)...")
    prompt = f"""
    Extract the following details from the Job Description as JSON:
    {{
        "company": "Name of Company (e.g. Google)",
        "role": "Job Title (e.g. Software Engineer)",
        "address": "Street Address or City, State (if found, else leave empty)"
    }}
    
    JOB DESCRIPTION:
    {job_text[:5000]}
    """
    try:
        # We request JSON specifically
        response = model.generate_content(
            prompt, 
            generation_config={"response_mime_type": "application/json"}
        )
        return import_json_safe(response.text)
    except Exception as e:
        print(f"    [!] Metadata extraction warning: {e}")
        return {"company": "Company", "role": "Software Engineer", "address": ""}

def fetch_single_readme(url):
    path = url.replace("https://github.com/", "").strip("/")
    branches = ["main", "master"]
    for branch in branches:
        try:
            raw_url = f"https://raw.githubusercontent.com/{path}/{branch}/README.md"
            resp = requests.get(raw_url, timeout=5)
            if resp.status_code == 200:
                return resp.text
        except:
            continue
    return None

def fetch_readmes_parallel():
    print("  [IO] Fetching GitHub READMEs in parallel...")
    project_docs = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_title = {executor.submit(fetch_single_readme, url): title for title, url in settings.PROJECT_REPO_MAP.items()}
        for future in concurrent.futures.as_completed(future_to_title):
            title = future_to_title[future]
            try:
                data = future.result()
                if data:
                    print(f"    [+] Loaded: {title}")
                    project_docs[title] = data[:8000]
            except Exception: pass
    return project_docs

def generate_strategy(model, job_text):
    print("  [AI] Analyzing Job Strategy...")
    prompt = f"Analyze this job description... (Keep your previous prompt logic here)... JOB: {job_text[:15000]}"
    response = model.generate_content(prompt)
    return response.text
import os
import re
from src import services, resume, cover_letter

def sanitize_filename(name):
    """
    Turns 'Google Inc.' into 'Google_Inc' and removes bad characters.
    """
    # Remove non-alphanumeric chars (except spaces/underscores)
    clean = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces with underscores
    return clean.strip().replace(' ', '_')

def main():
    print("=== Career Automator v2.1 ===")
    
    # 1. Initialize
    try:
        model = services.get_gemini_model()
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        return

    # 2. Ingestion
    job_input = input("\nEnter Job URL (or paste description): ")
    job_text = services.get_job_content(job_input)
    if not job_text: return

    # 3. Strategy & Metadata (The "Brain")
    # We now fetch metadata here so we can use it for file naming later
    job_strategy = services.generate_strategy(model, job_text)
    meta_data = services.extract_job_metadata(model, job_text) 
    readmes = services.fetch_readmes_parallel()
    
    context = {
        "job_text": job_text,
        "job_strategy": job_strategy,
        "readmes": readmes
    }

    # 4. Execution
    # --- Resume ---
    resume_latex = resume.optimize_resume(context, model)
    
    # --- Cover Letter ---
    # Pass meta_data explicitly
    cl_latex = cover_letter.write_cover_letter(context, model, meta_data)

    # 5. Output with Dynamic Naming
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Clean the company name for the file system
    company_name = sanitize_filename(meta_data.get('company', 'Company'))
    
    # Construct Filenames: Andrew_Obwocha_(DocType)_(Company).tex
    resume_filename = f"Andrew_Obwocha_Resume_{company_name}.tex"
    cl_filename = f"Andrew_Obwocha_CoverLetter_{company_name}.tex"

    resume_path = os.path.join(output_dir, resume_filename)
    cl_path = os.path.join(output_dir, cl_filename)

    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(resume_latex)
        
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl_latex)

    print(f"\nSUCCESS! Generated for {company_name}:")
    print(f"1. {resume_path}")
    print(f"2. {cl_path}")

if __name__ == "__main__":
    main()
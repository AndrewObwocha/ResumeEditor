import re
import os
import requests
import concurrent.futures
import google.generativeai as genai
from dotenv import load_dotenv

# ==============================================================================
# 1. CONFIGURATION & AUTH (GEMINI)
# ==============================================================================

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Error: GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)

# Initialize the Flash model (Fast & Cheap)
model = genai.GenerativeModel('gemini-2.0-flash')

# GitHub Repos Mapped to Resume Titles
PROJECT_REPO_MAP = {
    "Knowledge Graph": "https://github.com/AndrewObwocha/GraphMind",
    "Tokenized Note System": "https://github.com/AndrewObwocha/UniNotes",
    "House Forecaster": "https://github.com/AndrewObwocha/HouseValuator",
}

# Your Raw LaTeX Source
LATEX_SOURCE = r"""
\documentclass[11pt]{article}
\usepackage[margin=0.5in]{geometry}
\usepackage{enumitem}
\usepackage[colorlinks=true, urlcolor=blue]{hyperref}
\usepackage{titlesec}

% Variables
\newcommand{\Name}{Andrew Obwocha}
\newcommand{\Email}{aobwocha@ualberta.ca}
\newcommand{\Phone}{(780)-717-0986}
\newcommand{\Github}{https://github.com/AndrewObwocha}
\newcommand{\Linkedin}{https://linkedin.com/in/andrewobwocha}

% Section Formatting
\newcommand{\ressection}[1]{%
  \begin{center}
    {\normalsize\bfseries\MakeUppercase{#1}}\\[4pt]
    \hrule
  \end{center}
  \vspace{-4pt}%
}

\begin{document}

% Header
\begin{center}
    {\LARGE \bfseries \Name} \\[4pt]
    \scriptsize
    \underline{\href{mailto:\Email}{\Email}} \,\textbar\, 
    \Phone \,\textbar\, 
    \underline{\href{\Linkedin}{linkedin.com/in/andrewobwocha}} \,\textbar\, 
    \underline{\href{\Github}{github.com/AndrewObwocha}}
\end{center}

% Education
\small
\ressection{Education}
\textbf{The University of Alberta}, Edmonton AB \hfill May 2028 \\
Bachelor of Science – Computer Science Honors \\
\textbf{GPA:} 4.00/4.00 \,\textbar\, \textbf{SAT:} 1540/1600
\vspace{-0.25em}

\begin{itemize}[leftmargin=2.3em, label={}, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item \textbf{Coursework:} Multivariable Calculus, Linear Algebra, Probability, Data Structures, Machine Learning, Algorithms
    \item \textbf{Honours/Awards:} Salutatorian (2/126), Doug Owram Scholar, Dean's List, 2x UKMT Challenge Silver
\end{itemize}


% Experience
\ressection{Experience}

\noindent \textbf{Kenya National Highways Authority}, Nairobi, KE \hfill June 2023 - August 2023 \\
Software Engineering Intern \,\textbar\, Python, Django
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Built Python/R pipelines on 50M+ shots to geocode 200K+ addresses, compress commute times, and engineer panel features
    \item Modeled how 10-min commute cuts reduce absence 1.8pp and lateness 1.6pp
\end{itemize}

% Projects
\ressection{Projects}

\noindent \textbf{Knowledge Graph} \,\textbar\, Java, Javascript, Springboot, D3js
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Built a graph-persistent web app to help researchers visualize and discover connections in complex information networks, replacing a cumbersome and inefficient list-based interface.
    \item Reduced data-fetching inefficiencies by re-architecting the backend from REST to a Spring Boot GraphQL API, reducing network round-trips by 5x.
\end{itemize}

\noindent \textbf{Tokenized Note System} \,\textbar\, Python, Javascript, Django, React
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Engineered a full-stack note management system to centralize academic resources, enabling users to perform full CRUD operations on private course notes.
    \item Reduced the user click workflow for compiling course-specific notes by over 60\% compared to a fragmented file system with immediate, centralized data access.
    \item Managed project development using Git for version control and GitHub for code hosting.
\end{itemize}

\noindent \textbf{House Forecaster} \,\textbar\, Java, Javascript, Springboot, D3js
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Developed a predictive ML pipeline using feature engineering to accurately forecast housing prices from raw data, achieving a cross-validated R² score of 0.78.
    \item Constructed a reproducible ML pipeline using Scikit-learn to process raw housing data, standardizing missing value imputation and categorical encoding to prevent data leakage during cross-validation.
\end{itemize}

% Leadership
\ressection{Leadership \& Community Involvement}

\noindent \textbf{Undergraduate AI Society} \,\textbar\, Vice President of External Affairs \hfill March 2025 - Present
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Developed a predictive ML pipeline using feature engineering to accurately forecast housing prices from raw data, achieving a cross-validated R² score of 0.78.
    \item Constructed a reproducible ML pipeline using Scikit-learn to process raw housing data, standardizing missing value imputation and categorical encoding to prevent data leakage during cross-validation.
\end{itemize}
    
\noindent \textbf{Univeristy of Alberta Innovation Fund} \,\textbar\, AI Analyst \hfill August 2025 - Present
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Developed a predictive ML pipeline using feature engineering to accurately forecast housing prices from raw data, achieving a cross-validated R² score of 0.78.
    \item Constructed a reproducible ML pipeline using Scikit-learn to process raw housing data, standardizing missing value imputation and categorical encoding to prevent data leakage during cross-validation.
\end{itemize}

% Skills
\ressection{Technical Skills}
\textbf{Languages \& Libraries:}  Python, JavaScript, SQL, HTML, CSS, React, Django, REST APIs, NumPy \\
\textbf{Tools \& Platforms:} Git, VSCode, Jupyter

\end{document}
"""

# ==============================================================================
# 2. HELPER FUNCTIONS
# ==============================================================================

def get_job_content(user_input):
    """Fetches Job Description via Jina (if URL) or returns raw text."""
    user_input = user_input.strip()
    
    if user_input.startswith("http"):
        print(f"\n[Job] Detected URL: {user_input}")
        print("[Job] Attempting to fetch via Jina Reader...")
        try:
            jina_url = f"https://r.jina.ai/{user_input}"
            response = requests.get(jina_url, timeout=10)
            
            content = response.text
            # Basic validation to ensure we didn't get a Login Page
            if response.status_code != 200 or "Sign in" in content or len(content) < 300:
                print(">>> WARNING: Link blocked (AuthWall). Falling back to manual entry.")
                return input("\nPASTE JOB DESCRIPTION HERE: ")
            
            print("[Job] Successfully fetched content!")
            return content
        except Exception:
            print(">>> Network Error. Falling back to manual entry.")
            return input("\nPASTE JOB DESCRIPTION HERE: ")
    else:
        return user_input

def fetch_readme(url):
    """Downloads raw README from GitHub."""
    path = url.replace("https://github.com/", "").strip("/")
    branches = ["main", "master"]
    
    for branch in branches:
        raw_url = f"https://raw.githubusercontent.com/{path}/{branch}/README.md"
        try:
            resp = requests.get(raw_url, timeout=5)
            if resp.status_code == 200:
                return resp.text
        except:
            continue
    return None

# ==============================================================================
# 3. MAIN EXECUTION FLOW
# ==============================================================================

if __name__ == "__main__":
    
    # --- STEP A: JOB STRATEGY ---
    job_input = input("Enter Job URL (or paste description): ")
    job_text = get_job_content(job_input)

    print("\n[Gemini] Analyzing Job Strategy...")
    strategy_prompt = f"""
    Analyze this job description. Return a concise summary of:
    1. EXPLICIT Keywords (Tech Stack, Tools).
    2. IMPLICIT Keywords (Qualities that are often associated with this role and technologies).
    3. The "Ideal Candidate Persona" in 1 sentence.

    JOB DESCRIPTION:
    {job_text[:15000]}
    """

    # FIX: Using Gemini Syntax
    strategy_response = model.generate_content(strategy_prompt)
    job_strategy = strategy_response.text
    print(f"\n--- TARGET STRATEGY ---\n{job_strategy}\n")

    # --- STEP B: PARALLEL RAG FETCHING ---
    print("[RAG] Fetching Project READMEs in parallel...")
    project_docs = {}

    # ThreadPoolExecutor makes the network requests Async/Parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_title = {
            executor.submit(fetch_readme, url): title 
            for title, url in PROJECT_REPO_MAP.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_title):
            title = future_to_title[future]
            try:
                data = future.result()
                if data:
                    print(f"  [+] Loaded: {title}")
                    project_docs[title] = data[:8000] # Truncate for token limits
                else:
                    print(f"  [-] No README found: {title}")
            except Exception as exc:
                print(f"  [!] Error {title}: {exc}")

    # --- STEP C: OPTIMIZATION LOGIC ---
    def rewrite_block(match):
        original_chunk = match.group(0)
        
        # FILTER: Skip Education
        if "Bachelor of Science" in original_chunk or "University of Alberta" in original_chunk:
            return original_chunk

        # CHECK RAG CONTEXT
        rag_context = ""
        for title, doc in project_docs.items():
            if title in original_chunk:
                rag_context = f"\nPROJECT README (Documentation):\n{doc}\n"
                break
                
        print(f"[Optimizing] {original_chunk.splitlines()[1][:30]}...")

        prompt = f"""
        You are an expert Resume Strategist.
        
        GOAL: Rewrite the bullet points (\item) of this LaTeX section to target the Job Strategy.
        
        INPUTS:
        1. TARGET STRATEGY: 
        {job_strategy}
        
        2. PROJECT CONTEXT (If available):
        {rag_context if rag_context else "No external docs. Use existing text."}
        
        3. ORIGINAL LATEX:
        {original_chunk}
        
        INSTRUCTIONS:
        - Rewrite the bullet points to demonstrate the Explicit and Implicit keywords from the Strategy.
        - If Project Context is provided, pull specific technical proofs (libraries, metrics) from it that match the Job.
        - If the original text looks like a duplicate/placeholder (e.g. repeated text in Leadership), INVENT new valid bullet points based on the Title/Role in the header.
        - STRICTLY PRESERVE all LaTeX tags (\noindent, \\textbf, \hfill, [leftmargin...]).
        - Do not output markdown fences (```). Return raw LaTeX only.
        """

        try:
            # FIX: Using Gemini Syntax
            response = model.generate_content(prompt)
            cleaned = response.text.strip()
            return cleaned.replace("```latex", "").replace("```", "")
        except Exception as e:
            print(f"Error optimizing block: {e}")
            return original_chunk

    # --- STEP D: EXECUTE REGEX ---
    regex_pattern = r"((?:\\noindent\s*)?\\textbf\{.*?\}.*?\\begin\{itemize\}.*?\\end\{itemize\})"
    
    print("\n[Gemini] Applying LaTeX Transformations...")
    final_latex = re.sub(regex_pattern, rewrite_block, LATEX_SOURCE, flags=re.DOTALL)

    output_filename = "tailored_resume.tex"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(final_latex)

    print(f"\nSUCCESS! Saved optimized resume to: {output_filename}")
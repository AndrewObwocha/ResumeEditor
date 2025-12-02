
import re
from config import settings
from config.templates import RESUME_LATEX

def optimize_resume(context, model):
    """
    context: dict containing 'job_strategy', 'readmes', 'job_text'
    model: Gemini model instance
    """
    print("\n[Resume Agent] Optimizing bullet points...")
    
    def rewrite_block(match):
        original_chunk = match.group(0)
        
        # 1. SKIP Check (Education, Headers, etc.)
        if any(keyword in original_chunk for keyword in settings.SKIP_KEYWORDS):
            return original_chunk

        # 2. RAG Context Injection
        rag_context = ""
        for title, doc in context['readmes'].items():
            if title in original_chunk:
                rag_context = f"\nPROJECT README (Documentation):\n{doc}\n"
                break
        
        # 3. Prompting
        prompt = f"""
        You are a Senior Software Engineering Resume Reviewer.
        
        GOAL: Optimize the LaTeX bullet points for a specific section to target a Job Strategy.
        
        INPUT DATA:
        1. TARGET JOB STRATEGY: 
        {context['job_strategy']}
        
        2. PROJECT DOCS (Truth Source):
        {rag_context if rag_context else "No external docs. Rely strictly on the Original Text."}
        
        3. ORIGINAL LATEX SECTION:
        {original_chunk}
        
        ---
        
        ### INSTRUCTION FRAMEWORK
        
        **1. THE STRUCTURAL FORMULA**
        Every bullet point must follow this logical flow (though you may vary the phrasing):
        `[Action Verb] + [Specific Technical Implementation (Libraries/Patterns)] + [Quantifiable Engineering Outcome]`
        - *Bad:* "Wrote code for the backend."
        - *Good:* "Refactored the monolithic backend into Microservices using Django, reducing deployment time by 40%."
        
        **2. METRIC DECISION TREE**
        - *If you have hard numbers:* Use them, but add context (e.g., don't say "30 users," say "scaled to 30k concurrent users").
        - *If you lack hard numbers:* Use **Relative Metrics** (e.g., "reduced latency by ~20%", "eliminated N+1 query bottlenecks").
        - *If purely qualitative:* Cite the **Standard** or **Mechanism** (e.g., "ensured 100% compliance with ISO 27001," "enforced strict CI/CD linting rules").
        
        **3. RELEVANCY & SKILLS**
        - Inject keywords from the **TARGET STRATEGY** naturally.
        - Ensure actions are grounded in reality (e.g., "Deployed via Docker," "Cached with Redis").
        - **Teamwork Check:** Ensure at least one bullet point implies collaboration (e.g., "Standardized API protocols for the frontend team," "Conducted code reviews").
        
        **4. VISUAL DENSITY**
        - Aim for "Full Line" density (approx. 20-35 words per bullet). 
        - Avoid short, weak points. Combine two weak points into one strong narrative if necessary.

        ---
        
        ### EXAMPLES 
        
        **Input:** "\item Built a web app using React."
        **Output:** "\item Architected a responsive Single Page Application using \textbf React and Redux, improving client-side state management and reducing page load times by 30\%."

        **Input:** "\item Fixed bugs in the database."
        **Output:** "\item Optimized SQL query performance by implementing composite indexes in \textbf PostgreSQL, cutting average query execution time from 500ms to 50ms."

        ---
        
        ### EXECUTION STEP
        
        Perform the rewrite. 
        - STRICTLY PRESERVE all LaTeX tags (\noindent, \\textbf, \hfill, [leftmargin...]).
        - DO NOT output the instructions or "meta-text" (like [Action]).
        - DO NOT invent facts not supported by the Input Data or plausible inference.
        
        Output format:
        :::THOUGHTS:::
        (Briefly explain your strategy: which keywords you included and why.)
        :::END_THOUGHTS:::
        
        :::LATEX:::
        (The valid LaTeX code)
        :::END_LATEX:::
        """

        try:
            response = model.generate_content(prompt)
            raw_text = response.text
            
            # 4. Parsing Logic
            # We extract the thoughts to print to console, and the latex to save to file.
            thoughts_match = re.search(r":::THOUGHTS:::(.*?):::END_THOUGHTS:::", raw_text, re.DOTALL)
            latex_match = re.search(r":::LATEX:::(.*?):::END_LATEX:::", raw_text, re.DOTALL)
            
            if thoughts_match:
                print(f"\n  [AI Reasoning] for section starting: '{original_chunk.splitlines()[1][:30]}...'")
                print(f"  {thoughts_match.group(1).strip()[:200]}...") # Print first 200 chars of thought
            
            if latex_match:
                cleaned_latex = latex_match.group(1).strip()
                # Double check: ensure no markdown fences lingered
                cleaned_latex = cleaned_latex.replace("```latex", "").replace("```", "")
                return cleaned_latex
            else:
                # Fallback: If AI messed up format, try to return raw or original
                print("  [!] Warning: AI didn't follow output format. Returning raw cleanup.")
                return raw_text.replace("```latex", "").replace("```", "").strip()

        except Exception as e:
            print(f"    [!] Error optimizing block: {e}")
            return original_chunk

    # Execute Regex Replacement
    regex_pattern = r"((?:\\noindent\s*)?\\textbf\{.*?\}.*?\\begin\{itemize\}.*?\\end\{itemize\})"
    
    # Note: We run this on the RESUME_LATEX imported from templates
    final_latex = re.sub(regex_pattern, rewrite_block, RESUME_LATEX, flags=re.DOTALL)
    return final_latex
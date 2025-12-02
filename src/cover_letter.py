from config.templates import COVER_LETTER_LATEX

def write_cover_letter(context, model, meta_data):
    """
    context: dict containing 'job_strategy', 'readmes', 'job_text'
    model: Gemini model instance
    meta_data: dict containing 'company', 'role', 'address' (Passed from main.py)
    """
    print("\n[Cover Letter Agent] Drafting narrative...")

    # 1. Prepare Context
    all_projects_context = "\n".join([f"PROJECT: {k}\nDETAILS: {v[:1500]}" for k,v in context['readmes'].items()])

    # 3. Generate Body Content
    print("  [AI] Writing Body Content...")
    body_prompt = f"""
    You are an expert Copywriter. Write the BODY CONTENT for a cover letter.

    GOAL: Write a cover letter in 300 words with my authentic voice as a University of Alberta student for the associated job.

    
    INPUTS:
    1. JOB DESCRIPTION: {context['job_text'][:5000]}
    2. STRATEGY: {context['job_strategy']}
    3. COMPANY: {meta_data.get('company')}
    4. MY PROJECTS: 
    {all_projects_context}
    
    INSTRUCTIONS:
    - This cover letter is for the associated job.
    - The candidate (me) is a second-year Computer Science student at the University of Alberta who is eager to learn from professionals and contribute to the industry.
            With this in mind, any writing done should emphasise my authentic voice to reflect my student mindset and eagerness.
    - The overarching result of the cover letter is to convince the recruiter of my technical curiosity in the field relevant to the role, my problem-solving initiative relevant to the role and cultural fit with the company.
            To achieve this, I need to research the scope and attributes of this role. Find information relevant to my needs and provide me with context/perspective as to what you could find, if anything, on the role and company before proceeding. 
    - The audience/reader is likely the company's non-technical recruitment team that values effective communication of value that allows them to understand my technical aptitude. 
            With this in mind, dont target buzzwords but an elegant intersection between technical showcasing but lay enough for the non-technical to understand. 
            Any writing done should maintain the idea of this audience.
    - When writing the hook, the main principle to follow is that if I were to apply to a different job using this same hook, would it still make sense? If so, its not tailored and needs editing. 
            The main spirit of this section is to capture attention with the research I have done and build genuine connection to myself. 
            Therefore, I need to show them that I not only know what to emphasise, but why I need to emphasise it to connect to the role and them. 
            If you do not have enough information on the role, err on the side of caution and provide a broadly acceptable hook such as state excitement for {meta_data.get('company')} and the {meta_data.get('role')} role.
    - For subsequent points, there are a few principles to adhere to beyond the natural authentic voice and connection to MY PROJECTS (which should be explicitly mentioned to prove I have the skills in the Strategy)
            - Firstly, they serve as a body of work for the research I have done. The main selling point is the company knowledge I can display, so each paragraph begins with a nugget of information (I can potentially influence as an intern) about the company. 
                The following explanation is about how the 3 pillars: Technical Curiosity, Problem Solving, and Cultural Fit can provide value to that nugget of company information.
            - Secondly, the more granular and specific I can go, the better. To achieve this, I need to understand specifically the context of that company information. 
                In this context, my explanations need to be ultra-granular. A good filter is that the value must be something tangible and realistically interactable with, whether it's physical, digital or conceptual. 
                If I cant interact with it, it is not granular enough. Keep in mind, value can be interpreted at multiple levels of granularity/abstraction. I am not interested in high-level, superficial, abstract value; I want the granular, nitty-gritty value. 
                Virtually, think of this as official documentation rather than a brief overview.
            - Thirdly, the language needs to sound natural and authentic but graceful, professionala and purposeful.
            - Fourthly, the length is preferably concise while still remaining impactful. This is flexible and dependent on the context, but in general, concision is valued.
    - FORMAT: Return ONLY the LaTeX text for the paragraphs. Use \\ (double backslash) for paragraph breaks. Do NOT include headers or \begin{{document}}.
    """

    body_response = model.generate_content(body_prompt)
    body_content = body_response.text.replace("```latex", "").replace("```", "").strip()

    # 3. Inject into Template
    final_cl = COVER_LETTER_LATEX.replace("%BODY_CONTENT%", body_content)
    final_cl = final_cl.replace("%COMPANY_NAME%", meta_data.get('company', "Hiring Manager"))
    final_cl = final_cl.replace("%JOB_TITLE%", meta_data.get('role', "Software Engineer"))
    final_cl = final_cl.replace("%COMPANY_ADDRESS%", meta_data.get('address', ""))
    
    return final_cl
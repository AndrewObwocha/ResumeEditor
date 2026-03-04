"""
Prompt templates for AI-powered resume and cover letter generation.
All prompts use placeholders that should be formatted with actual data.
"""

APPLICATION_STRATEGY_PROMPT = """
Analyze this job description and create a comprehensive application strategy.

Job Description:
{job_description}

Your task:
1. Identify the key technical skills required
2. Highlight important soft skills and cultural values
3. Note any specific requirements or preferences
4. Suggest which skills and experiences should be emphasized
5. Recommend the tone and approach for the application

Provide a detailed strategy that can guide resume optimization and cover letter writing.
"""

JOB_METADATA_EXTRACTION_PROMPT = """
Extract the following details from the Job Description as JSON:
{{
    "company": "Name of Company (e.g. Google)",
    "role": "Job Title (e.g. Software Engineer)",
    "address": "Street Address or City, State (if found, else leave empty)"
}}

Job Description:
{job_description}
"""

RESUME_OPTIMIZER_PROMPT = """
You are a Senior Software Engineering Resume Reviewer.

GOAL: Optimize the LaTeX bullet points for a specific section to target a Job Strategy.

INPUT DATA:
1. TARGET JOB STRATEGY: 
{job_strategy}

2. PROJECT DOCS (Truth Source):
{rag_context}

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

**Input:** "\\item Built a web app using React."
**Output:** "\\item Architected a responsive Single Page Application using \\textbf{{React}} and Redux, improving client-side state management and reducing page load times by 30\\%."

**Input:** "\\item Fixed bugs in the database."
**Output:** "\\item Optimized SQL query performance by implementing composite indexes in \\textbf{{PostgreSQL}}, cutting average query execution time from 500ms to 50ms."

---

### EXECUTION STEP

Perform the rewrite. 
- STRICTLY PRESERVE all LaTeX tags (\\noindent, \\textbf, \\hfill, [leftmargin...]).
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

COVER_LETTER_PROMPT = """
You are a professional cover letter writer specializing in software engineering positions.

Write a compelling cover letter based on the following information:

1. JOB STRATEGY:
{job_strategy}

2. COMPANY & ROLE:
Company: {company}
Role: {role}
Address: {address}

3. PROJECT CONTEXT (for demonstrating relevant experience):
{rag_context}

4. JOB DESCRIPTION EXCERPT:
{job_description_excerpt}

---

### INSTRUCTIONS:

1. **Opening Paragraph**: Express genuine enthusiasm for the specific role and company. Mention something specific about the company that resonates.

2. **Body Paragraphs**: 
   - Highlight 2-3 relevant experiences from the project context that align with the job strategy
   - Use specific technical details and quantifiable achievements
   - Connect your experiences directly to the role's requirements
   - Show understanding of the company's challenges/goals

3. **Closing Paragraph**: Reiterate interest, suggest next steps, and thank them for consideration.

4. **Tone**: Professional yet personable, confident but not arrogant.

5. **Format**: Output as LaTeX using the cover letter template structure provided.

Output the complete LaTeX cover letter code ready to compile.
"""

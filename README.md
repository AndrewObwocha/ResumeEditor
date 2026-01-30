# Resume Editor: AI-Powered LaTeX Resume and Cover Letter Generator

## Automatically tailor your application to any job description.

This project is a command-line application that leverages the Google Gemini Pro API to generate customized LaTeX resumes and cover letters. The tool takes a job description as input, analyzes it to create a strategic plan, and then rewrites a master resume template to align with the specific role. It uses local project README files as a knowledge base (RAG) to ensure technical details are accurate.

-   **AI-Powered Resume Optimization:** Rewrites resume bullet points to match keywords and requirements from the job description.
-   **Dynamic Cover Letter Generation:** Creates a personalized and authentic cover letter based on the job and your project experience.
-   **RAG for Technical Accuracy:** Uses your own project documentation (READMEs) as a source of truth to ground the AI's output in reality.
-   **Web Scraper Integration:** Automatically fetches job descriptions from URLs using the Jina Reader API.
-   **LaTeX Output:** Generates professional, ready-to-compile `.tex` files for both your resume and cover letter.

## How to install and run this project

No complex setup is required. Ensure you have Python installed and an environment set up.

```bash
# Clone the repository
git clone https://github.com/{yourUsername}/ResumeEditor.git
cd ResumeEditor

# Install dependencies
pip install -r requirements.txt

# Set up your API key
# Create a .env file in the root directory and add your Gemini API key:
# GEMINI_API_KEY=your_api_key_here

# Run the application
python main.py
```

## How to tweak this project for your own use cases

This tool is designed to be customized. To adapt it for your own profile, you should:
1.  Modify the `config/templates.py` file to change the base LaTeX templates for your resume and cover letter.
2.  Add your own project `README.md` files to a relevant directory that the tool can access to use as context.
3.  Adjust the prompts in `src/resume.py` and `src/cover_letter.py` to change the tone, style, or logic of the AI agents.

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the "Issues" tab above. If you would like to submit a PR with a fix, please reference the issue you created.

## License

This project is licensed under the MIT License.

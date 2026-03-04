# ResumeEditor: AI-Powered Application Material Generator

## Generate tailored resumes and cover letters in seconds using AI and your project experience.

ResumeEditor is a Python CLI application leveraging Google Gemini API for intelligent content generation with async event-driven architecture. It fetches job descriptions via Jina Reader, analyzes requirements, and generates customized LaTeX resumes and cover letters. The system uses GitHub README files as a RAG knowledge base to ground outputs in real project experience, ensuring technical accuracy.

- **AI-Powered Resume Optimization**: Intelligently rewrites bullet points to match job keywords and requirements
- **Personalized Cover Letters**: Creates authentic letters based on job requirements and your project portfolio
- **RAG-Enhanced Accuracy**: Leverages your project documentation as source-of-truth context
- **One-Click Generation**: Fetch job descriptions from URLs or paste manually in seconds
- **Professional LaTeX Output**: Ready-to-compile `.tex` files for polished applications
- **Async Performance**: Concurrent operations for fast processing of large job descriptions

## How to install and run ResumeEditor

Getting started is simple—no complex setup required.

**Prerequisites**: Python 3.10+ and a free Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

```bash
git clone https://github.com/AndrewObwocha/ResumeEditor.git
cd ResumeEditor

make setup

echo "GEMINI_API_KEY=your_api_key_here" > .env

make run
```

That's it! Follow the prompts to paste a job description or enter a job posting URL. The app will generate your customized resume and cover letter in the `output/` folder.

## How to customize and extend ResumeEditor

Since this project follows a modular event-driven architecture, extending it is straightforward.

**Key files to explore:**

- `src/config.py` - Update `PROJECT_REPO_MAP` with your GitHub repositories
- `src/templates/templates.py` - Customize personal information and LaTeX formatting
- `src/prompts.py` - Adjust AI tone and strategy for generating content

**For developers:**

```bash
pip install -r requirements.txt

make test

make run
```

The codebase uses async/await throughout with clear separation of concerns via the event bus pattern. See `src/events/events.py` for the event definitions and `src/infra/event_bus.py` for the pub/sub system. Each stage (resume optimization, cover letter generation, etc.) is a separate handler that listens for events and publishes new ones—making it easy to add new features.

## Contributing

We welcome contributions! Here's how to help:

1. **Report issues**: Found a bug? Open an issue with reproduction steps and system info
2. **Submit improvements**: Fork the repo, create a feature branch, and open a PR
3. **Code guidelines**: Ensure all tests pass (`make test`) before submitting a PR
4. **Documentation**: Help improve README, docstrings, or add examples

When submitting a PR, please:

- Create a descriptive title and reference any related issues
- Include tests for new functionality
- Run `make test` to validate your changes
- Keep commits atomic and well-messaged

## License

This project is licensed under the MIT License.

---

_Happy job hunting!_

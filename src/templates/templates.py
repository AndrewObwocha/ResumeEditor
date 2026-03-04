RESUME_LATEX = r"""
\documentclass[10pt]{extarticle}
\usepackage[margin=0.5in]{geometry}
\usepackage{enumitem}
\usepackage[colorlinks=true, urlcolor=black]{hyperref}
\usepackage{titlesec}
\usepackage[T1]{fontenc}     
\usepackage{newtxtext}
\usepackage{anyfontsize}

\pagestyle{empty}

\linespread{0.95} 

% Variables
\newcommand{\Name}{Andrew Obwocha}
\newcommand{\City}{Edmonton, AB}
\newcommand{\Email}{aobwocha@ualberta.ca}
\newcommand{\Phone}{(780)-717-0986}
\newcommand{\Github}{https://github.com/AndrewObwocha}
\newcommand{\Linkedin}{https://linkedin.com/in/andrewobwocha}

% Section Formatting
\newcommand{\ressection}[1]{%
  \vspace{0.6em}
  \noindent{\fontsize{11pt}{15.6pt}\selectfont\bfseries\MakeUppercase{#1}}\\[-8pt] 
  \hrule height 1.35pt
  \vspace{0.6em}
}

% Usage: \resumeEducation{University}{Faculty}{Graduation Date}
        % {Bachelor}{GPA}
\newcommand{\resumeEducation}[5]{
  \noindent \textbf{#1}, #2 \hfill \textbf{#3} \\
  #4 \hfill #5 \\
}

% Usage: \resumeExperience{Title}{Company}{Location}{Date}
\newcommand{\resumeExperience}[4]{
  \noindent \textbf{#1}, #2 - \textbf{#3} \hfill \textbf{#4}
}

% Usage: \resumeProject{Title}{Company/Location}{Date}
\newcommand{\resumeProject}[3]{
  \noindent \textbf{#1}, #2 \hfill \textbf{#3}
  
}

\begin{document}
\fontsize{11pt}{12.6pt}\selectfont 

% Header
\begin{center}
    {\LARGE \bfseries \Name} \\[4pt]
    \small
    \City \ | \ 
    \href{mailto:\Email}{\Email} \ | \ 
    \Phone \ | \ 
    \href{\Linkedin}{linkedin.com/in/andrewobwocha} \ | \ 
    \href{\Github}{github.com/AndrewObwocha}
\end{center}

% Education
\ressection{Education}

\resumeEducation{University of Alberta}{Faculty of Science}{Expected June 2028}{Bachelor of Science in Computer Science; Minor in Economics}{Cumulative GPA: 4.00/4.00}
\textit{Relevant Coursework: Programming Methodology, Databases, Algorithms, Data Structures, Discrete Math, Calculus}



% Experience
\ressection{Experience}

\resumeExperience{Software Engineering Intern}{Kenya National Highways Authority}{Nairobi, KE}{Jun 2024 - Aug 2024}
\begin{itemize}[leftmargin=1.5em, noitemsep, topsep=0pt]
    \item Eliminated 100+ silent request failures by enforcing geolocation boundaries in the Django serializer to return appropriate HTTP 500 error responses for invalid user coordinates.
    \item Engineered an automated resource-monitoring daemon in Python using psutil, logging memory-leak events (80\%+ RAM usage) to improve workstation reliability.
    \item Collaborated in an Agile team environment, utilizing Git/GitHub for version control and participating in peer code reviews.
    \item Authored unit tests for the Django serializer and utilized Docker for local development and deployment.
\end{itemize}

% Projects
\ressection{Projects}

\resumeProject{\href{https://github.com/AndrewObwocha/ResumeEditor}{AI-Powered LaTeX Career Generator}}{Edmonton, AB}{Sep 2025 - Jan 2026}
\begin{itemize}[leftmargin=1.5em, noitemsep, topsep=0pt]
    \item Architected a FastAPI backend service in Python that generates a LaTeX resume script tailored to a job description.
    \item Implemented a queue to handle high-latency service dependencies, including API calls to GitHub and the Gemini LLM. 
    \item Integrated user-selected GitHub projects as LLM context by parsing README files from provided repository links.
    \item Achieved 70\% test coverage in Pytest across project environment by developing a suite of unit and integration tests.
\end{itemize}

\vspace{5pt}

\resumeProject{\href{https://github.com/AndrewObwocha/GraphMind}{Knowledge Graph Data API}}{Edmonton, AB}{Jun 2025 - Aug 2025}
\begin{itemize}[leftmargin=1.5em, noitemsep, topsep=0pt]
    \item Engineered a Spring Boot API microservice in Java to service a graph application through PostgreSQL queries to a relational database, providing node and relationship objects required to build a knowledge graph structure.
    \item Enforced session security using JSON Web Tokens (JWT) with 30-minute automatic refreshes to avoid repetitive logins.
    \item Implemented a GraphQL schema to avoid repetitive backend refactors of a rigid REST API from conflicting client needs.
\end{itemize}

\vspace{5pt}

\resumeProject{\href{https://github.com/AndrewObwocha/UniNotes}{UniDoc API}}{Edmonton, AB}{Mar 2025 - May 2025}
\begin{itemize}[leftmargin=1.5em, noitemsep, topsep=0pt]
    \item Designed a Python Django RESTful API endpoint to service a course management application through SQLite queries to a relational database, providing proprietary course data.
    \item Implemented a hierarchical design to eliminate redundant validation during GET requests, reducing latency by 60\%.
\end{itemize}

\vspace{5pt}

\resumeProject{\href{https://github.com/AndrewObwocha/amazon-price-analyzer}{Amazon Price Statistics Extension}}{Edmonton, AB}{Nov 2025 - Dec 2025}
\begin{itemize}[leftmargin=1.5em, noitemsep, topsep=0pt]
    \item Developed a Chrome extension in Javascript that provides real-time statistical price analysis (quartiles, mean, std. deviation) across Amazon search results using client-side DOM parsing.
\end{itemize}

% Leadership
\ressection{Leadership \& Community Involvement}

\resumeExperience{Vice President of External Affairs}{Undergraduate AI Society (800 members)}{Edmonton, AB}{Mar 2025 - Present}
\begin{itemize}[leftmargin=1.5em, noitemsep, topsep=0pt]
    \item Hosted 12 interviews with professional Software Engineers discussing AI's impact on the software development life cycle (SDLC), reaching 1000 students and addressing career anxiety in the club community.
    \item Organized R\&D career panel of 4 research academics (Prof/PhD/Masters/Undergraduate) to clarify the early steps to starting reputable CS research, gathering 100+ undergraduate attendees.
\end{itemize}

% Skills
\ressection{Technical Skills}
\noindent \textbf{Languages:} Python, C, Java, SQL, JavaScript, LaTeX, Bash \\
\textbf{Frameworks:} Django, SpringBoot, Gradle, RESTful APIs, GraphQL, Pytest, React \\
\textbf{Tools:} Git, GitHub, Linux, PostgreSQL, Docker, VSCode

\end{document}
"""

COVER_LETTER = COVER_LETTER_LATEX = r"""
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

\today \\

\textbf{Hiring Manager} \\
%COMPANY_NAME% \\
%COMPANY_ADDRESS%

\vspace{0.5cm}

\textbf{RE: Application for %JOB_TITLE%}

\vspace{0.5cm}

%BODY_CONTENT%

\vspace{1cm}
Sincerely, \\
\\
Andrew Obwocha

\end{document}
"""
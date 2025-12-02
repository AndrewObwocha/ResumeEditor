RESUME_LATEX = r"""
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
    \item \textbf{Honours/Awards:}
    
    \vspace{-0.25em}

    \begin{itemize}[leftmargin=2.3em, label={}, itemsep=0pt, topsep=0pt, parsep=0pt]
        \item \textbf{Dean's List:} Currently inducted into the Dean's list at the Unviersity of Alberta for high performance
        \item \textbf{Regional Excellence Scholar:} Recipient of CAD\$ 10,000 merit scholarship for East African Region
        \item \textbf{UKMT Challenge Medalist:} 2x Silver medalist for Global British Mathematics Challenge in the Senior Division
        \item \textbf{Valedictorian (1/256):} Recognized as highest performer in British A-Level Class of 2024 in Brookhouse School
    \end{itemize}
\end{itemize}


% Projects
\ressection{Projects}

\noindent \textbf{Knowledge Graph} \,\textbar\, Java, Javascript, Springboot, D3js
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Developed a graph-persistent web application using \textbf{React} and \textbf{D3.js} to empower researchers visualize and discover connections in information networks, improving on a cumbersome list-based interface
    \item Refactored the backend from REST to \textbf{Springboot GraphQL}, resulting in a \textbf{5x reduction} in network trips.
\end{itemize}

\noindent \textbf{Tokenized Note System} \,\textbar\, Python, Javascript, Django, React
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Engineered a full-stack note system with \textbf{React} and \textbf{Django}, enabling \textbf{CRUD} operations on private material.
    \item Reduced the user-click workflow for compiling notes by over 60\%, using \textbf{REST APIs} for centralized data access.
\end{itemize}

\noindent \textbf{House Forecaster} \,\textbar\, Java, Javascript, Springboot, D3js
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Engineered an ML pipeline using \textbf{Scikit-learn} in \textbf{Python}, incorporating data preprocessing, exploratory data analysis, and feature engineering to forecast housing prices in Manhattan, achieving an R² score of 0.78.
    \item Engineered 2 novel features (HouseAge, NeighbourhoodSafety) that imprvoed R² score by 5 percentage points 
\end{itemize}

% Experience
\ressection{Experience}

\noindent \textbf{Kenya National Highways Authority}, Nairobi, KE \hfill June 2023 - August 2023 \\
Software Engineering Intern \,\textbar\, Python, Django
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Implemented custom model validation using GeoDjango, eliminating 50+ monthly erroneous data points.
    \item Automated system health checks with Python, achieving greater than 99\% uptime during 5-day financial closing.
\end{itemize}

% Leadership
\ressection{Leadership \& Community Involvement}

\noindent \textbf{Undergraduate AI Society} \,\textbar\, Vice President of External Affairs \hfill March 2025 - Present
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Drove the 'Career Highlights' series, distilling complex career advice from senior leaders into actionable roadmaps for 100+ students, bridging the industry-academia gap and platforming students to network with professionals.
    \item Recruited a diverse panel (PhD, MSc, Prof) for comparative look at academic vs. industry R\&D, demystifying graduate pathways for undergraduates, with over 75 students in attendance for the moderated session.
\end{itemize}
    
\noindent \textbf{Univeristy of Alberta Innovation Fund} \,\textbar\, AI Analyst \hfill August 2025 - Present
\begin{itemize}[leftmargin=5em, itemsep=0pt, topsep=0pt, parsep=0pt]
    \item Applied risk assessment frameworks to evaluate the architectural designs of 2 AI startups, informing investors.
    \item Spearheaded standardization of assessment protocols by training a 5-person team on startup declarative analysis.
\end{itemize}

% Skills
\ressection{Technical Skills}
\textbf{Languages \& Libraries:}  Python, JavaScript, SQL, HTML, CSS, React, Django, REST APIs, NumPy \\
\textbf{Tools \& Platforms:} Git, VSCode, Jupyter

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
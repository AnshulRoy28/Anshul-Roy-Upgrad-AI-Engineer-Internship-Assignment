# Quick Start Guide

Get up and running with the AI Mock Interview Coach in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Google API Key (get one at https://aistudio.google.com/app/apikey)

## Installation

### 1. Clone or Download

```bash
cd interview-coach
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

Create a `.env` file in the project root:

```bash
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

Replace `your_google_api_key_here` with your actual Google API key.

## Running the Application

### Option 1: One-Click Start (Easiest)

**Linux/Mac:**
```bash
./start_interview_app.sh
```

**Windows:**
```bash
start_interview_app.bat
```

This will:
- Start the API server on port 8000
- Start the frontend on port 3000
- Open two terminal windows

### Option 2: Manual Start

**Terminal 1 - API Server:**
```bash
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd Frontend
python -m http.server 3000
```

## Using the Application

1. **Open Your Browser**
   - Navigate to `http://localhost:3000/index.html`
   - Click "Start Practicing"

2. **Enter API Key (if not in .env)**
   - Find the "API Key" field in the top navigation
   - Paste your Google API key

3. **Prepare Your Materials**
   - **Resume**: LaTeX format (see `examples/sample_resume.tex`)
   - **Job Description**: Plain text (see `examples/sample_job_description.txt`)

4. **Start Interview**
   - Paste your resume in the first text area
   - Paste the job description in the second text area
   - Choose focus area (behavioral/technical/case/mixed)
   - Click "Start Interview"

5. **Answer Questions**
   - Read each question carefully
   - Use the STAR format (Situation, Task, Action, Result)
   - Be specific with metrics and examples
   - Click "Submit Answer" after each response

6. **Review Feedback**
   - Get real-time scores on 5 dimensions:
     - Completeness
     - Depth
     - Structure
     - Relevance
     - Confidence
   - See outcome prediction after 3 questions
   - Get comprehensive coaching report at the end

## Example Resume (LaTeX)

```latex
\documentclass{article}
\begin{document}

\name{John Doe}

\section{Contact}
\email{john.doe@email.com}
\phone{(555) 123-4567}
\linkedin{linkedin.com/in/johndoe}
\github{github.com/johndoe}

\section{Education}
Bachelor of Science in Computer Science
University of Example, 2020-2024
GPA: 3.8/4.0

\section{Experience}
Software Engineer Intern
Tech Company, Summer 2023
\begin{itemize}
\item Built scalable microservices handling 1M+ requests/day
\item Reduced API latency by 40% through caching optimization
\item Implemented CI/CD pipeline reducing deployment time by 60%
\end{itemize}

\section{Skills}
Python, Java, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL, MongoDB

\section{Projects}
E-commerce Platform
\begin{itemize}
\item Built full-stack web application with React and Node.js
\item Implemented payment processing with Stripe API
\item Deployed on AWS with auto-scaling
\end{itemize}

\end{document}
```

## Example Job Description

```
Senior Software Engineer

Company: Tech Innovations Inc.
Location: San Francisco, CA (Remote)

About the Role:
We're looking for a Senior Software Engineer to join our platform team.

Requirements:
- 5+ years of software development experience
- Strong proficiency in Python and Java
- Experience with cloud platforms (AWS/GCP/Azure)
- Excellent problem-solving skills
- Strong communication and collaboration abilities

Responsibilities:
- Design and implement scalable distributed systems
- Lead technical discussions and architecture decisions
- Mentor junior engineers
- Collaborate with cross-functional teams
- Write clean, maintainable, well-tested code

Nice to Have:
- Experience with Kubernetes and Docker
- Knowledge of microservices architecture
- Contributions to open-source projects
- Experience with CI/CD pipelines
```

## Tips for Best Results

### Resume Tips
- Use standard LaTeX sections: `\section{Education}`, `\section{Experience}`, etc.
- Include specific metrics and numbers
- List concrete technologies and tools
- Keep it concise and relevant

### Interview Tips
- **Use STAR Format**:
  - **S**ituation: Set the context
  - **T**ask: Describe the challenge
  - **A**ction: Explain what you did
  - **R**esult: Share the outcome with metrics

- **Be Specific**: Use numbers, percentages, and concrete examples
- **Stay Concise**: Aim for 90-120 seconds per answer
- **Relate to Job**: Connect your experience to the job requirements
- **Show Impact**: Emphasize the results and business value

## Troubleshooting

### "API_KEY_MISSING" Error
- Make sure you created the `.env` file
- Check that the API key is correct
- Or enter it manually in the UI

### "Port Already in Use" Error
- Change the port in `api_server.py` (line at the bottom)
- Update the frontend base URL to match

### CORS Errors
- Make sure `flask-cors` is installed: `pip install flask-cors`
- Restart the API server

### Resume Not Parsing
- Check LaTeX syntax
- Use standard section names
- See example resume above

### Slow Responses
- Normal: 3-7 seconds per question
- The system uses multiple AI agents with tools
- First question may take 5-10 seconds (includes profiling)

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for API details
- See [frontend-api-spec.json](frontend-api-spec.json) for complete API spec
- Try the demo: `python demo.py`

## Support

If you encounter issues:
1. Check the console logs (browser and server)
2. Review the troubleshooting section above
3. See example files in `examples/` directory
4. Check the API specification

## Stopping the Application

### If using startup script:
- Press `Ctrl+C` in the terminal (Linux/Mac)
- Close the command windows (Windows)

### If running manually:
- Press `Ctrl+C` in each terminal window

---

**Enjoy your interview practice!** 🎯

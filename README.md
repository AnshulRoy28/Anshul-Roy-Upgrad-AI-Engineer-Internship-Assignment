# AI Mock Interview Coach

An intelligent mock interview system powered by Google's Agent Development Kit (ADK) and Gemini API. Features adaptive difficulty, real-time evaluation, outcome prediction, and personalized coaching.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd upgrad-take-home
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Run the Application

**Option 1: Quick Start (Recommended)**
```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

**Option 2: Manual Start**
```bash
# Terminal 1 - API Server
python api_server.py

# Terminal 2 - Frontend
cd Frontend && python -m http.server 5500
```

Then open: **http://localhost:5500/interview.html**

## ✨ Features

### Core Capabilities
- 🧠 **Multi-Agent Architecture** - Specialized agents for profiling, interviewing, evaluating, and coaching
- 🎯 **Adaptive Difficulty** - Adjusts question difficulty based on performance
- 📊 **Real-Time Evaluation** - Instant feedback on answer quality
- 🔮 **Outcome Prediction** - Early prediction of interview success
- 📈 **Pattern Detection** - Identifies strengths and weaknesses
- 🎓 **Personalized Coaching** - Custom 2-week practice plans

### Technical Features
- ✅ **Input Validation** - Length limits and sanitization
- ✅ **Auto-Retry Logic** - Handles network errors gracefully
- ✅ **Draft Auto-Save** - Never lose your work
- ✅ **Health Monitoring** - Real-time connection status
- ✅ **Session Management** - 24-hour session expiration
- ✅ **Comprehensive Logging** - Full audit trail

## 📁 Project Structure

```
├── api_server.py           # REST API backend
├── main.py                 # CLI interface
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── .env                    # API key (create this)
├── start.sh / start.bat    # Quick start scripts
├── test_api.py             # API test suite
│
├── adk_agents/             # ADK-based agents
│   ├── orchestrator.py     # Main orchestrator
│   ├── profiler_agent.py   # Strategy creation
│   ├── interviewer_agent.py # Question generation
│   ├── evaluator_agent.py  # Answer evaluation
│   └── coach_agent.py      # Coaching reports
│
├── Frontend/               # Modern web UI
│   ├── interview.html      # Main application
│   ├── app.js             # Frontend logic
│   └── styles.css         # Styling
│
├── prompts/               # Agent prompts
├── state/                 # State management
├── tools/                 # Agent tools
├── utils/                 # Utilities
├── examples/              # Sample data
└── docs/                  # Documentation
```

## 🧪 Testing

### Run API Tests
```bash
python test_api.py
```

### Manual Testing
1. Start the servers (see Quick Start)
2. Open http://localhost:5500/interview.html
3. Enter your API key
4. Paste sample resume from `examples/sample_resume.tex`
5. Paste sample job from `examples/sample_job_description.txt`
6. Start interview and test features

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Detailed integration instructions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[docs/](docs/)** - Additional documentation
  - Testing guides
  - Enhancement summaries
  - Integration status
  - Quick reference

## 🎯 Usage

### Web Interface (Recommended)
1. Open http://localhost:5500/interview.html
2. Enter your Google API key
3. Paste your resume (LaTeX format)
4. Paste the job description
5. Configure settings (focus area, adaptive strategy, etc.)
6. Start interview and answer questions
7. Receive personalized coaching report

### CLI Interface
```bash
python main.py
```
Follow the prompts to complete the interview.

## 🔧 Configuration

Edit `.env` file:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Edit `config.py` for advanced settings:
- `MAX_INTERVIEW_TURNS` - Number of interview questions (default: 7)
- `MODEL` - Gemini model to use (default: gemini-2.5-flash)

## 🛠️ Development

### Project Architecture
- **Backend**: Flask REST API with ADK agents
- **Frontend**: Vanilla JavaScript with modern UI
- **Agents**: Google ADK pattern-based multi-agent system
- **State**: Centralized state management
- **Tools**: Agent-specific tools and utilities

### Key Components
1. **ProfilerAgent** - Analyzes candidate and creates interview strategy
2. **InterviewerAgent** - Generates contextual questions
3. **EvaluatorAgent** - Scores answers and detects patterns
4. **CoachAgent** - Provides personalized feedback and practice plans
5. **Orchestrator** - Coordinates all agents and manages workflow

## 🚨 Troubleshooting

### API Server Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Check API key
cat .env
```

### Frontend Can't Connect
- Verify API server is running: `curl http://localhost:8000/api/v1/health`
- Check browser console (F12) for errors
- Ensure CORS is enabled (it should be by default)

### Session Expired
- Sessions expire after 24 hours
- Start a new interview
- For production, implement Redis storage

## 📊 Performance

- Health check: < 100ms
- Resume parsing: < 1s
- Job parsing: < 1s
- Interview initialization: 5-10s
- Question generation: 3-7s
- Answer evaluation: 3-5s
- Report generation: 5-10s

## 🔒 Security

- ✅ Input validation and length limits
- ✅ XSS protection via sanitization
- ✅ Session expiration (24 hours)
- ✅ No sensitive data in error messages
- ✅ API key not logged

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [Google ADK](https://github.com/google/adk)
- Powered by [Gemini API](https://ai.google.dev/)
- UI inspired by modern design patterns

## 📧 Support

For issues or questions:
1. Check the [documentation](docs/)
2. Review [TROUBLESHOOTING](docs/TESTING_GUIDE.md#troubleshooting)
3. Open an issue on GitHub

---

**Made with ❤️ using Google ADK and Gemini API**

A multi-agent system powered by Google's ADK (Agent Development Kit) that conducts realistic mock interviews and provides structured feedback.

## ✨ New: Modern Frontend Included!

This project now includes a beautiful, modern frontend with:
- 🎨 Dark theme with glassmorphism design
- 📊 Real-time scoring visualization
- 📱 Responsive layout
- ⚡ No build step required
- 🚀 One-click startup

**[Quick Start Guide →](QUICKSTART.md)**

## Features

- **🌐 Web Interface** - Upload resume (LaTeX) and job description for personalized interviews
- **🧠 Agentic AI** - Autonomous agents with memory, tools, and learning capabilities
- **🔄 Adaptive Strategy** - Adjusts difficulty based on your performance
- **🔮 Outcome Prediction** - Early prediction of interview results
- **📊 Pattern Detection** - Identifies your answering patterns
- **🎯 Personalized Coaching** - Custom 2-week practice plans

## Quick Start

### Option 1: New Modern Frontend (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Start API server
python api_server.py

# In another terminal, serve frontend
cd Frontend
python -m http.server 3000

# Open http://localhost:3000/index.html
```

### Option 2: Streamlit UI (Legacy)

```bash
# Install
pip install -r requirements.txt

# Set up API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run web UI
streamlit run app.py
```

### Option 3: CLI

```bash
python main.py
```

## Usage

### Modern Frontend (Recommended)

1. **Start the Application**
   ```bash
   # Linux/Mac
   chmod +x start_interview_app.sh
   ./start_interview_app.sh
   
   # Windows
   start_interview_app.bat
   ```

2. **Open the App**
   - Navigate to `http://localhost:3000/index.html`
   - Click "Start Practicing"

3. **Enter API Key**
   - Enter your Google API key in the top navigation bar
   - Or set it in `.env` file (recommended)

4. **Upload Resume & Job**
   - Paste LaTeX format resume
   - Paste plain text job description

5. **Configure Settings**
   - Choose focus area (behavioral/technical/case/mixed)
   - Enable adaptive strategy (recommended)
   - Enable outcome prediction (recommended)

6. **Interview**
   - Answer 5-7 personalized questions
   - Get real-time scoring on 5 dimensions

7. **Get Feedback**
   - Detailed coaching report
   - Skill gap analysis
   - 2-week practice plan

### Streamlit UI (Legacy)

```bash
streamlit run app.py
```

### CLI

```bash
python main.py
```

### Example Resume (LaTeX)

```latex
\documentclass{article}
\begin{document}
\name{Your Name}
\section{Experience}
Software Engineer, Company, 2020-2023
\begin{itemize}
\item Built systems handling 1M+ requests/day
\item Reduced latency by 40%
\end{itemize}
\section{Skills}
Python, AWS, Docker, Kubernetes
\end{document}
```

### Example Job Description

```
Senior Software Engineer
Requirements:
- 5+ years experience
- Python, Java, AWS
- System design expertise
```

## Architecture

### Multi-Agent System (ADK)

```
ProfilerAgent → Creates interview strategy
InterviewerAgent → Generates questions
EvaluatorAgent → Scores answers (5 dimensions)
CoachAgent → Provides coaching feedback
```

### Agent Features

- **Memory**: Short-term, long-term, working memory
- **Tools**: Specialized capabilities per agent
- **Adaptive**: Adjusts based on performance
- **Learning**: Reflects and improves

## Project Structure

```
interview-coach/
├── api_server.py                # Flask REST API server ⭐ NEW
├── app.py                       # Streamlit UI (legacy)
├── main.py                      # CLI interface
├── demo.py                      # Feature demo
│
├── Frontend/                    # Modern frontend ⭐ NEW
│   ├── index.html              # Landing page
│   ├── interview.html          # Interview app
│   ├── app.js                  # JavaScript logic
│   ├── styles.css              # Styles
│   ├── guide.md                # Build guide
│   └── spec.json               # Component spec
│
├── start_interview_app.sh       # Startup script (Linux/Mac) ⭐ NEW
├── start_interview_app.bat      # Startup script (Windows) ⭐ NEW
├── INTEGRATION_GUIDE.md         # Integration guide ⭐ NEW
├── frontend-api-spec.json       # Complete API specification
├── FRONTEND_SPEC.md             # Frontend quick reference
│
├── adk_agents/                  # ADK-based agents
│   ├── base_agent.py           # Base class with memory & tools
│   ├── profiler_agent.py       # Strategy creation
│   ├── interviewer_agent.py    # Question generation
│   ├── evaluator_agent.py      # Answer evaluation
│   ├── coach_agent.py          # Coaching feedback
│   └── orchestrator.py         # Agent coordination
│
├── utils/                       # Parsers
│   ├── latex_parser.py         # Resume parser
│   └── job_parser.py           # Job description parser
│
├── prompts/                     # Agent prompts
├── state/                       # State management
└── examples/                    # Sample files
```

## Technology

- **Python 3.8+**
- **Google Gemini 2.5 Flash** - LLM for all agents
- **Google ADK Patterns** - Agent architecture
- **Streamlit** - Web interface
- **Pydantic** - Data validation

## Frontend Options

### 1. Modern Frontend (Included) ⭐ NEW

A beautiful, modern frontend built with vanilla HTML/CSS/JS:
- Dark theme with glassmorphism design
- Real-time scoring visualization
- Responsive layout
- No build step required

See **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** for setup instructions.

### 2. Build Your Own

See **[frontend-api-spec.json](frontend-api-spec.json)** for complete API specification to build your own frontend (React/Vue/Angular).

Quick reference: **[FRONTEND_SPEC.md](FRONTEND_SPEC.md)**

## Tips

**Resume:**
- Use standard LaTeX sections
- Include metrics and numbers
- List specific technologies

**Interview:**
- Use STAR format (Situation, Task, Action, Result)
- Be specific with metrics
- Keep answers concise (90-120 seconds)
- Relate to job requirements

## Troubleshooting

**API Key Error:**
```bash
export GOOGLE_API_KEY=your_key_here
```

**Slow Responses:**
- Normal: 3-7 seconds per turn
- Uses multiple agents with tools

**Resume Not Parsing:**
- Check LaTeX syntax
- Use standard sections
- See `examples/sample_resume.tex`

## Examples

See `examples/` directory:
- `sample_resume.tex` - Example resume
- `sample_job_description.txt` - Example job

## License

MIT

## Contributing

Contributions welcome! Fork, create a branch, and submit a PR.

---

**Ready to start?**

```bash
# Modern frontend (recommended)
./start_interview_app.sh      # Linux/Mac
start_interview_app.bat       # Windows

# Or manually
python api_server.py          # Start API
cd Frontend && python -m http.server 3000  # Start frontend

# Legacy options
streamlit run app.py          # Streamlit UI
python main.py                # CLI
python demo.py                # Feature demo
```

**Happy interviewing!** 🚀

# AI Mock Interview Coach

An intelligent mock interview system powered by Google's Agent Development Kit (ADK) and Gemini API. Features adaptive difficulty, real-time evaluation, outcome prediction, and personalized coaching.

🌐 **[Live Demo on Render](https://your-app.onrender.com)** (Deploy your own!)

## ✨ Features

- 🧠 **Multi-Agent AI System** - Specialized agents for profiling, interviewing, evaluating, and coaching
- 🎯 **Adaptive Difficulty** - Questions adjust based on your performance
- 📊 **Real-Time Evaluation** - Instant feedback on 5 dimensions (completeness, depth, structure, relevance, confidence)
- 🔮 **Outcome Prediction** - Early prediction of interview success
- 📈 **Pattern Detection** - Identifies your strengths and weaknesses
- 🎓 **Personalized Coaching** - Custom 2-week practice plans with skill gap analysis
- 🎨 **Modern UI** - Beautiful, responsive interface with dark theme

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/AnshulRoy28/Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment.git
cd Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Start the server
python run_server.py
```

**Or use the startup scripts:**

Linux/Mac: `./start.sh`  
Windows: `start.bat`

Then open http://localhost:8000

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.**

Quick steps:
1. Push code to GitHub
2. Connect GitHub to Render
3. Add `GOOGLE_API_KEY` environment variable
4. Deploy!

## 🎯 How It Works

### 1. Upload Your Materials
- Paste your resume (LaTeX format)
- Paste the job description (plain text)
- See `examples/` folder for samples

### 2. Configure Settings
- Choose focus area (behavioral/technical/case/mixed)
- Enable adaptive strategy
- Enable outcome prediction

### 3. Complete Interview
- Answer 5-7 personalized questions
- Get real-time scoring on each answer
- Receive instant feedback

### 4. Get Coaching Report
- Detailed performance analysis
- Skill gap identification
- 2-week personalized practice plan
- Benchmark against other candidates

## 🏗️ Architecture

### Unified Server
Single Flask server serves both API and frontend:
- **Frontend**: Landing page, interview app, static assets
- **API**: REST endpoints at `/api/v1/*`
- **No CORS issues**: Same-origin requests
- **Simple deployment**: One process, one port

### Multi-Agent System

```
ProfilerAgent → Analyzes candidate & creates strategy
     ↓
InterviewerAgent → Generates contextual questions
     ↓
EvaluatorAgent → Scores answers (5 dimensions)
     ↓
CoachAgent → Provides personalized feedback
```

Each agent has:
- **Memory**: Short-term, long-term, working memory
- **Tools**: Specialized capabilities
- **Adaptive behavior**: Adjusts based on performance

## 📁 Project Structure

```
├── api_server.py           # Flask server (API + static files)
├── run_server.py           # Server launcher
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── .env.example            # Environment template
│
├── Frontend/               # Web interface
│   ├── index.html          # Landing page
│   ├── interview.html      # Interview app
│   ├── app.js              # Frontend logic
│   └── styles.css          # Styling
│
├── adk_agents/             # ADK-based agents
│   ├── orchestrator.py     # Agent coordinator
│   ├── profiler_agent.py   # Strategy creation
│   ├── interviewer_agent.py # Question generation
│   ├── evaluator_agent.py  # Answer evaluation
│   └── coach_agent.py      # Coaching reports
│
├── utils/                  # Utilities
│   ├── latex_parser.py     # Resume parser
│   └── job_parser.py       # Job description parser
│
├── prompts/                # Agent prompts
├── state/                  # State management
├── tools/                  # Agent tools
└── examples/               # Sample files
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key: https://aistudio.google.com/app/apikey

### Advanced Settings

Edit `config.py`:
```python
MAX_INTERVIEW_TURNS = 7  # Number of questions
MODEL = "gemini-2.5-flash"  # Gemini model
```

## 🧪 Testing

```bash
# Run API tests
python test_api.py

# Manual testing
python run_server.py
# Open http://localhost:8000/interview.html
# Use sample files from examples/ folder
```

## 📊 API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Parse Resume
```bash
POST /api/v1/parse/resume
Content-Type: application/json

{
  "latex_content": "\\documentclass{article}..."
}
```

### Parse Job Description
```bash
POST /api/v1/parse/job
Content-Type: application/json

{
  "job_text": "Senior Software Engineer..."
}
```

### Initialize Interview
```bash
POST /api/v1/interview/initialize
Content-Type: application/json

{
  "resume_data": {...},
  "job_data": {...},
  "focus_area": "behavioral",
  "adaptive_strategy": true,
  "outcome_prediction": true
}
```

See `frontend-api-spec.json` for complete API documentation.

## 🚀 Production Deployment

### Render (Recommended)

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed guide.

```bash
# Deploy via GitHub
git push origin main
# Render auto-deploys on push
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "api_server:app"]
```

```bash
docker build -t ai-interview-coach .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key ai-interview-coach
```

### Other Platforms

Works on any Python hosting platform:
- Heroku
- Railway
- Fly.io
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

## 💡 Tips for Best Results

### Resume Tips
- Use standard LaTeX sections
- Include metrics and numbers
- List specific technologies
- Highlight achievements

### Interview Tips
- Use STAR format (Situation, Task, Action, Result)
- Be specific with metrics
- Keep answers concise (90-120 seconds)
- Relate answers to job requirements

## 🚨 Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Use different port
python run_server.py --port 3000
```

### API Key Issues
```bash
# Verify .env file
cat .env

# Should contain:
# GOOGLE_API_KEY=your_actual_key
```

### Frontend Not Loading
1. Verify `Frontend/` folder exists
2. Check server logs for errors
3. Try http://localhost:8000/api/v1/health

## 📚 Documentation

- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Deploy to Render
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment
- **[frontend-api-spec.json](frontend-api-spec.json)** - Complete API docs

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.11
- **Frontend**: Vanilla JavaScript (no build step!)
- **AI**: Google Gemini 2.5 Flash
- **Agents**: Google ADK patterns
- **Deployment**: Render, Docker-ready

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
- ✅ HTTPS on Render

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
- Deployed on [Render](https://render.com/)

## 📧 Contact

**Anshul Roy**
- GitHub: [@AnshulRoy28](https://github.com/AnshulRoy28)
- Repository: [AI Interview Coach](https://github.com/AnshulRoy28/Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment)

---

**Made with ❤️ for UpGrad AI Engineer Internship Assignment**

Ready to ace your next interview? 🚀

```bash
./start.sh  # or start.bat on Windows
```

Then open http://localhost:8000 and start practicing!

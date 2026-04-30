# Quick Reference Card

## 🚀 Start Commands

```bash
# Backend
python api_server.py

# Frontend
cd Frontend && python -m http.server 3000

# Test API
python test_api.py
```

## 🌐 URLs

- **Frontend**: http://localhost:3000/interview.html
- **API**: http://localhost:8000/api/v1
- **Health Check**: http://localhost:8000/api/v1/health

## 📁 Key Files

| File | Purpose |
|------|---------|
| `api_server.py` | Backend API server |
| `Frontend/app.js` | Frontend JavaScript |
| `Frontend/interview.html` | Main UI |
| `.env` | API key configuration |
| `examples/sample_resume.tex` | Sample resume |
| `examples/sample_job_description.txt` | Sample job |

## 🔑 Environment Setup

```bash
# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Quick Test

```bash
# Test health
curl http://localhost:8000/api/v1/health

# Test resume parsing
curl -X POST http://localhost:8000/api/v1/parse/resume \
  -H "Content-Type: application/json" \
  -d '{"latex_content": "\\documentclass{article}..."}'
```

## ✨ New Features

| Feature | Description |
|---------|-------------|
| **Connection Status** | Green/red dot in header |
| **Auto-Retry** | Retries failed requests 3 times |
| **Draft Save** | Auto-saves answers every 2s |
| **Health Check** | Checks API every 30s |
| **Input Validation** | Validates length before submit |

## 🎯 Limits

| Input | Max Length |
|-------|------------|
| Resume | 50,000 chars |
| Job Description | 20,000 chars |
| Answer | 5,000 chars |
| Session Timeout | 24 hours |

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Red connection dot | Start API server |
| API_KEY_MISSING | Set in .env or UI |
| Session expired | Start new interview |
| Port in use | Change port or kill process |

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/parse/resume` | Parse resume |
| POST | `/parse/job` | Parse job |
| POST | `/interview/initialize` | Start interview |
| GET | `/interview/{id}/question` | Get question |
| POST | `/interview/{id}/answer` | Submit answer |
| GET | `/interview/{id}/report` | Get report |

## 🔒 Security

- ✅ Input validation
- ✅ XSS protection
- ✅ Session expiration
- ✅ Length limits
- ✅ Error sanitization

## 📚 Documentation

| File | Content |
|------|---------|
| `READY_FOR_TESTING.md` | Start here! |
| `TESTING_GUIDE.md` | Detailed testing |
| `INTEGRATION_GUIDE.md` | Setup guide |
| `ENHANCEMENTS_SUMMARY.md` | All improvements |
| `CHANGELOG.md` | Version history |

## 💡 Tips

- Open DevTools (F12) to debug
- Check server logs for errors
- Use sample files for testing
- Clear localStorage to reset: `localStorage.clear()`

## 🎨 UI Elements

| Element | Location |
|---------|----------|
| Connection Status | Top right header |
| API Key Input | Top right header |
| Toast Notifications | Bottom of screen |
| Progress Bar | Interview page |
| Score Bars | After each answer |

## ⚡ Performance

| Operation | Expected Time |
|-----------|---------------|
| Health check | < 100ms |
| Parse resume | < 1s |
| Parse job | < 1s |
| Initialize | 5-10s |
| Get question | 3-7s |
| Submit answer | 3-5s |
| Generate report | 5-10s |

## 🎯 Testing Priority

1. ✅ Basic flow (setup → interview → results)
2. ✅ Connection status indicator
3. ✅ Retry logic (disconnect network)
4. ✅ Draft auto-save (refresh page)
5. ✅ Input validation (empty/long inputs)

---

**Quick Start**: `python api_server.py` → `cd Frontend && python -m http.server 3000` → Open http://localhost:3000/interview.html

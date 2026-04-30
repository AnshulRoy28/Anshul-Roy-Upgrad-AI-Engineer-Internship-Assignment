# Testing Guide

This guide will help you test the AI Mock Interview Coach application.

## Prerequisites

1. **Python 3.8+** installed
2. **Google API Key** for Gemini API
3. **Dependencies installed**: `pip install -r requirements.txt`

## Quick Start Testing

### 1. Start the Backend API Server

```bash
# Make sure you have your .env file configured
echo "GOOGLE_API_KEY=your_key_here" > .env

# Start the server
python api_server.py
```

You should see:
```
🚀 AI Mock Interview Coach - API Server
📡 Server starting on http://localhost:8000
📚 API Base URL: http://localhost:8000/api/v1
✅ Ready to accept requests!
```

### 2. Start the Frontend

Open a new terminal:

```bash
cd Frontend
python -m http.server 3000
```

### 3. Open the Application

Navigate to: `http://localhost:3000/interview.html`

## Manual Testing Checklist

### ✅ Connection & Setup

- [ ] Page loads without errors
- [ ] Connection status shows "● Connected" (green)
- [ ] API Key input is visible
- [ ] API URL input shows correct default URL

### ✅ Health Check

- [ ] Connection status updates automatically
- [ ] If API server is stopped, status shows "● Disconnected" (red)
- [ ] Warning toast appears if API key not configured

### ✅ Resume Input

- [ ] Can paste LaTeX resume
- [ ] Character count validation works (max 50,000 chars)
- [ ] Start button remains disabled until all fields filled

### ✅ Job Description Input

- [ ] Can paste plain text job description
- [ ] Character count validation works (max 20,000 chars)
- [ ] Start button enables when all fields valid

### ✅ Interview Initialization

- [ ] Click "Start Interview" button
- [ ] See toast: "Parsing resume..."
- [ ] See toast: "Parsing job description..."
- [ ] See toast: "Initializing interview..."
- [ ] View switches to interview page
- [ ] First question appears

### ✅ Interview Flow

- [ ] Question displays correctly
- [ ] Turn counter shows "Turn 1 of 7"
- [ ] Progress bar updates
- [ ] Can type answer in text area
- [ ] Answer auto-saves as draft (check localStorage)
- [ ] Submit button works
- [ ] Evaluation scores appear
- [ ] Next question loads automatically

### ✅ Adaptive Features

- [ ] After turn 3, adaptive strategy triggers (if enabled)
- [ ] After turn 3, outcome prediction appears (if enabled)
- [ ] Prediction shows outcome and confidence percentage

### ✅ Interview Completion

- [ ] Interview completes after max turns or early end
- [ ] "Generating coaching report..." toast appears
- [ ] View switches to results page
- [ ] Coaching report displays
- [ ] Readiness level shows
- [ ] Strengths list appears
- [ ] Skill gaps list appears
- [ ] Stats card shows correct data

### ✅ Error Handling

- [ ] Empty answer shows error toast
- [ ] Answer > 5000 chars shows error toast
- [ ] Network errors trigger retry (up to 3 times)
- [ ] Server errors (5xx) trigger retry
- [ ] Session expiration handled gracefully

### ✅ Draft Recovery

- [ ] Type answer but don't submit
- [ ] Refresh page
- [ ] Start new interview
- [ ] Prompt appears to restore draft
- [ ] Draft restores correctly if accepted

### ✅ Restart Flow

- [ ] Click "Start New Interview" on results page
- [ ] Returns to setup page
- [ ] All inputs cleared
- [ ] State reset correctly

## API Testing

### Test Health Endpoint

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-04-30T...",
  "active_sessions": 0,
  "api_key_configured": true
}
```

### Test Resume Parsing

```bash
curl -X POST http://localhost:8000/api/v1/parse/resume \
  -H "Content-Type: application/json" \
  -d '{
    "latex_content": "\\documentclass{article}\\begin{document}\\name{John Doe}\\end{document}"
  }'
```

### Test Job Parsing

```bash
curl -X POST http://localhost:8000/api/v1/parse/job \
  -H "Content-Type: application/json" \
  -d '{
    "job_text": "Senior Software Engineer\n\nRequirements:\n- 5+ years experience"
  }'
```

### Test Full Interview Flow

```bash
# 1. Parse resume
RESUME_DATA=$(curl -s -X POST http://localhost:8000/api/v1/parse/resume \
  -H "Content-Type: application/json" \
  -d @examples/sample_resume.tex)

# 2. Parse job
JOB_DATA=$(curl -s -X POST http://localhost:8000/api/v1/parse/job \
  -H "Content-Type: application/json" \
  -d @examples/sample_job_description.txt)

# 3. Initialize interview
SESSION=$(curl -s -X POST http://localhost:8000/api/v1/interview/initialize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d "{
    \"resume_data\": $RESUME_DATA,
    \"job_data\": $JOB_DATA,
    \"focus_area\": \"behavioral\",
    \"adaptive_strategy\": true,
    \"outcome_prediction\": true
  }")

SESSION_ID=$(echo $SESSION | jq -r '.session_id')

# 4. Get question
curl http://localhost:8000/api/v1/interview/$SESSION_ID/question

# 5. Submit answer
curl -X POST http://localhost:8000/api/v1/interview/$SESSION_ID/answer \
  -H "Content-Type: application/json" \
  -d '{
    "answer": "In my previous role as a senior engineer, I led a team of 5 developers..."
  }'
```

## Performance Testing

### Response Time Benchmarks

- Health check: < 100ms
- Parse resume: < 1s
- Parse job: < 1s
- Initialize interview: 5-10s (includes AI profiler)
- Get question: 3-7s (AI generation)
- Submit answer: 3-5s (AI evaluation)
- Generate report: 5-10s (AI coaching)

### Load Testing

```bash
# Install Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/api/v1/health
```

## Browser Testing

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari

Check:
- [ ] Layout renders correctly
- [ ] Animations work smoothly
- [ ] LocalStorage works
- [ ] Fetch API works
- [ ] No console errors

## Mobile Testing

- [ ] Responsive design works on mobile
- [ ] Touch interactions work
- [ ] Text inputs work on mobile keyboard
- [ ] Scrolling works smoothly

## Security Testing

### Input Validation

- [ ] XSS protection: Try `<script>alert('xss')</script>` in inputs
- [ ] SQL injection: Try `'; DROP TABLE users; --` (should be sanitized)
- [ ] Long inputs: Try 100,000 character strings (should be rejected)

### API Key Security

- [ ] API key not visible in network requests (check DevTools)
- [ ] API key stored securely in localStorage
- [ ] API key not logged to console

## Common Issues & Solutions

### Issue: "Cannot connect to API server"

**Solution:**
1. Check if API server is running: `curl http://localhost:8000/api/v1/health`
2. Check firewall settings
3. Verify port 8000 is not in use: `lsof -i :8000`

### Issue: "API_KEY_MISSING" error

**Solution:**
1. Set API key in `.env` file
2. Or enter API key in the UI
3. Restart API server after updating `.env`

### Issue: Session expired

**Solution:**
- Sessions expire after 24 hours
- Restart interview if session expired
- For production, implement Redis session storage

### Issue: Slow AI responses

**Solution:**
- Normal for first request (cold start)
- Subsequent requests should be faster
- Check internet connection
- Verify API key has quota remaining

### Issue: CORS errors

**Solution:**
- Ensure `flask-cors` is installed
- Check API server logs for CORS configuration
- Verify frontend URL matches CORS settings

## Debugging Tips

### Enable Verbose Logging

Backend:
```python
# In api_server.py
logging.basicConfig(level=logging.DEBUG)
```

Frontend:
```javascript
// In app.js, uncomment console.log statements
console.log('API call:', method, path, body);
```

### Check Browser DevTools

1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "Fetch/XHR"
4. Check request/response details
5. Look for errors in Console tab

### Check Server Logs

```bash
# API server logs appear in terminal
# Look for ERROR or WARNING messages
```

### Inspect LocalStorage

```javascript
// In browser console
console.log(localStorage);
console.log(localStorage.getItem('interviewai_apikey'));
console.log(localStorage.getItem('interviewai_draft_answer'));
```

## Automated Testing (Future)

Consider adding:
- Unit tests with pytest (backend)
- Integration tests with pytest + requests
- E2E tests with Playwright/Selenium
- API tests with Postman/Newman
- Load tests with Locust

## Test Data

Use the provided sample files:
- `examples/sample_resume.tex` - Sample LaTeX resume
- `examples/sample_job_description.txt` - Sample job description

## Reporting Issues

When reporting issues, include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Browser/OS version
5. API server logs
6. Browser console errors
7. Network request details

---

**Happy Testing!** 🧪

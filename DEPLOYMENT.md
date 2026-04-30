# Deployment Guide

This guide covers deploying the AI Mock Interview Coach to various platforms.

## 📋 Pre-Deployment Checklist

- [ ] All tests passing locally (`python test_api.py`)
- [ ] `.env` file configured with valid API key
- [ ] Code pushed to GitHub
- [ ] Dependencies listed in `requirements.txt`
- [ ] Frontend tested locally

---

## 🚀 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Backend (API Server)**

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   ```
   Name: interview-coach-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn api_server:app
   ```

3. **Add Environment Variables**
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note the URL: `https://interview-coach-api.onrender.com`

**Frontend (Static Site)**

1. **Create New Static Site**
   - Click "New +" → "Static Site"
   - Connect same GitHub repository

2. **Configure**
   ```
   Name: interview-coach-frontend
   Build Command: (leave empty)
   Publish Directory: Frontend
   ```

3. **Update Frontend**
   - Edit `Frontend/app.js`
   - Change `baseUrl` to your Render API URL:
   ```javascript
   baseUrl: 'https://interview-coach-api.onrender.com/api/v1'
   ```

4. **Deploy**
   - Click "Create Static Site"
   - Access at: `https://interview-coach-frontend.onrender.com`

---

### Option 2: Heroku

**Backend**

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create interview-coach-api
   ```

3. **Add Procfile**
   ```bash
   echo "web: gunicorn api_server:app" > Procfile
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_key_here
   ```

5. **Deploy**
   ```bash
   git push heroku prototype:main
   ```

**Frontend**

Deploy to Netlify or Vercel (see below)

---

### Option 3: Railway

**Backend**

1. **Create New Project**
   - Go to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

2. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `GOOGLE_API_KEY`
   - Set start command: `gunicorn api_server:app`

3. **Deploy**
   - Railway deploys automatically
   - Get URL from dashboard

---

### Option 4: Vercel (Frontend Only)

**Frontend Deployment**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd Frontend
   vercel
   ```

3. **Configure**
   - Update `app.js` with your API URL
   - Redeploy: `vercel --prod`

---

### Option 5: Netlify (Frontend Only)

**Frontend Deployment**

1. **Create `netlify.toml`**
   ```toml
   [build]
     publish = "Frontend"
   
   [[redirects]]
     from = "/*"
     to = "/interview.html"
     status = 200
   ```

2. **Deploy**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Deploy
   netlify deploy --prod --dir=Frontend
   ```

---

### Option 6: AWS (Production)

**Backend (EC2 + Elastic Beanstalk)**

1. **Create `application.py`**
   ```python
   from api_server import app as application
   
   if __name__ == "__main__":
       application.run()
   ```

2. **Create `.ebextensions/python.config`**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: application:application
   ```

3. **Deploy**
   ```bash
   eb init -p python-3.11 interview-coach
   eb create interview-coach-env
   eb setenv GOOGLE_API_KEY=your_key_here
   eb deploy
   ```

**Frontend (S3 + CloudFront)**

1. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://interview-coach-frontend
   ```

2. **Upload Files**
   ```bash
   aws s3 sync Frontend/ s3://interview-coach-frontend/
   ```

3. **Enable Static Website Hosting**
   - Go to S3 bucket settings
   - Enable static website hosting
   - Set index document: `interview.html`

4. **Create CloudFront Distribution**
   - Point to S3 bucket
   - Enable HTTPS

---

### Option 7: Google Cloud Platform

**Backend (Cloud Run)**

1. **Create `Dockerfile`**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-b", "0.0.0.0:8080", "api_server:app"]
   ```

2. **Deploy**
   ```bash
   gcloud run deploy interview-coach-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your_key_here
   ```

**Frontend (Firebase Hosting)**

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Initialize**
   ```bash
   firebase init hosting
   # Select Frontend as public directory
   ```

3. **Deploy**
   ```bash
   firebase deploy
   ```

---

## 🔧 Production Configuration

### Required Changes for Production

1. **Add Gunicorn** (for WSGI server)
   ```bash
   echo "gunicorn>=21.0.0" >> requirements.txt
   ```

2. **Update CORS Settings** (in `api_server.py`)
   ```python
   from flask_cors import CORS
   
   # Replace
   CORS(app)
   
   # With
   CORS(app, origins=[
       "https://your-frontend-domain.com",
       "http://localhost:5500"  # For local testing
   ])
   ```

3. **Enable Production Mode**
   ```python
   # In api_server.py, change:
   app.run(host='0.0.0.0', port=8000, debug=True)
   
   # To:
   app.run(host='0.0.0.0', port=8000, debug=False)
   ```

4. **Add Health Check Endpoint** (already implemented ✅)
   ```
   GET /api/v1/health
   ```

5. **Set Environment Variables**
   ```bash
   GOOGLE_API_KEY=your_production_key
   FLASK_ENV=production
   PORT=8000
   ```

---

## 🔒 Security Checklist

- [ ] API key stored in environment variables (not in code)
- [ ] CORS configured for specific domains
- [ ] HTTPS enabled
- [ ] Rate limiting implemented (optional)
- [ ] Input validation enabled (already implemented ✅)
- [ ] Session expiration configured (24 hours ✅)
- [ ] Error messages don't leak sensitive info (already implemented ✅)

---

## 📊 Monitoring

### Recommended Tools

1. **Uptime Monitoring**
   - [UptimeRobot](https://uptimerobot.com/) (Free)
   - [Pingdom](https://www.pingdom.com/)

2. **Error Tracking**
   - [Sentry](https://sentry.io/) (Free tier)
   - [Rollbar](https://rollbar.com/)

3. **Analytics**
   - Google Analytics
   - Plausible Analytics

### Health Check Endpoint

Monitor this endpoint:
```
GET https://your-api-domain.com/api/v1/health
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

---

## 🐛 Troubleshooting Deployment

### Common Issues

**1. Module Not Found**
```bash
# Solution: Ensure all dependencies in requirements.txt
pip freeze > requirements.txt
```

**2. Port Already in Use**
```bash
# Solution: Use environment variable
PORT=${PORT:-8000}
```

**3. API Key Not Found**
```bash
# Solution: Set environment variable in platform
GOOGLE_API_KEY=your_key_here
```

**4. CORS Errors**
```python
# Solution: Update CORS settings
CORS(app, origins=["https://your-frontend.com"])
```

**5. Timeout Errors**
```bash
# Solution: Increase timeout in platform settings
# Or optimize API calls
```

---

## 📈 Scaling Considerations

### For High Traffic

1. **Use Redis for Sessions**
   - Replace in-memory sessions
   - Enable session sharing across instances

2. **Add Load Balancer**
   - Distribute traffic across multiple instances
   - Most platforms provide this automatically

3. **Enable Caching**
   - Cache parsed resumes/jobs
   - Use CDN for frontend assets

4. **Database for Persistence**
   - Store interview sessions
   - Enable analytics

---

## 💰 Cost Estimates

### Free Tier Options
- **Render**: Free (with limitations)
- **Heroku**: Free dyno (sleeps after 30 min)
- **Railway**: $5 credit/month
- **Vercel/Netlify**: Free for frontend

### Paid Options
- **Render**: $7/month (Starter)
- **Heroku**: $7/month (Hobby)
- **AWS**: ~$10-20/month (t2.micro)
- **GCP**: ~$10-20/month (Cloud Run)

---

## 🎯 Recommended Setup

**For Development/Testing:**
- Backend: Render (Free)
- Frontend: Netlify (Free)

**For Production:**
- Backend: Render (Starter $7/mo) or Railway
- Frontend: Vercel or Netlify (Free)
- Monitoring: UptimeRobot + Sentry (Free tiers)

---

## 📝 Post-Deployment

1. **Test All Endpoints**
   ```bash
   curl https://your-api.com/api/v1/health
   ```

2. **Update Documentation**
   - Add production URLs to README
   - Update QUICKSTART with deployment info

3. **Set Up Monitoring**
   - Configure uptime checks
   - Set up error alerts

4. **Enable Analytics**
   - Track usage patterns
   - Monitor performance

---

## 🔄 Continuous Deployment

### GitHub Actions (Recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main, prototype]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review error logs
3. Test locally first
4. Check environment variables

---

**Ready to deploy!** Choose your platform and follow the steps above. 🚀

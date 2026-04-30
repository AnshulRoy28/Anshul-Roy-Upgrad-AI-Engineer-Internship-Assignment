# 🚀 Render Deployment Guide

This guide will help you deploy the AI Mock Interview Coach to Render using GitHub.

## Prerequisites

- GitHub account
- Render account (free tier works!)
- Google API Key ([Get one here](https://aistudio.google.com/app/apikey))

## 📋 Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Mock Interview Coach"

# Add remote
git remote add origin https://github.com/AnshulRoy28/Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment.git

# Push to GitHub
git push -u origin main
```

### 2. Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** (if not already connected)
4. Select your repository: `AnshulRoy28/Anshul-Roy-Upgrad-AI-Engineer-Internship-Assignment`

### 3. Configure the Service

Render will auto-detect the `render.yaml` file. Verify these settings:

**Basic Settings:**
- **Name**: `ai-interview-coach` (or your preferred name)
- **Region**: Oregon (or closest to you)
- **Branch**: `main`
- **Runtime**: Python 3

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT api_server:app`

### 4. Add Environment Variables

In the Render dashboard, add the following environment variable:

| Key | Value |
|-----|-------|
| `GOOGLE_API_KEY` | Your Google API key |

**How to add:**
1. Go to your service dashboard
2. Click **"Environment"** in the left sidebar
3. Click **"Add Environment Variable"**
4. Enter `GOOGLE_API_KEY` as the key
5. Paste your Google API key as the value
6. Click **"Save Changes"**

### 5. Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start the server
   - Assign a public URL

**Deployment takes 2-5 minutes.**

### 6. Access Your Application

Once deployed, Render will provide a URL like:
```
https://ai-interview-coach.onrender.com
```

**Test it:**
- Landing page: `https://your-app.onrender.com/`
- Interview app: `https://your-app.onrender.com/interview.html`
- Health check: `https://your-app.onrender.com/api/v1/health`

## 🔧 Configuration Details

### render.yaml

The `render.yaml` file contains all deployment configuration:

```yaml
services:
  - type: web
    name: ai-interview-coach
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT api_server:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: GOOGLE_API_KEY
        sync: false
    healthCheckPath: /api/v1/health
```

### Key Features

- **Auto-deploy**: Pushes to `main` branch trigger automatic deployments
- **Health checks**: Render monitors `/api/v1/health` endpoint
- **Free tier**: Includes 750 hours/month (enough for continuous operation)
- **HTTPS**: Automatic SSL certificate
- **Custom domain**: Can add your own domain (optional)

## 🎯 Post-Deployment

### 1. Test the Application

Visit your Render URL and:
1. ✅ Verify landing page loads
2. ✅ Navigate to interview page
3. ✅ Enter API key in the app (or use environment variable)
4. ✅ Upload sample resume and job description
5. ✅ Complete a mock interview
6. ✅ Verify coaching report generates

### 2. Monitor Logs

In Render dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. Monitor for any errors

### 3. Check Health

```bash
curl https://your-app.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "active_sessions": 0,
  "api_key_configured": true
}
```

## 🔄 Updating Your Application

### Automatic Deployment

Any push to the `main` branch triggers automatic deployment:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically:
1. Detect the push
2. Rebuild the application
3. Deploy the new version
4. Zero-downtime deployment

### Manual Deployment

In Render dashboard:
1. Go to your service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## ⚙️ Advanced Configuration

### Custom Domain

1. In Render dashboard, go to **"Settings"**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Follow DNS configuration instructions

### Scaling

**Free Tier Limitations:**
- Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month

**Upgrade to Paid Plan:**
- No spin-down
- More CPU/RAM
- Better performance
- Starting at $7/month

### Environment Variables

Add more environment variables as needed:

```yaml
envVars:
  - key: MAX_INTERVIEW_TURNS
    value: 7
  - key: MODEL
    value: gemini-2.5-flash
```

## 🚨 Troubleshooting

### Build Fails

**Check logs for:**
- Missing dependencies in `requirements.txt`
- Python version compatibility
- Syntax errors

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python api_server.py
```

### Application Won't Start

**Common issues:**
1. Missing `GOOGLE_API_KEY` environment variable
2. Port binding issues (ensure using `$PORT`)
3. Import errors

**Check:**
- Environment variables are set correctly
- `api_server.py` uses `os.environ.get('PORT', 8000)`
- All imports are in `requirements.txt`

### Health Check Failing

**Verify:**
```bash
curl https://your-app.onrender.com/api/v1/health
```

**If failing:**
1. Check logs for errors
2. Verify Flask app is running
3. Ensure `/api/v1/health` endpoint exists

### Slow First Request

**This is normal on free tier:**
- App spins down after 15 minutes of inactivity
- First request wakes it up (30-60 seconds)
- Subsequent requests are fast

**Solutions:**
- Upgrade to paid plan (no spin-down)
- Use a service like UptimeRobot to ping every 14 minutes
- Accept the cold start on free tier

### API Key Issues

**If API key not working:**
1. Verify it's set in Render environment variables
2. Check it's not in `.env` file (not used in production)
3. Restart the service after adding environment variables

## 📊 Monitoring

### Render Dashboard

Monitor:
- **Metrics**: CPU, memory, response time
- **Logs**: Real-time application logs
- **Events**: Deployment history
- **Health**: Uptime and health checks

### Custom Monitoring

Add monitoring tools:
- **Sentry**: Error tracking
- **LogDNA**: Log management
- **UptimeRobot**: Uptime monitoring

## 💰 Cost Estimate

### Free Tier
- **Cost**: $0/month
- **Hours**: 750/month
- **Limitations**: Spins down after 15 min inactivity
- **Best for**: Testing, demos, low-traffic apps

### Starter Plan
- **Cost**: $7/month
- **Hours**: Unlimited
- **Limitations**: None
- **Best for**: Production apps, consistent traffic

## 🔒 Security

### Environment Variables
- ✅ Never commit API keys to Git
- ✅ Use Render environment variables
- ✅ Rotate keys regularly

### HTTPS
- ✅ Automatic SSL certificate
- ✅ All traffic encrypted
- ✅ No configuration needed

### Best Practices
- ✅ Keep dependencies updated
- ✅ Monitor logs for suspicious activity
- ✅ Use strong API keys
- ✅ Implement rate limiting (if needed)

## 📚 Resources

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-flask)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Custom Domains](https://render.com/docs/custom-domains)

## ✅ Deployment Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] `render.yaml` configured
- [ ] `requirements.txt` includes all dependencies
- [ ] Google API key ready
- [ ] Tested locally

After deploying:
- [ ] Service deployed successfully
- [ ] Environment variables set
- [ ] Health check passing
- [ ] Landing page accessible
- [ ] Interview app working
- [ ] API endpoints responding
- [ ] Logs show no errors

## 🎉 Success!

Your AI Mock Interview Coach is now live on Render!

**Share your app:**
```
https://your-app.onrender.com
```

**Next steps:**
1. Test all features
2. Share with users
3. Monitor performance
4. Gather feedback
5. Iterate and improve

---

**Need help?** Check the [Render Community](https://community.render.com/) or open an issue on GitHub.

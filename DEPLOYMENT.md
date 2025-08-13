# Deployment Guide

This portfolio can be deployed in multiple ways. Here's how the components work together across different platforms.

## How Hybrid Deployment Works

When you split deployment across platforms, the **launcher** acts as the central hub that knows where each component is deployed:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Pages  │    │     Render       │    │    Netlify      │
│                 │    │                  │    │                 │
│ • Launcher      │────│ • Flask App      │    │ • Alternative   │
│ • React App     │    │ • Django App     │    │   Static Host   │
│ • Vue App       │    │                  │    │                 │
│ • Angular App   │    │                  │    │                 │
│ • Shared Assets │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

The launcher uses `deployment-config.js` to automatically detect the environment and route to the correct URLs.

## Option 1: Hybrid Deployment (Recommended)

### Step 1: Deploy Dynamic Apps to Render

1. **Flask App**:
   - Create new Web Service on Render
   - Connect your GitHub repo
   - Set build command: `cd flask-app && pip install -r requirements.txt`
   - Set start command: `cd flask-app && python app.py`
   - Note the deployed URL (e.g., `https://your-flask.onrender.com`)

2. **Django App**:
   - Create new Web Service on Render
   - Connect your GitHub repo
   - Set build command: `cd django-app && pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Set start command: `cd django-app && python manage.py runserver 0.0.0.0:$PORT`
   - Note the deployed URL (e.g., `https://your-django.onrender.com`)

### Step 2: Configure and Deploy Static Components

1. **Configure URLs**:
   ```bash
   ./deploy-hybrid.sh
   # Enter your Flask and Django URLs when prompted
   ```

2. **Deploy to GitHub Pages**:
   - Push your code to GitHub
   - Enable GitHub Actions in your repo
   - The workflow will automatically build and deploy to `gh-pages` branch
   - Enable GitHub Pages in repo settings → Pages → Source: Deploy from branch → `gh-pages`

### Step 3: Test the Integration

Visit your GitHub Pages URL (e.g., `https://yourusername.github.io/portfolio/`):
- React, Vue, Angular will load from GitHub Pages
- Flask, Django will load from Render
- All components appear as one unified portfolio

## Option 2: All Static Deployment

### Netlify (Free tier: 100GB bandwidth)
1. Connect your GitHub repo to Netlify
2. Build settings are configured in `netlify.toml`
3. Automatic deployments on every push

### Vercel (Free tier: 100GB bandwidth)
1. Connect GitHub repo to Vercel
2. Auto-detects build settings
3. Excellent performance and CDN

## Option 2: Full Docker Deployment

### Railway (Free tier: $5 credit monthly)
1. Connect GitHub repo to Railway
2. Uses `railway.toml` configuration
3. Supports full Docker setup with all frameworks

### Render (Free tier with limitations)
1. Create new Web Service
2. Connect GitHub repo
3. Use Docker build
4. Set start command: `docker-compose up --build`

### Fly.io (Free allowance)
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

## Option 3: Hybrid Approach (Recommended)

1. **Static parts** (React, Vue, Angular, Launcher) → GitHub Pages/Netlify
2. **Dynamic parts** (Flask, Django) → Railway/Render
3. Update launcher to point to deployed dynamic apps

## Quick Deploy Commands

### Build static version:
```bash
./deploy-static.sh
```

### Test production build locally:
```bash
./production-test.sh
```

### Deploy to Surge.sh:
```bash
npm install -g surge
./deploy-static.sh
surge ./deploy/static/
```

## Environment Variables

For dynamic deployments, set these environment variables:
- `PORT` - Application port (usually set automatically)
- `NODE_ENV=production`
- `PYTHONPATH` - For Django/Flask apps

## Custom Domain

Most platforms support custom domains:
- GitHub Pages: Add CNAME file
- Netlify: Domain settings in dashboard
- Vercel: Domain settings in dashboard
- Railway: Custom domain in project settings

## Performance Tips

1. **Enable CDN** - Most platforms include this
2. **Compress assets** - Already configured in build
3. **Cache headers** - Configured in nginx/netlify.toml
4. **Minification** - Enabled in Vite configs

## Monitoring

Free monitoring options:
- **Uptime Robot** - Free uptime monitoring
- **Google Analytics** - Add to launcher page
- **Netlify Analytics** - Built-in (paid feature)

## Costs

- **GitHub Pages**: Free (public repos)
- **Netlify**: Free tier → $19/month
- **Vercel**: Free tier → $20/month  
- **Railway**: $5 credit/month → $5/month
- **Render**: Free tier → $7/month
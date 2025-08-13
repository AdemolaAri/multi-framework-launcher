#!/bin/bash

echo "🔧 Setting up Hybrid Deployment..."

# Get deployment URLs from user
echo "Enter your deployment URLs:"
read -p "Flask app URL (e.g., https://your-flask.onrender.com): " FLASK_URL
read -p "Django app URL (e.g., https://your-django.onrender.com): " DJANGO_URL

# Create hybrid configuration
cat > nginx/launcher/deployment-config.js << EOF
// Deployment configuration for different environments
const DEPLOYMENT_CONFIGS = {
  // Local development (Docker)
  local: {
    react: '/react/',
    vue: '/vue/',
    angular: '/angular/',
    flask: '/flask/',
    django: '/django/',
    shared: '/shared/'
  },
  
  // Hybrid deployment (static on GitHub Pages, dynamic on Render)
  hybrid: {
    react: '/react/',
    vue: '/vue/',
    angular: '/angular/',
    flask: '${FLASK_URL}',
    django: '${DJANGO_URL}',
    shared: '/shared/'
  },
  
  // All static (GitHub Pages/Netlify)
  static: {
    react: '/react/',
    vue: '/vue/',
    angular: '/angular/',
    flask: '/flask/',
    django: '/django/',
    shared: '/shared/'
  }
};

// Auto-detect environment
function getDeploymentConfig() {
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return DEPLOYMENT_CONFIGS.local;
  } else if (hostname.includes('github.io') || hostname.includes('netlify.app')) {
    return DEPLOYMENT_CONFIGS.hybrid;
  } else {
    return DEPLOYMENT_CONFIGS.static;
  }
}

window.PORTFOLIO_CONFIG = getDeploymentConfig();
console.log('Portfolio deployment config:', window.PORTFOLIO_CONFIG);
EOF

echo "✅ Hybrid configuration created!"
echo ""
echo "📦 Building static components..."
./deploy-static.sh

echo ""
echo "🚀 Next steps:"
echo "1. Deploy Flask app to Render: ${FLASK_URL}"
echo "2. Deploy Django app to Render: ${DJANGO_URL}"
echo "3. Deploy static files to GitHub Pages/Netlify"
echo ""
echo "📁 Static files ready in: ./deploy/static/"
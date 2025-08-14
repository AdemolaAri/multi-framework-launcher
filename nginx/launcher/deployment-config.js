// Deployment configuration for different environments
const DEPLOYMENT_CONFIGS = {
  // Local development (Docker)
  local: {
    react: 'react/',
    vue: 'vue/',
    angular: 'angular/',
    flask: 'flask/',
    django: 'django/',
    shared: 'shared/'
  },
  
  // Hybrid deployment (static on GitHub Pages, dynamic on Render)
  hybrid: {
    react: 'react/',  // Served from same static host
    vue: 'vue/',      // Served from same static host
    angular: 'angular/', // Served from same static host
    flask: 'https://your-portfolio-flask.onrender.com/',
    django: 'https://your-portfolio-django.onrender.com/',
    shared: 'shared/' // Served from same static host
  },
  
  // All static (GitHub Pages/Netlify)
  static: {
    react: 'react/',
    vue: 'vue/',
    angular: 'angular/',
    flask: 'flask/',  // Static version
    django: 'django/', // Static version
    shared: 'shared/'
  },
  
  // Full Docker deployment (Railway/Render)
  docker: {
    react: 'react/',
    vue: 'vue/',
    angular: 'angular/',
    flask: 'flask/',
    django: 'django/',
    shared: 'shared/'
  }
};

// Auto-detect environment or use manual override
function getDeploymentConfig() {
  // Check for manual override
  const override = window.DEPLOYMENT_ENV;
  if (override && DEPLOYMENT_CONFIGS[override]) {
    return DEPLOYMENT_CONFIGS[override];
  }
  
  // Auto-detect based on hostname
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return DEPLOYMENT_CONFIGS.local;
  } else if (hostname.includes('github.io') || hostname.includes('netlify.app')) {
    return DEPLOYMENT_CONFIGS.static; // Use static config for GitHub Pages
  } else if (hostname.includes('railway.app') || hostname.includes('fly.dev')) {
    return DEPLOYMENT_CONFIGS.docker;
  } else {
    // Default to hybrid for custom domains
    return DEPLOYMENT_CONFIGS.hybrid;
  }
}

// Export the active configuration
window.PORTFOLIO_CONFIG = getDeploymentConfig();

console.log('Portfolio deployment config:', window.PORTFOLIO_CONFIG);
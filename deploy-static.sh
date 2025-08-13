#!/bin/bash

echo "🚀 Building Static Sites for Deployment..."

# Create deployment directory
mkdir -p deploy/static

echo "📦 Building React app..."
cd react-app
npm run build
cp -r dist ../deploy/static/react
cd ..

echo "📦 Building Vue app..."
cd vue-app
npm run build
cp -r dist ../deploy/static/vue
cd ..

echo "📦 Building Angular app..."
cd angular-app
# Angular is already built as static files
cp -r dist ../deploy/static/angular
cd ..

echo "📦 Copying launcher..."
cp -r nginx/launcher/* deploy/static/

echo "📦 Copying shared assets..."
cp -r shared deploy/static/

echo "✅ Static build complete!"
echo "📁 Files ready in: ./deploy/static/"
echo ""
echo "🌐 Deploy options:"
echo "1. GitHub Pages: Push to gh-pages branch"
echo "2. Netlify: Drag & drop ./deploy/static/ folder"
echo "3. Vercel: Connect GitHub repo"
echo "4. Surge: Run 'surge ./deploy/static/'"
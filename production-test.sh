#!/bin/bash

echo "🏗️  Testing Production Build Approach..."

echo "🧹 Cleaning up existing containers..."
docker-compose down
docker system prune -f

echo "🔨 Building production containers..."
echo "This may take a few minutes as we're building React and Vue apps..."
docker-compose build --no-cache react vue nginx

echo "🚀 Starting containers..."
docker-compose up -d

echo "⏳ Waiting for containers to fully start..."
sleep 20

echo "🔍 Checking container status..."
docker-compose ps

echo ""
echo "🌐 Testing endpoints..."
echo "Main launcher: http://localhost:8080"
echo "React app: http://localhost:8080/react/"
echo "Vue app: http://localhost:8080/vue/"

echo ""
echo "📋 Testing HTTP responses..."
echo "--- React Response ---"
curl -I http://localhost:8080/react/ 2>/dev/null | head -3

echo ""
echo "--- Vue Response ---"
curl -I http://localhost:8080/vue/ 2>/dev/null | head -3

echo ""
echo "📝 Container logs (last 5 lines each):"
echo "--- React ---"
docker-compose logs react | tail -5
echo ""
echo "--- Vue ---"
docker-compose logs vue | tail -5
echo ""
echo "--- Nginx ---"
docker-compose logs nginx | tail -5

echo ""
echo "✅ Production build test complete!"
echo "🌐 Visit http://localhost:8080 to test the portfolio"
echo ""
echo "If you see any issues, check the logs above or run:"
echo "docker-compose logs [service-name]"
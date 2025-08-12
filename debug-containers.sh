#!/bin/bash

echo "🔍 Debugging Portfolio Containers..."

echo "📋 Container Status:"
docker-compose ps

echo ""
echo "🌐 Testing Direct Container Access:"
echo "React container: http://localhost:3000"
echo "Vue container: http://localhost:5173"

echo ""
echo "📝 Container Logs:"
echo "--- React Logs ---"
docker-compose logs react | tail -10

echo ""
echo "--- Vue Logs ---"
docker-compose logs vue | tail -10

echo ""
echo "--- Nginx Logs ---"
docker-compose logs nginx | tail -10

echo ""
echo "🔧 Testing nginx proxy paths:"
curl -I http://localhost:8080/react/ 2>/dev/null | head -5
echo ""
curl -I http://localhost:8080/vue/ 2>/dev/null | head -5
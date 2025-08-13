#!/bin/bash

echo "🔧 Testing MIME Type Fix..."

echo "🔄 Rebuilding containers with new configuration..."
docker-compose down
docker-compose build nginx react vue
docker-compose up -d

echo "⏳ Waiting for containers to start..."
sleep 15

echo "🔍 Testing React app..."
echo "URL: http://localhost:8080/react/"
curl -I http://localhost:8080/react/ 2>/dev/null | head -3

echo ""
echo "🔍 Testing Vue app..."
echo "URL: http://localhost:8080/vue/"
curl -I http://localhost:8080/vue/ 2>/dev/null | head -3

echo ""
echo "📋 Container status:"
docker-compose ps

echo ""
echo "📝 Recent logs:"
echo "--- React ---"
docker-compose logs react | tail -3
echo "--- Vue ---"
docker-compose logs vue | tail -3

echo ""
echo "✅ Test complete. Try accessing the apps now:"
echo "React: http://localhost:8080/react/"
echo "Vue: http://localhost:8080/vue/"
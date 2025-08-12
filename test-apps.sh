#!/bin/bash

echo "🧪 Testing React and Vue Apps..."

echo "🔄 Rebuilding containers..."
docker-compose down
docker-compose build react vue
docker-compose up -d

echo "⏳ Waiting for containers to start..."
sleep 15

echo "🔍 Checking container status..."
docker-compose ps

echo ""
echo "📋 Testing React app..."
echo "Direct access: http://localhost:3000"
echo "Through proxy: http://localhost:8080/react/"

echo ""
echo "📋 Testing Vue app..."
echo "Direct access: http://localhost:5173"
echo "Through proxy: http://localhost:8080/vue/"

echo ""
echo "🔧 Container logs:"
echo "--- React Container ---"
docker-compose logs react | tail -5

echo ""
echo "--- Vue Container ---"
docker-compose logs vue | tail -5

echo ""
echo "✅ Test complete. Check the URLs above in your browser."
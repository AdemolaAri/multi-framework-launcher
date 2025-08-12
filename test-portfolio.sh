#!/bin/bash

echo "🚀 Testing Portfolio Setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose down
docker-compose up --build -d

echo "⏳ Waiting for containers to start..."
sleep 10

echo "🔍 Checking container status..."
docker-compose ps

echo "🌐 Testing endpoints..."
echo "Main launcher: http://localhost:8080"
echo "React app: http://localhost:8080/react/"
echo "Vue app: http://localhost:8080/vue/"
echo "Angular app: http://localhost:8080/angular/"
echo "Flask app: http://localhost:8080/flask/"
echo "Django app: http://localhost:8080/django/"

echo "✅ Portfolio setup complete! Visit http://localhost:8080 to test."
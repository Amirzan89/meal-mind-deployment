#!/bin/bash

echo "🚀 Deploying Meal Mind Backend with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start the containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for the service to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 10

# Check if the service is healthy
echo "🔍 Checking service health..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend is running successfully!"
    echo "🌐 Backend API available at: http://localhost:5000"
    echo "🔍 Health check: http://localhost:5000/health"
    echo "📊 API test: http://localhost:5000/api/test"
else
    echo "❌ Backend is not responding. Checking logs..."
    docker-compose logs backend
fi

echo "📝 To view logs: docker-compose logs -f backend"
echo "🛑 To stop: docker-compose down" 
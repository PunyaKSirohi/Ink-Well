#!/bin/bash

# Production deployment script for InkWell

echo "🚀 Starting InkWell production deployment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🗄️ Starting database..."
docker-compose up -d db

echo "⏳ Waiting for database to be ready..."
sleep 30

echo "🔄 Running database migrations..."
docker-compose run --rm web python manage.py migrate

echo "📦 Collecting static files..."
docker-compose run --rm web python manage.py collectstatic --noinput

echo "👤 Creating superuser (if needed)..."
docker-compose run --rm web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "🚀 Starting all services..."
docker-compose up -d

echo "✅ Deployment completed!"
echo "🌐 Application is available at: http://localhost"
echo "⚙️ Admin panel is available at: http://localhost/admin"
echo ""
echo "📊 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down"

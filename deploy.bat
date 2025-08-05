@echo off
REM Production deployment script for InkWell (Windows)

echo 🚀 Starting InkWell production deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found. Please copy .env.example to .env and configure it.
    exit /b 1
)

REM Build and start services
echo 🔨 Building Docker images...
docker-compose build

echo 🗄️ Starting database...
docker-compose up -d db

echo ⏳ Waiting for database to be ready...
timeout /t 30 /nobreak

echo 🔄 Running database migrations...
docker-compose run --rm web python manage.py migrate

echo 📦 Collecting static files...
docker-compose run --rm web python manage.py collectstatic --noinput

echo 👤 Creating superuser (if needed)...
docker-compose run --rm web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(is_superuser=True).exists() else print('Superuser already exists')"

echo 🚀 Starting all services...
docker-compose up -d

echo ✅ Deployment completed!
echo 🌐 Application is available at: http://localhost
echo ⚙️ Admin panel is available at: http://localhost/admin
echo.
echo 📊 To view logs:
echo    docker-compose logs -f
echo.
echo 🛑 To stop services:
echo    docker-compose down

pause

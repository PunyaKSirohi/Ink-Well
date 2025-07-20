InkWell 🖋️InkWell is more than just a blog application; it's a comprehensive, hands-on project designed to demonstrate the end-to-end lifecycle of a modern web application. Built with Django, this project serves as a practical guide covering everything from initial setup and core development to professional practices like containerization, automated deployment (CI/CD), and long-term maintenance.The philosophy behind InkWell is to build software the right way—prioritizing best practices, scalability, and maintainability at every step. It's a living project that showcases a developer's ability to not only write code but to architect, deploy, and manage a production-ready application.✨ FeaturesInkWell is being built in phases, with a feature set that grows in complexity and sophistication over time.Current Features (Phase 1 & 2)Dynamic Post Management: Full CRUD (Create, Read, Update, Delete) functionality for blog posts.Powerful Admin Interface: A customized Django Admin panel for efficient content management, featuring search, filtering, and auto-populated slugs.Clean, SEO-Friendly URLs: Utilizes slugs for clear and readable post URLs (e.g., /my-first-post/).Published/Draft Status: Control the visibility of posts, allowing for drafts before publishing.(Coming Soon) Interactive Comment System.(Coming Soon) Full User Authentication (Registration, Login, Profiles).(Coming Soon) Frontend post creation and editing for authenticated users.Architectural & DevOps Features (Phase 3-5)Containerized Environment: Fully containerized with Docker and Docker Compose for consistent development and production environments.Production-Ready Database: Uses PostgreSQL for data integrity and scalability.Automated CI/CD Pipeline: GitHub Actions workflow for automated testing and deployment. Every push to the main branch triggers a new deployment.Comprehensive Testing: A suite of unit and integration tests to ensure code reliability.Monitoring & Maintenance: (Planned) Integration with logging and error monitoring services, plus an automated database backup strategy.🛠️ Tech StackThis project utilizes a modern, robust stack chosen for scalability and industry relevance.Backend: Django, Django REST Framework (for future API)Database: PostgreSQL (Production), SQLite3 (Development)Containerization: Docker, Docker ComposeCI/CD: GitHub ActionsServer: Gunicorn (WSGI Server)Testing: PytestFrontend: Django Templates, Bootstrap 5 (for styling)(Planned) Infrastructure: DigitalOcean/AWS, Nginx (Reverse Proxy)🚀 Getting StartedTo get a local copy up and running, follow these simple steps.PrerequisitesPython 3.8+Docker and Docker Compose (for containerized setup)1. Clone the Repositorygit clone https://github.com/your-username/inkwell.git
cd inkwell
2. Local Development (Virtual Environment)This method is ideal for theme development and simple debugging.# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser to access the admin panel
python manage.py createsuperuser

# Run the development server
python manage.py runserver
The application will be available at http://127.0.0.1:8000.The admin panel is at http://127.0.0.1:8000/admin/.3. Containerized Development (Docker)This is the recommended method as it perfectly mirrors the production environment.# Build and run the containers in detached mode
docker-compose up --build -d

# Apply database migrations (only need to do this the first time)
docker-compose exec web python manage.py migrate

# Create a superuser
docker-compose exec web python manage.py createsuperuser

# The application will be available at http://localhost:8000
To stop the services, run:docker-compose down
🗺️ Project RoadmapThis project is being developed in distinct phases. See the detailed Project Plan for more information.[x] Phase 0: The Blueprint - Environment & Project Setup[x] Phase 1: The Core Build - Models, Admin, Views, Templates[ ] Phase 2: Adding Features - Comments, Users, Frontend Forms, Tests[ ] Phase 3: Production Readiness - Docker, PostgreSQL[ ] Phase 4: Deployment & Automation - Cloud Deployment, CI/CD[ ] Phase 5: Maintenance & Monitoring - Logging, Error Tracking, Backups

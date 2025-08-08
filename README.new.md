# Inkwell - Django Blog Platform

A modern, feature-rich blog platform built with Django that allows users to create, publish, and manage blog posts with advanced commenting functionality.

## Features

- 📝 **Post Management**: Create, edit, and publish blog posts with rich content
- 🏷️ **Tagging System**: Organize posts with custom tags
- 💬 **Comment System**: Interactive commenting with moderation capabilities
- 👤 **User Authentication**: Secure user registration and login
- 🎨 **Admin Interface**: Powerful Django admin for content management
- 🔍 **Search Functionality**: Find posts by title, content, or tags
- 📱 **Responsive Design**: Mobile-friendly interface
- 🧪 **Comprehensive Testing**: Full test coverage with pytest
- 🚀 **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- 🐳 **Docker Support**: Containerized deployment

## Tech Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production)
- **Testing**: pytest, pytest-django, factory-boy
- **Code Quality**: Black, isort, flake8, mypy
- **Security**: Bandit, Safety
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Installation

### Prerequisites

- Python 3.11 or 3.12
- pip
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/PunyaKSirohi/Ink-Well.git
   cd Ink-Well
   ```

2. **Create virtual environment**
   ```bash
   python -m venv inkenv
   source inkenv/bin/activate  # On Windows: inkenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations in container**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser in container**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Usage

### Creating Posts

1. Log in to the admin interface at `/admin`
2. Navigate to Posts section
3. Click "Add Post" to create a new blog post
4. Fill in the title, content, tags, and publish status
5. Save to publish or save as draft

### Managing Comments

- Comments can be moderated through the admin interface
- Approve or disapprove comments in bulk
- View comment details and associated posts

### User Authentication

- Users can register and log in through the provided authentication views
- Password reset functionality included
- Secure session management

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with recent posts |
| GET | `/post/<slug>/` | Individual post detail |
| GET | `/admin/` | Django admin interface |
| POST | `/accounts/login/` | User login |
| POST | `/accounts/logout/` | User logout |
| POST | `/accounts/register/` | User registration |

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=blog --cov=inkwell --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

View coverage report in `htmlcov/index.html`.

## Code Quality

```bash
# Format code
black blog/ inkwell/ tests/

# Sort imports
isort blog/ inkwell/ tests/

# Lint code
flake8 blog/ inkwell/ tests/

# Type checking
mypy blog/ inkwell/

# Security checks
bandit -r blog/ inkwell/
safety check
```

## Deployment

### Production Environment

1. **Set environment variables**
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.com`
   - `DATABASE_URL=postgres://...`
   - `SECRET_KEY=your-secret-key`

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Deploy using Docker**
   ```bash
   docker-compose -f docker-compose.yml up --build -d
   ```

### CI/CD Pipeline

The project includes a GitHub Actions workflow that:
- Runs tests on Python 3.11 and 3.12
- Performs code quality checks
- Builds Docker images
- Deploys to production (when configured)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Project Structure

```
Inkwell/
├── blog/                   # Main blog application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Form definitions
│   └── templates/         # HTML templates
├── inkwell/               # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI configuration
├── tests/                 # Test files
├── templates/             # Global templates
├── static/               # Static files
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker configuration
└── manage.py            # Django management script
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/PunyaKSirohi/Ink-Well/issues) page
2. Create a new issue with detailed description
3. Contact the maintainer: [PunyaKSirohi](https://github.com/PunyaKSirohi)

## Acknowledgments

- Django community for the excellent framework
- Contributors and testers
- Open source libraries used in this project

---

Made with ❤️ by [Punya K Sirohi](https://github.com/PunyaKSirohi)

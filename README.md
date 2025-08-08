# Inkwell - Django Blog Platform

A simple and elegant blog platform built with Django.

## Features

- 📝 Create, edit, and publish blog posts
- 💬 Comment system with moderation
- 👤 User authentication and registration
- 🏷️ Tag posts for better organization
- 📱 Responsive design
- 🎨 Clean and modern interface

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PunyaKSirohi/Inkwell.git
   cd Inkwell
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser** to `http://127.0.0.1:8000`

## Using Docker (Alternative)

If you prefer using Docker:

```bash
# Clone and navigate to project
git clone https://github.com/PunyaKSirohi/Inkwell.git
cd Inkwell

# Run with Docker Compose
docker-compose up --build
```

Visit `http://localhost:8000` to access the application.

## Project Structure

```
Inkwell/
├── blog/              # Main blog application
├── inkwell/           # Django project settings
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── manage.py         # Django management script
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker configuration
└── docker-compose.yml # Docker Compose setup
```

## Usage

1. **Admin Panel**: Visit `/admin` to manage posts and users
2. **Create Posts**: Use the admin panel or create posts programmatically
3. **View Blog**: Navigate to the home page to see published posts
4. **Comments**: Users can comment on posts after registration

## Tech Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5
- **Containerization**: Docker

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ by [Punya K Sirohi](https://github.com/PunyaKSirohi)
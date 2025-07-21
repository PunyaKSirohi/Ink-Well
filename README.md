# 🖋️ InkWell

InkWell is more than just a blog app — it's a **hands-on blueprint** for architecting, deploying, and maintaining a modern web application using Django. Built with real-world practices in mind, it walks through everything from bare-metal setup to Dockerized environments and CI/CD automation.

---

## ✨ Key Features

Built in progressive phases to highlight real-world development practices:

### ✅ Phase 1–2: Core Functionality
- 📝 **Dynamic Post Management**: Full CRUD operations for blog entries.
- 🛠️ **Admin Panel**: Django Admin with slug auto-generation, search, and filtering.
- 🔗 **SEO-Friendly URLs**: Clean slugs (e.g. `/my-first-post/`).
- 📄 **Published/Draft Control**: Manage post visibility with simple status toggling.

### 🚧 Coming Soon
- 💬 Interactive comment system
- 👤 Full user authentication (register/login/profile)
- 🖊️ Frontend post creation & editing (auth-only)

### 🏗️ Phase 3–5: DevOps & Architecture
- 🐳 **Dockerized Environment**: Local + production-ready containers.
- 🛢️ **PostgreSQL**: Production-grade DB for performance and scale.
- ⚙️ **CI/CD Pipeline**: GitHub Actions for automated deployment + testing.
- 🧪 **Unit & Integration Testing**: Pytest suite planned.
- 📈 **Monitoring & Backup** _(planned)_: Logs, error tracking & DB snapshots.

---

## 🔧 Tech Stack

| Layer        | Tools                                         |
|--------------|-----------------------------------------------|
| **Backend**  | Django, Django REST Framework _(future API)_  |
| **Database** | SQLite (dev), PostgreSQL (prod)               |
| **Frontend** | Django Templates, Bootstrap 5                 |
| **DevOps**   | Docker, Docker Compose                        |
| **CI/CD**    | GitHub Actions                                |
| **Server**   | Gunicorn (WSGI)                               |
| **Infra (planned)** | DigitalOcean/AWS, Nginx              |

---

## 🚀 Getting Started

### 🔁 Local Development (Virtual Environment)

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install & migrate
pip install -r requirements.txt
python manage.py migrate

# Create admin
python manage.py createsuperuser

# Run server
python manage.py runserver

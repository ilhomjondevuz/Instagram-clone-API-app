# 📸 Instagram Clone app API

A RESTful API inspired by Instagram, built with **Django REST Framework**.

This project provides a backend API for an Instagram-like social media platform with user authentication, profiles, posts, likes, comments, followers/following and other social-media features.

## 🚀 Features

* 🔐 User registration and authentication
* 👤 User profiles
* 📝 Create, retrieve, update and delete posts
* ❤️ Like and unlike posts
* 💬 Comment on posts
* 👥 Follow and unfollow users
* 📰 User feed
* 🔍 Search users and posts
* 🖼️ Image upload support
* 🔑 Token/JWT authentication
* 📚 Swagger API documentation
* 📖 ReDoc API documentation
* 🛡️ Permission and authentication system
* 🗄️ PostgreSQL database support
* 🌍 Environment variable configuration

---

## 🛠️ Technologies

| Technology                 | Purpose                   |
| -------------------------- | ------------------------- |
| Python                     | Programming language      |
| Django                     | Web framework             |
| Django REST Framework      | REST API                  |
| PostgreSQL                 | Database                  |
| Pillow                     | Image processing          |
| drf-spectacular / Swagger  | API documentation         |
| JWT / Token Authentication | Authentication            |
| python-dotenv / environs   | Environment configuration |

---

# 📁 Project Structure

```text
instagram-clone/
│
├── apps/
│   ├── users/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── posts/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── comments/
│   ├── likes/
│   ├── follows/
│   └── ...
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── media/
├── static/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The exact application structure may differ depending on the current implementation.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/ilhomjondevuz/instagram-clone.git
```

```bash
cd instagram-clone
```

## 2. Create a virtual environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=instagram
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

If email functionality is enabled:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

> Never commit your `.env` file or secret credentials to GitHub.

---

# 🗄️ Database Setup

Create the database in PostgreSQL:

```sql
CREATE DATABASE instagram;
```

Then run Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 👨‍💻 Create Superuser

```bash
python manage.py createsuperuser
```

Enter:

```text
Username:
Email:
Password:
```

---

# ▶️ Run the Project

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Authentication

The API uses authentication to protect private endpoints.

After successful registration/login, include the authentication token in the request header:

```http
Authorization: Bearer <access_token>
```

Example:

```http
GET /api/v1/posts/

Authorization: Bearer eyJhbGciOi...
```

---

# 👤 User API

## Register

```http
POST /api/v1/auth/register/
```

Example:

```json
{
    "username": "ilhomjon",
    "email": "ilhomjon@example.com",
    "password": "StrongPassword123!",
    "password2": "StrongPassword123!"
}
```

## Login

```http
POST /api/v1/auth/login/
```

Example:

```json
{
    "username": "ilhomjon",
    "password": "StrongPassword123!"
}
```

## Get Profile

```http
GET /api/v1/users/<username>/
```

## Update Profile

```http
PATCH /api/v1/users/profile/
```

---

# 📝 Posts API

Users can create and manage their posts.

## Create Post

```http
POST /api/v1/posts/
```

Example:

```json
{
    "caption": "Beautiful day ☀️"
}
```

With an image:

```text
multipart/form-data
```

```text
image: photo.jpg
caption: Beautiful day!
```

## Get Posts

```http
GET /api/v1/posts/
```

## Get Single Post

```http
GET /api/v1/posts/<id>/
```

## Update Post

```http
PATCH /api/v1/posts/<id>/
```

## Delete Post

```http
DELETE /api/v1/posts/<id>/
```

---

# ❤️ Likes

Users can like and unlike posts.

## Like Post

```http
POST /api/v1/posts/<id>/like/
```

## Unlike Post

```http
DELETE /api/v1/posts/<id>/like/
```

Example response:

```json
{
    "message": "Post liked successfully."
}
```

---

# 💬 Comments

Users can comment on posts.

## Create Comment

```http
POST /api/v1/posts/<id>/comments/
```

Example:

```json
{
    "content": "Great photo! 🔥"
}
```

## Get Comments

```http
GET /api/v1/posts/<id>/comments/
```

## Update Comment

```http
PATCH /api/v1/comments/<id>/
```

## Delete Comment

```http
DELETE /api/v1/comments/<id>/
```

---

# 👥 Follow System

Users can follow and unfollow other users.

## Follow User

```http
POST /api/v1/users/<username>/follow/
```

## Unfollow User

```http
DELETE /api/v1/users/<username>/follow/
```

## Followers

```http
GET /api/v1/users/<username>/followers/
```

## Following

```http
GET /api/v1/users/<username>/following/
```

---

# 📰 Feed

The feed contains posts from users that the authenticated user follows.

```http
GET /api/v1/feed/
```

Example response:

```json
[
    {
        "id": 1,
        "author": {
            "username": "ilhomjon"
        },
        "image": "/media/posts/photo.jpg",
        "caption": "Hello Instagram!",
        "likes_count": 15,
        "comments_count": 4,
        "created_at": "2026-08-10T12:30:00Z"
    }
]
```

---

# 🔍 Search

Users can search for other users.

```http
GET /api/v1/users/?search=ilhomjon
```

Example:

```text
/api/v1/users/?search=python
```

Depending on the implementation, post search can also be supported:

```text
/api/v1/posts/?search=django
```

---

# 📚 API Documentation

Interactive API documentation is available through Swagger and ReDoc.

## Swagger

```text
http://127.0.0.1:8000/api/docs/
```

## ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

The documentation allows you to:

* View available endpoints
* Test API requests
* View request parameters
* View response schemas
* Authorize requests
* Test authenticated endpoints

---

# 🖼️ Media Files

Uploaded images are stored in the media directory:

```text
media/
└── posts/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

Development configuration:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

# 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

For a specific application:

```bash
python manage.py test apps.users
```

---

# 🛠️ Useful Django Commands

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run development server:

```bash
python manage.py runserver
```

Check the project:

```bash
python manage.py check
```

Collect static files:

```bash
python manage.py collectstatic
```

---

# 🔒 Production Checklist

Before deploying the API to production:

* Set `DEBUG=False`
* Use a strong `SECRET_KEY`
* Configure `ALLOWED_HOSTS`
* Use PostgreSQL
* Configure HTTPS
* Protect secret environment variables
* Configure secure cookies
* Configure CORS properly
* Configure CSRF protection
* Configure static and media storage
* Use Gunicorn/Uvicorn
* Configure a reverse proxy such as Nginx
* Run Django deployment checks

```bash
python manage.py check --deploy
```

---

# 🚧 Future Improvements

Possible future features:

* 📱 Stories
* 🎥 Reels
* 💬 Direct Messages
* 🔔 Notifications
* 🔖 Saved posts
* 📍 Post locations
* #️⃣ Hashtags
* 🔎 Advanced search
* 📊 User statistics
* 📨 Email verification
* 🔑 Password reset
* 🔐 Two-factor authentication
* ☁️ Cloud image storage
* ⚡ Redis caching
* 🐳 Docker support
* 🚀 CI/CD pipeline

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add new feature"
```

5. Push the branch

```bash
git push origin feature/new-feature
```

6. Create a Pull Request

---

# 👨‍💻 Author

**Ilhomjon**

GitHub:
https://github.com/ilhomjondevuz

---

# 📄 License

This project is licensed under the **MIT License**.

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

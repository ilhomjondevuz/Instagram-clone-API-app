# 📸 Instagram Clone API

A feature-rich Instagram-inspired REST API built with **Django**, **Django REST Framework**, **PostgreSQL**, **JWT Authentication**, **Django Channels**, and **Redis**.

The project provides a backend for a social media platform with authentication, user profiles, posts, likes, comments, follow/unfollow functionality, feeds, search, notifications, and saved posts.

---

## 🚀 Features

### 🔐 Authentication & Account Management

* User registration
* Email / phone number based registration
* Account verification
* Verification code resend
* JWT authentication
* Access and refresh tokens
* Token refresh
* Token verification
* Logout
* Forgot password
* Reset password
* Update account information
* Update profile avatar
* Get current authenticated user

### 👤 User & Social Features

* User profiles
* View another user's profile
* Follow users
* Unfollow users
* Followers list
* Following list
* Personalized home feed

### 📝 Posts

* Create posts
* Retrieve posts
* Retrieve a single post
* Update posts
* Delete posts
* Image upload
* Post captions
* Post likes count
* Comment count
* Check whether the current user liked a post
* Display latest post comment

### ❤️ Likes

* Like posts
* Unlike posts
* Get post likes
* Like/unlike comments
* Get comment likes

### 💬 Comments

* Create comments
* Retrieve comments
* Update comments
* Delete comments
* Nested/reply comments
* Like comments
* Retrieve comment likes

### 🔔 Notifications

* User notifications
* Read notifications
* Unread notifications
* Mark notification as read
* Notification history
* Notification types for social interactions
* Real-time notification infrastructure using Django Channels and Redis

### 🔖 Saved Posts

* Save posts
* View saved posts
* Prevent duplicate saved posts per user/post pair

### 🔍 Search

* Search posts
* Search functionality through query parameters

### 📚 API Documentation

* OpenAPI schema
* Swagger UI
* ReDoc
* Interactive API testing

---

# 🛠️ Technology Stack

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| Python 3.12           | Programming language                |
| Django 6.1            | Backend framework                   |
| Django REST Framework | REST API                            |
| PostgreSQL            | Relational database                 |
| SimpleJWT             | JWT authentication                  |
| Django Channels       | WebSocket / real-time communication |
| Redis                 | Channel layer / real-time messaging |
| drf-spectacular       | OpenAPI / Swagger / ReDoc           |
| Pillow                | Image processing                    |
| django-filter         | Filtering                           |
| environs              | Environment variables               |
| WhiteNoise            | Static file serving                 |
| Gunicorn              | Production WSGI server              |
| Uvicorn               | ASGI server                         |
| Twilio                | SMS integration                     |
| environs              | Environment configuration           |

---

# 📁 Project Structure

```text
Instagram-clone-API-app/
│
├── apps/
│   │
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── home/
│   │   └── ...
│   │
│   ├── post/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── social/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── notification/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── savedpost/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   └── shared/
│       └── ...
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│
├── media/
│
├── static/
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/ilhomjondevuz/Instagram-clone-API-app.git
cd Instagram-clone-API-app
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

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=instagram_clone_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password

TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-account-auth-token
TWILIO_NUMBER=yout-phone-number

DJANGO_SETTINGS_MODULE=core.settings
```

> ⚠️ Never commit `.env` or secret credentials to GitHub.

Add `.env` to `.gitignore`.

---

# 🗄️ PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE instagram_clone_db;
```

Configure the database credentials in `.env`.

Then run:

 python manage.py migrate

---

# 👨‍💻 Create Superuser

```bash
python manage.py createsuperuser
```

Then enter:

```text
Username:
Email:
Password:
```

---

# ▶️ Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

# 🔑 Authentication

The API uses **JWT authentication**.

After login, use the access token in the request header:

```http
Authorization: Bearer <access_token>
```

Example:

```http
GET /api/posts/all/
Authorization: Bearer eyJhbGciOi...
```

The project uses:

* Access Token
* Refresh Token
* Token Refresh
* Token Verification
* Token Blacklisting / Logout

---

# 👤 Accounts API

Base URL:

```text
/api/accounts/
```

## Register

```http
POST /api/accounts/signup/
```

Example:

```json
{
    "phone_number_or_email": "user@example.com"
}
```

The registration flow determines whether the identifier is an email address or phone number and generates a verification code.

---

## Verify Account

```http
POST /api/accounts/verify/
```

Example:

```json
{
    "code": "1234"
}
```

---

## Send Verification Code Again

```http
POST /api/accounts/send-again-verify-code/
```

---

## Login

```http
POST /api/accounts/login/
```

Login supports username, email, or phone number depending on the authentication flow.

Example:

```json
{
    "user_input": "username",
    "password": "your-password"
}
```

---

## Refresh Token

```http
POST /api/accounts/login/refresh/
```

---

## Logout

```http
POST /api/accounts/logout/
```

Example:

```json
{
    "refresh": "<refresh_token>"
}
```

---

## Forgot Password

```http
POST /api/accounts/forgot-password/
```

---

## Reset Password

```http
POST /api/accounts/reset-password/
```

---

## Get Current User

```http
GET /api/accounts/get-me/
```

Requires authentication.

---

## Update User

```http
PATCH /api/accounts/update/
```

---

## Change User Information

```http
PATCH /api/accounts/change-user-information/
```

---

## Change Avatar

```http
PATCH /api/accounts/change-user-avatar/
```

Use:

```text
multipart/form-data
```

Example:

```text
avatar: profile.jpg
```

---

# 📝 Posts API

Base URL:

```text
/api/posts/
```

## Get All Posts

```http
GET /api/posts/all/
```

---

## Create Post

```http
POST /api/posts/create/
```

Use:

```text
multipart/form-data
```

Example:

```text
photo: image.jpg
caption: Beautiful day!
```

---

## Retrieve Single Post

```http
GET /api/posts/<uuid>/
```

---

## Update Post

```http
PATCH /api/posts/<uuid>/
```

---

## Delete Post

```http
DELETE /api/posts/<uuid>/
```

---

# ❤️ Post Likes

## Get Post Likes

```http
GET /api/posts/<uuid>/likes/
```

---

## Toggle Post Like

```http
POST /api/posts/<uuid>/toggle-like/
```

This endpoint handles the like/unlike behavior.

---

# 💬 Comments

## Get Post Comments

```http
GET /api/posts/<uuid>/comments/
```

---

## Create Comment

```http
POST /api/posts/<uuid>/comments/create/
```

Example:

```json
{
    "comment": "Great post! 🔥"
}
```

---

## Retrieve / Update / Delete Comment

```http
GET /api/posts/comments/<comment_uuid>/
PATCH /api/posts/comments/<comment_uuid>/
DELETE /api/posts/comments/<comment_uuid>/
```

---

# ❤️ Comment Likes

## Get Comment Likes

```http
GET /api/posts/comments/<comment_uuid>/likes/
```

---

## Toggle Comment Like

```http
POST /api/posts/comments/<comment_uuid>/toggle-like/
```

---

# 👥 Social / Follow API

Base URL:

```text
/api/social/
```

## Follow / Unfollow

```http
POST /api/social/follow/
```

The endpoint handles the follow relationship for the authenticated user.

---

## Following List

```http
GET /api/social/followings/list/
```

---

## Followers List

```http
GET /api/social/followers/list/
```

---

## Get Another User

```http
GET /api/social/user/<uuid>/
```

---

# 📰 Home Feed

```http
GET /api/social/feeds/
```

The feed returns posts related to the authenticated user's social graph.

Typical post information includes:

```json
{
    "id": "uuid",
    "author": {
        "id": "uuid",
        "username": "username"
    },
    "photo": "/media/posts/photo.jpg",
    "caption": "Hello Instagram!",
    "post_likes_count": 15,
    "comments_count": 4,
    "me_like": true,
    "post_comments": []
}
```

---

# 🔍 Post Search

```http
GET /api/posts/search/?q=django
```

Example:

```text
/api/posts/search/?q=python
```

The search endpoint accepts a query parameter and returns matching posts according to the implemented search logic.

---

# 🔔 Notifications

Base URL:

```text
/api/notifications/
```

## My Notifications

```http
GET /api/notifications/my-list/
```

---

## Read Notifications

```http
GET /api/notifications/my-list/read/
```

---

## Unread Notifications

```http
GET /api/notifications/my-list/unread/
```

---

## Mark Notification as Read

```http
PUT /api/notifications/<uuid>/read/
```

---

## Reading Unread Notifications

```http
GET /api/notifications/my-list/unread/reading/
```

---

# ⚡ Real-Time Notifications

The project includes infrastructure for real-time communication using:

* Django Channels
* WebSockets
* Redis
* ASGI

The Django settings configure Channels as the ASGI application and Redis as the channel layer.

Redis should be running locally:

```bash
redis-server
```

The default Redis configuration uses:

```text
127.0.0.1:6379
```

For production, use a managed Redis instance or a dedicated Redis server.

---

# 🔖 Saved Posts

Base URL:

```text
/api/saved_posts/
```

## Save a Post

```http
POST /api/saved_posts/create/
```

Example:

```json
{
    "post": "<post_uuid>"
}
```

The authenticated user is automatically associated with the saved post.

---

## My Saved Posts

```http
GET /api/saved_posts/my-list/
```

Saved posts are associated with the authenticated user.

The database prevents the same user from saving the same post more than once.

---

# 📚 API Documentation

The project uses **drf-spectacular** for OpenAPI schema generation and interactive API documentation.

## OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

## Swagger UI

```text
http://127.0.0.1:8000/api/docs/swagger/
```

## ReDoc

```text
http://127.0.0.1:8000/api/docs/redoc/
```

Swagger/ReDoc can be used to:

* Explore API endpoints
* Inspect request schemas
* Inspect response schemas
* Test endpoints
* Authorize JWT requests
* Test authenticated APIs

---

# 🖼️ Media Files

Uploaded images are stored under the media directory.

Example:

```text
media/
└── posts/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

Development settings:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

# 📦 Static Files

The project uses Django static files together with WhiteNoise.

Collect static files with:

```bash
python manage.py collectstatic
```

---

# 🧪 Testing

Run the complete test suite:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test apps.accounts
```

```bash
python manage.py test apps.post
```

```bash
python manage.py test apps.social
```

```bash
python manage.py test apps.notification
```

---

# 🛠️ Useful Django Commands

### Check project

```bash
python manage.py check
```

### Check deployment configuration

```bash
python manage.py check --deploy
```

### Create migrations

```bash
python manage.py makemigrations
```

### Apply migrations

```bash
python manage.py migrate
```

### Create superuser

```bash
python manage.py createsuperuser
```

### Run server

```bash
python manage.py runserver
```

### Collect static files

```bash
python manage.py collectstatic
```

---

# 🌿 Git Workflow

The project uses feature branches for development.

Create a new feature branch:

```bash
git switch -c future/new-feature
```

Example:

```bash
git switch -c future/savedpost
```

Check the current branch:

```bash
git branch
```

Stage changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Add saved posts feature"
```

Push:

```bash
git push -u origin future/savedpost
```

Merge a feature branch into `master`:

```bash
git switch master
git pull origin master
git merge future/new-feature
git push origin master
```

---

# 🔒 Security

Before deploying to production:

* Set `DEBUG=False`
* Use a strong `SECRET_KEY`
* Configure `ALLOWED_HOSTS`
* Never commit `.env`
* Never expose database passwords
* Never expose JWT secrets
* Use HTTPS
* Configure CORS correctly
* Configure CSRF protection where applicable
* Use secure cookies where applicable
* Protect media and static infrastructure
* Use a production-grade PostgreSQL database
* Use a production Redis instance
* Run:

```bash
python manage.py check --deploy
```

---

# 🚀 Production Deployment

For production, the application can be served through an ASGI/WSGI stack.

Recommended components:

```text
                    ┌─────────────┐
                    │   Nginx     │
                    └──────┬──────┘
                           │
                  ┌────────┴────────┐
                  │                 │
             HTTP/API          WebSocket
                  │                 │
                  ↓                 ↓
             Django/DRF         Uvicorn
                  │                 │
                  └────────┬────────┘
                           │
                    ┌──────┴──────┐
                    │ PostgreSQL  │
                    │    Redis    │
                    └─────────────┘
```

Possible production stack:

* Nginx
* Uvicorn
* Gunicorn
* PostgreSQL
* Redis
* Django Channels
* HTTPS / SSL

---

# 🧩 Application Architecture

```text
                    Instagram Clone API
                            │
             ┌──────────────┼──────────────┐
             │              │              │
         Accounts          Posts          Social
             │              │              │
      Authentication      Likes         Follow
      Verification        Comments      Followers
      JWT                  Search        Following
      Password             Images        Feed
             │              │              │
             └──────────────┼──────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Notifications                Saved Posts
              │                           │
        REST + WebSocket                  │
              │                           │
             Redis                    PostgreSQL
```

---

# 📡 API Flow

A typical user flow:

```text
1. Signup
   ↓
2. Email / Phone Verification
   ↓
3. Login
   ↓
4. Receive JWT Access + Refresh Tokens
   ↓
5. Update Profile
   ↓
6. Follow Users
   ↓
7. View Feed
   ↓
8. Create Posts
   ↓
9. Like / Comment
   ↓
10. Receive Notifications
   ↓
11. Save Posts
   ↓
12. Search Posts
```

---

# 📌 API Endpoint Summary

| Method | Endpoint                                     | Description               |
| ------ | -------------------------------------------- | ------------------------- |
| POST   | `/api/accounts/signup/`                      | Register user             |
| POST   | `/api/accounts/verify/`                      | Verify account            |
| POST   | `/api/accounts/send-again-verify-code/`      | Resend verification code  |
| POST   | `/api/accounts/login/`                       | Login                     |
| POST   | `/api/accounts/login/refresh/`               | Refresh JWT               |
| POST   | `/api/accounts/logout/`                      | Logout                    |
| POST   | `/api/accounts/forgot-password/`             | Forgot password           |
| POST   | `/api/accounts/reset-password/`              | Reset password            |
| GET    | `/api/accounts/get-me/`                      | Current user              |
| PATCH  | `/api/accounts/update/`                      | Update user               |
| PATCH  | `/api/accounts/change-user-information/`     | Change information        |
| PATCH  | `/api/accounts/change-user-avatar/`          | Change avatar             |
| GET    | `/api/posts/all/`                            | List posts                |
| POST   | `/api/posts/create/`                         | Create post               |
| GET    | `/api/posts/<uuid>/`                         | Retrieve post             |
| PATCH  | `/api/posts/<uuid>/`                         | Update post               |
| DELETE | `/api/posts/<uuid>/`                         | Delete post               |
| GET    | `/api/posts/<uuid>/comments/`                | List comments             |
| POST   | `/api/posts/<uuid>/comments/create/`         | Create comment            |
| GET    | `/api/posts/<uuid>/likes/`                   | List post likes           |
| POST   | `/api/posts/<uuid>/toggle-like/`             | Toggle post like          |
| GET    | `/api/posts/comments/<uuid>/likes/`          | List comment likes        |
| POST   | `/api/posts/comments/<uuid>/toggle-like/`    | Toggle comment like       |
| GET    | `/api/posts/search/`                         | Search posts              |
| POST   | `/api/social/follow/`                        | Follow / unfollow         |
| GET    | `/api/social/followings/list/`               | Following list            |
| GET    | `/api/social/followers/list/`                | Followers list            |
| GET    | `/api/social/user/<uuid>/`                   | Other user profile        |
| GET    | `/api/social/feeds/`                         | Home feed                 |
| GET    | `/api/notifications/my-list/`                | Notifications             |
| GET    | `/api/notifications/my-list/read/`           | Read notifications        |
| GET    | `/api/notifications/my-list/unread/`         | Unread notifications      |
| PUT    | `/api/notifications/<uuid>/read/`            | Mark notification read    |
| GET    | `/api/notifications/my-list/unread/reading/` | Read unread notifications |
| POST   | `/api/saved_posts/create/`                   | Save post                 |
| GET    | `/api/saved_posts/my-list/`                  | My saved posts            |
| POST   | `/api/token/`                                | Obtain JWT                |
| POST   | `/api/token/refresh/`                        | Refresh JWT               |
| POST   | `/api/token/verify/`                         | Verify JWT                |

---

# 🧑‍💻 Development

The project is structured as a modular Django application.

Each major domain has its own Django app:

```text
accounts       → Authentication and users
post           → Posts, comments and likes
social         → Follow, followers, following and feed
notification   → User notifications
savedpost      → Saved posts
home           → Home-related functionality
shared         → Shared utilities and base functionality
```

This structure keeps business logic separated and makes the application easier to maintain and extend.

---

# 🚧 Future Improvements

Possible future improvements:

* 📱 Stories
* 🎥 Reels
* 💬 Direct Messages
* 🔔 Advanced real-time notifications
* 📍 Post locations
* #️⃣ Hashtags
* 🔎 Advanced search
* 📊 User statistics
* ☁️ Cloud media storage
* ⚡ Redis caching
* 🐳 Docker / Docker Compose
* 🚀 CI/CD pipeline
* 📱 Push notifications
* 🧪 Expanded automated test coverage
* 📈 API performance optimization
* 🔐 Two-factor authentication
* 🛡️ Rate limiting
* 📄 Advanced API pagination and filtering

---

# 🤝 Contributing

Contributions, issues and suggestions are welcome.

### 1. Fork the repository

### 2. Clone your fork

```bash
git clone https://github.com/ilhomjondevuz/Instagram-clone-API-app
```

### 3. Create a feature branch

```bash
git switch -c feature/new-feature
```

### 4. Make your changes

### 5. Commit

```bash
git add .
git commit -m "Add new feature"
```

### 6. Push

```bash
git push -u origin feature/new-feature
```

### 7. Open a Pull Request

---

# 👨‍💻 Author

**Ilhomjon**

Python Backend Developer

GitHub:
https://github.com/ilhomjondevuz

---

# 📄 License

This project is licensed under the **MIT License**.

---

# ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

If you have suggestions or find a bug, feel free to open an issue.

---

## 🔗 Repository

https://github.com/ilhomjondevuz/Instagram-clone-API-app

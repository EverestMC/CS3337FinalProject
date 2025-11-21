# BookEx – CS 3337 Final Project

A simple book logging web app built with **Django 5.2.5**.  
This README explains exactly how to clone, set up, and run the project across Windows, macOS, and Linux. It also lists new features added (Ratings ⭐, Favorites ❤️, About page), required dependencies, and common troubleshooting steps.

---

## ✨ What’s new (compared to earlier versions)
- **Ratings (1–5 stars)** per user, per book.
- **Favorites** toggle for each book + a **Favorites** list view.
- **About Us** static page.
- Template updates for clean cards, rating display, and favorite buttons.
- Admin now exposes **Books, Comments, Ratings, MainMenu**.
- **Media settings** added so uploaded images work in development:
  - `MEDIA_URL = '/media/'` and `MEDIA_ROOT = BASE_DIR / 'media'`
  - Dev URLs serve media when `DEBUG=True`

> These changes are already integrated, but steps below explain how to prepare your local environment so everything "just works".

---

## 🧰 Requirements
- **Python 3.10+ (3.13 tested)**  
- **Pip** (Python package manager)  
- **Git** (to clone the repo)  
- (Windows) **Visual C++ Build Tools** are _not_ required for our dependency set.
- **No database server needed** — Django’s default SQLite is used.

### Python packages (installed automatically via `requirements.txt`)
- `Django==5.2.5`
- `Pillow>=10.0` (required for `ImageField`)
- `asgiref>=3.7`, `sqlparse>=0.5`, `tzdata>=2023.3`

> If `pip install -r requirements.txt` fails, see **Troubleshooting** at the bottom.

---

## 🧪 Quick Start (works on all platforms)

```bash
# 1) Clone the repo
git clone <YOUR_REPO_URL>.git
cd <REPO_FOLDER>/bookEx

# 2) (Recommended) Create a virtual environment
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4) Set up the database
python manage.py makemigrations
python manage.py migrate

# 5) Create a superuser (admin)
python manage.py createsuperuser

# 6) Run the development server
python manage.py runserver

# 7) Visit the app
# Site: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
```

---

## 🗂 Project Structure (important parts)
```
bookEx/
├── manage.py
├── bookEx/                  # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── templates/
│       └── base.html
├── bookMng/                 # App code
│   ├── models.py            # Book, Comment, Rating, MainMenu
│   ├── views.py             # ratings, favorites, comments, CRUD
│   ├── urls.py
│   ├── forms.py             # BookForm, RatingForm, CommentForm
│   └── templates/bookMng/   # index, displaybooks, book_detail, etc.
└── media/                   # (created on first upload) user images live here
```

---

## 🖼 Media / Image uploads (dev setup)
These are already in the codebase, but verify if needed:

**`bookEx/bookEx/settings.py`**
```python
from pathlib import Path
MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR) / 'media'
```

**`bookEx/bookEx/urls.py`**
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing URL patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Create the folder if missing:
```
bookEx/media/
```

---

## 🧾 New features – how they work

### 1) Ratings (1–5 stars)
- A user can rate a book once; updates overwrite the previous score.
- Average rating and rating count are displayed in list and detail views.
- Backed by a `Rating` model with `unique_together = ('user', 'book')`.

### 2) Favorites
- Click the heart to toggle a book as favorite.
- Use the **Show Favorites** button on the list page to filter favorites.

### 3) Admin
- Visit `/admin/` and sign in with your superuser.
- You’ll see **Books**, **Comments**, **Ratings**, **MainMenu**.

---

## 🛠 Commands you’ll use often
```bash
# Start server
python manage.py runserver

# Make & apply migrations (after model changes)
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect all installed packages (not usually required; our requirements.txt is minimal)
pip freeze > requirements.txt
```

---

## 🔁 Upgrading from an older local DB
If you already had this project and pull updates:
```bash
git pull
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
If prompted during migrations to provide a default for a new `DateTimeField` (e.g., `created_at`), choose:
- **Option 1**: Provide a one-off default  
- Enter: `timezone.now` (exactly like that, without parentheses)

---

## 🧩 Notes for Windows
If you see:  
`Cannot use ImageField because Pillow is not installed.`

Install Pillow for the exact interpreter running Django:
```bat
python -m pip install --upgrade pip
python -m pip install --only-binary=:all: Pillow
# Verify
python -c "from PIL import Image; print(Image.__version__)"
```

If you have multiple Pythons, explicitly call the path you use to run the server:
```bat
"C:\Path\to\python3.13.exe" -m pip install --only-binary=:all: Pillow
"C:\Path\to\python3.13.exe" manage.py runserver
```

---

## 🧰 Optional: Conda users
We recommend **venv + pip**, but if you’re using Conda, keep the project’s `requirements.txt` minimal and create your env like this:
```bash
conda create -n bookex python=3.11
conda activate bookex
pip install -r requirements.txt
python manage.py runserver
```

---

## 🧨 Troubleshooting

### 1) Pillow / ImageField error
```
bookMng.Book.picture: (fields.E210) Cannot use ImageField because Pillow is not installed.
```
**Fix:**
```bash
pip install --only-binary=:all: Pillow
```
Make sure you install it in the **same environment** used to run `manage.py`.

### 2) Migration prompt for `auto_now_add`
When adding `created_at` to existing models, Django may ask for a default during migration.
**Choose Option 1** (one-off default) and type:  
```
timezone.now
```

### 3) Media not loading
- Ensure `MEDIA_URL` and `MEDIA_ROOT` are in `settings.py` (see section above).
- Ensure dev URLs include `urlpatterns += static(...)`.
- Ensure your images exist under `bookEx/media/` and your template uses `{{ book.picture.url }}` (with `{% load static %}` at top).

### 4) Wrong Python
If `pip install` succeeded but `runserver` still errors with missing packages, you’re likely using a **different Python**.
Check:
```bash
where python        # Windows
which python        # macOS/Linux
python -c "import sys; print(sys.executable)"
```

### 5) Admin login / superuser
If you forgot your admin credentials, create a new one:
```bash
python manage.py createsuperuser
```

---

## 📦 Minimal `requirements.txt`
Your repo includes a slim, portable `requirements.txt` suitable for all classmates:
```
Django==5.2.5
Pillow>=10.0
asgiref>=3.7
sqlparse>=0.5
tzdata>=2023.3
```
Avoid exporting Anaconda’s full package list to `requirements.txt` (those `@ file:///...` entries will break installs).

---

## ✅ Done!
- Visit `http://127.0.0.1:8000/` to use the app.
- Visit `http://127.0.0.1:8000/admin/` to manage content.
- Reach out if anything fails; include your OS, Python version, and the error message.

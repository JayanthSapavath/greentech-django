# GreenTechProject

A Django web application for green/environment-friendly technologies.

## Features
- 10 models, 10 forms, 10 templates, 10 views
- User authentication (login, logout, registration, password reset)
- Different interfaces for registered/unregistered users
- Search bar with dropdown
- User history tracking (sessions/cookies)
- File upload
- Bootstrap styling
- About, Contact, Team, and more

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser (optional, for admin):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the site:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## PyCharm Compatibility
- Open this directory in PyCharm as a Django project.
- Mark the root as "Sources Root" if needed.
- Use PyCharm's Django support for running, debugging, and managing the project.

## Notes
- Static files are in `static/`, templates in `templates/greentech/`.
- Media uploads go to `media/`.
- To load initial data, use Django fixtures (see docs).

---

For any issues, contact the project maintainer. 
# Workshop AI

A Django-based website for managing and publishing practical AI workshops by **Indonesia AI (PT. Teknologi Artifisial Indonesia)**. The platform is designed to make it easy to create, update, archive, and reuse workshop pages through Django Admin without building a new page for every event.

## Features

- Dynamic workshop pages powered by Django
- Django Admin for managing workshops, mentors, schedules, benefits, FAQs, and testimonials
- Five reusable workshop layouts: Editorial, Workflow, Dashboard, Showcase, and Guide
- Automatic handling of upcoming and past workshops
- Registration CTA for active workshops
- Recording request CTA for past workshops
- Responsive design for desktop, tablet, and mobile

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Django Admin

Create an admin account:

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## License

This project is developed for Workshop AI by Indonesia AI.

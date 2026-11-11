# AI untuk Semua — Learning Platform

A simple Django learning platform by **Indonesia AI (PT. Teknologi Artifisial Indonesia)**, with two sections: **Courses** and **Workshop**.

## Pages

| Path | Description |
| --- | --- |
| `/` | Learning Platform homepage |
| `/courses/` | Online course catalog |
| `/courses/<slug>/` | Course details |
| `/workshop/` | Featured workshop landing page (previously `/`) |
| `/workshop/<slug>/` | Workshop details |
| `/workshops/` | All workshops (existing catalog) |
| `/admin-courses/` | Courses administration |
| `/admin-workshop/` | Workshop administration |

The original `/admin/` still works for backward compatibility.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` instead.

Open **http://127.0.0.1:8000/**. To create an administrator account:

```bash
python manage.py createsuperuser
```

## Managing Content

- **Courses:** Add, edit, and publish course information at `/admin-courses/`.
- **Workshop:** Manage existing workshops, mentors, testimonials, and workshop layouts at `/admin-workshop/`.

Three example courses are included as **Coming Soon** placeholders and can be edited or unpublished in Courses Admin.

This first version provides course listings and detail pages only. Lesson playback, accounts, enrollment, and payments are **not implemented**. The existing workshop landing pages and their five layout variants are preserved.

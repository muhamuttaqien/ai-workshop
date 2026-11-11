# Indonesia AI — Learning Platform

A simple Django learning platform by **Indonesia AI (PT. Teknologi Artifisial Indonesia)**, with two sections: **Courses** and **Workshop**.

## Pages

| Path | Description |
| --- | --- |
| `/` | Learning Platform homepage |
| `/courses/` | Online course catalog |
| `/courses/<slug>/` | Course details and lesson syllabus |
| `/courses/<slug>/lessons/<slug>/` | Lesson reader with video, explanation and quiz |
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

Five example courses are included. Each has **two introductory lessons** with explanation text and a sample quiz. All can be edited or unpublished.

### Managing lessons and quizzes

1. Open `/admin-courses/` and choose **Lessons** to edit a lesson. You can also see lessons linked from each Course.
2. Edit **Content** for the written explanation below the video.
3. To embed a video, fill **YouTube Video ID** with the 11-character ID from your YouTube URL; leave it blank to show a clear "video being prepared" placeholder. No third-party example video is embedded by default.
4. Add one or more **Quiz Questions** inside the Lesson editor. Each question has four answers, one correct option and an optional explanation.
5. Publish the Lesson to show it publicly; draft lessons are hidden. The Course must also be published.

The quiz checks answers on the server and displays the score and explanations. **No accounts, enrollment, persisted learning progress or payments are implemented yet.** Workshop pages and their five layout variants are unchanged. The Courses light/dark switch does not affect Workshop.

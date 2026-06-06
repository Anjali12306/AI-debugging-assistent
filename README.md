# AI Debugging Assistant

AI Debugging Assistant is a Flask-based web application that helps users debug code with AI-generated explanations, code fixes, optimization suggestions, and time complexity insights. The project now includes PostgreSQL-backed authentication, per-user analysis history, multi-language selection, and OpenAI-backed structured output.

## Features

- User signup and login with hashed passwords
- PostgreSQL database for users and analysis history
- OpenAI-powered code analysis with structured output
- Multi-language input support for Python, C, C++, Java, and JavaScript
- Optimized long-code mode for larger submissions
- Smart fallback analyzer if the live AI request fails
- Saved per-user debugging history
- Presentation-ready interface with sample snippets and copyable fixed code

## Tech Stack

- Python
- Flask
- PostgreSQL
- OpenAI API
- HTML, CSS, JavaScript

## Folder Structure

- `backend/routes/` handles auth, main routes, and history pages
- `backend/services/` contains OpenAI integration, PostgreSQL access, auth logic, and history saving
- `templates/` contains frontend pages
- `static/` contains styling and JavaScript
- `docs/` contains project report, PPT outline, viva notes, and deployment notes

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.4-mini
OPENAI_TIMEOUT=45
OPENAI_MAX_RETRIES=2
OPENAI_MAX_OUTPUT_TOKENS=450
SECRET_KEY=change-me
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

## Database

The project uses PostgreSQL through the `DATABASE_URL` environment variable. It stores:

- `users`
- `analysis_history`

The history table now tracks:

- selected language
- analysis mode
- structured AI/fallback response

## Deployment

This project includes:

- `Procfile`
- `render.yaml`
- `gunicorn` in `requirements.txt`

These files prepare the app for deployment on Render or similar Python hosting platforms.

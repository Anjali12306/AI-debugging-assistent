# Deployment Guide

## Recommended Platform

Render is a simple deployment option for this Flask project.

## Steps

1. Push the project to GitHub
2. Create a new Web Service on Render
3. Connect your repository
4. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Create a PostgreSQL database on Render or another provider and copy its connection string.
6. Add environment variables in Render:
   - `DATABASE_URL`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
   - `OPENAI_TIMEOUT`
   - `OPENAI_MAX_RETRIES`
   - `OPENAI_MAX_OUTPUT_TOKENS`
   - `SECRET_KEY`
7. Deploy the app

## Notes

- Do not commit real API keys
- PostgreSQL is now used for persistent deployment data such as users and analysis history

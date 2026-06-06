# Viva Notes

## What is your project?

AI Debugging Assistant is a Flask-based web application that helps users debug code using AI-generated structured explanations, fixes, and optimization suggestions.

## Why did you choose this project?

I chose this project because many beginners find compiler or runtime errors difficult to understand. I wanted to create a system that not only fixes code but also teaches the user why the error happened.

## Which technologies did you use?

I used Python, Flask, PostgreSQL, HTML, CSS, JavaScript, and the OpenAI API.

## What is the role of Flask?

Flask is used as the backend framework. It handles routing, form submission, session management, and communication between the frontend and the AI layer.

## Why did you use PostgreSQL?

PostgreSQL is more suitable for a scalable web application because it supports persistent cloud deployment, structured relational data, and better production readiness than a local file-based database.

## How does the system work?

The user logs in, submits code, the backend sends the code to OpenAI for analysis, and the response is shown in a structured format. If the live AI request fails, the fallback analyzer still gives a useful response.

## What are the main modules?

- Authentication module
- Code analysis module
- History module
- Fallback analysis module

## How is password security handled?

Passwords are not stored in plain text. They are hashed before saving to the database.

## What makes your project different?

The main strength is that it combines debugging with education. It not only identifies problems but also explains them in simple terms and stores previous analysis history.

## What are the future improvements?

I can add support for multiple languages, richer history analytics, downloadable reports, and stronger production-grade authentication.

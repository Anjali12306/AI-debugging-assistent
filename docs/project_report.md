# AI Debugging Assistant Project Report

## 1. Introduction

AI Debugging Assistant is a web-based application developed to simplify the debugging process for beginner programmers. The system accepts code from the user, analyzes it using an AI model, and returns structured feedback that includes the issue, suggested solution, explanation, improved code, and time complexity hints.

## 2. Problem Statement

Many students struggle to understand compiler or runtime errors because standard error messages are often technical and brief. The project solves this problem by translating debugging information into simple educational feedback.

## 3. Objectives

- Build a web-based debugging assistant
- Integrate AI to explain code errors in simple language
- Suggest corrected code and improvements
- Store user accounts and previous analysis history
- Provide a project-ready system using Flask and PostgreSQL
- Extend support toward multiple programming languages
- Handle long code inputs through optimized analysis flow

## 4. Technologies Used

- Python
- Flask
- PostgreSQL
- OpenAI API
- HTML
- CSS
- JavaScript

## 5. System Modules

### 5.1 Authentication Module

The authentication module supports signup, login, logout, password hashing, and session-based access control backed by PostgreSQL.

### 5.2 Debugging Module

The debugging module accepts code from the user, uses the selected programming language as context, sends it to the OpenAI API, and receives structured feedback.

### 5.3 Long-Code Optimization Module

If the submitted code is very large, the system switches to an optimized long-code mode. This mode prioritizes the most important sections of the program and focuses on major structural issues and high-value fixes.

### 5.4 Fallback Module

If the OpenAI request fails, the local analyzer provides syntax checking and basic improvement suggestions so the application remains usable.

### 5.5 History Module

Each analysis is saved in the PostgreSQL database and displayed on the history page for the logged-in user.

## 6. Database Design

### Users Table

- `id`
- `name`
- `email`
- `password_hash`
- `created_at`

### Analysis History Table

- `id`
- `user_id`
- `language`
- `submitted_code`
- `status`
- `source`
- `analysis_mode`
- `error_type`
- `issue`
- `solution`
- `explanation`
- `fixed_code`
- `improvements_json`
- `time_complexity`
- `created_at`

## 7. Working Principle

1. User creates an account or logs in
2. User selects a programming language and submits code
3. Flask processes the request
4. OpenAI analyzes the code and returns structured output
5. If OpenAI fails, the fallback analyzer responds
6. The result is shown on screen and saved to history

## 8. Advantages

- Beginner-friendly explanations
- Structured learning-oriented results
- User authentication and saved history
- Multi-language readiness
- Long-code optimized analysis flow
- Reliable fallback behavior
- Useful for academic learning and code improvement

## 9. Limitations

- Local fallback is strongest for Python and more limited for other languages
- OpenAI features require internet connectivity and an API key
- The fallback analyzer is simpler than the live AI model

## 10. Future Enhancements

- Expand live and fallback coverage for more programming languages
- Add code syntax highlighting
- Add admin dashboard and user analytics
- Add forgot-password workflow
- Add downloadable reports of debugging sessions

## 11. Conclusion

AI Debugging Assistant demonstrates how AI and web development can be combined to make debugging more accessible, educational, and efficient. It serves as a practical academic project with real-world relevance.

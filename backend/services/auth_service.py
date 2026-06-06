import re

from werkzeug.security import check_password_hash, generate_password_hash

from backend.services.db_service import execute, fetch_one


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_user(name: str, email: str, password: str) -> tuple[bool, str]:
    if not name or not email or not password:
        return False, "All fields are required."

    if len(name) < 3:
        return False, "Name should be at least 3 characters long."

    if not EMAIL_PATTERN.match(email):
        return False, "Please enter a valid email address."

    if len(password) < 6:
        return False, "Password should be at least 6 characters long."

    if not any(char.isdigit() for char in password):
        return False, "Password should include at least one number."

    existing_user = fetch_one("SELECT id FROM users WHERE email = %s", (email,))
    if existing_user:
        return False, "An account with this email already exists."

    execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (name, email, generate_password_hash(password)),
        commit=True,
    )
    return True, "User created."


def authenticate_user(email: str, password: str) -> dict | None:
    user = fetch_one(
        "SELECT id, name, email, password_hash FROM users WHERE email = %s",
        (email,),
    )
    if user and check_password_hash(user["password_hash"], password):
        return {"id": user["id"], "name": user["name"], "email": user["email"]}
    return None

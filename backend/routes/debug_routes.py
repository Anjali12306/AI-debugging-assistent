from flask import Blueprint, redirect, render_template, request, session, url_for

from backend.services.ai_service import analyze_code_with_ai
from backend.services.history_service import get_user_history, save_analysis
from backend.utils.code_parser import normalize_code


debug_bp = Blueprint("debug", __name__)


@debug_bp.route("/", methods=["GET", "POST"])
def index():
    if "user_email" not in session or "user_id" not in session:
        session.clear()
        return redirect(url_for("auth.login"))

    analysis = None
    submitted_code = ""
    selected_language = "Python"

    if request.method == "POST":
        selected_language = request.form.get("language", "Python")
        submitted_code = request.form.get("code", "")
        cleaned_code = normalize_code(submitted_code)
        analysis = analyze_code_with_ai(cleaned_code, selected_language)
        save_analysis(session["user_id"], selected_language, cleaned_code, analysis)

    return render_template(
        "index.html",
        analysis=analysis,
        submitted_code=submitted_code,
        selected_language=selected_language,
        current_user=session.get("user_name"),
    )


@debug_bp.route("/history")
def history():
    if "user_email" not in session or "user_id" not in session:
        session.clear()
        return redirect(url_for("auth.login"))

    history_items = get_user_history(session["user_id"])
    return render_template(
        "history.html",
        history_items=history_items,
        current_user=session.get("user_name"),
    )

import json

from backend.services.db_service import execute, fetch_all


def save_analysis(user_id: int, language: str, submitted_code: str, analysis: dict) -> None:
    execute(
        """
        INSERT INTO analysis_history (
            user_id,
            language,
            submitted_code,
            status,
            source,
            analysis_mode,
            error_type,
            issue,
            solution,
            explanation,
            fixed_code,
            improvements_json,
            time_complexity
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            language,
            submitted_code,
            analysis["status"],
            analysis.get("source", "Unknown"),
            analysis.get("analysis_mode", "Standard"),
            analysis["error_type"],
            analysis["issue"],
            analysis["solution"],
            analysis["explanation"],
            analysis["fixed_code"],
            json.dumps(analysis.get("improvements", [])),
            analysis["time_complexity"],
        ),
        commit=True,
    )


def get_user_history(user_id: int) -> list[dict]:
    rows = fetch_all(
        """
        SELECT id, language, submitted_code, status, source, analysis_mode, error_type, issue, solution,
               explanation, fixed_code, improvements_json, time_complexity, created_at
        FROM analysis_history
        WHERE user_id = %s
        ORDER BY created_at DESC, id DESC
        """,
        (user_id,),
    )

    history_items = []
    for row in rows:
        history_items.append(
            {
                "id": row["id"],
                "language": row["language"],
                "submitted_code": row["submitted_code"],
                "status": row["status"],
                "source": row["source"],
                "analysis_mode": row["analysis_mode"],
                "error_type": row["error_type"],
                "issue": row["issue"],
                "solution": row["solution"],
                "explanation": row["explanation"],
                "fixed_code": row["fixed_code"],
                "improvements": json.loads(row["improvements_json"]),
                "time_complexity": row["time_complexity"],
                "created_at": row["created_at"],
            }
        )
    return history_items

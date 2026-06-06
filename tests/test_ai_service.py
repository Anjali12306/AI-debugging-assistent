from backend.services.ai_service import analyze_code_with_ai


def test_missing_code_response():
    result = analyze_code_with_ai("")
    assert result["error_type"] == "Missing Code"

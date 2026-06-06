from __future__ import annotations

import ast
import os
from collections import Counter
from functools import lru_cache

from openai import OpenAI
from pydantic import BaseModel, Field


class DebugAnalysis(BaseModel):
    status: str = Field(description="Overall result status for the analysis.")
    source: str = Field(description="Whether the result came from OpenAI live mode or the local fallback.")
    language: str = Field(description="The programming language selected by the user.")
    analysis_mode: str = Field(description="Whether the request used standard mode or optimized long-code mode.")
    error_type: str = Field(description="The category of issue found in the code.")
    issue: str = Field(description="A short description of the main bug or concern.")
    solution: str = Field(description="A practical next step to fix the issue.")
    explanation: str = Field(description="A beginner-friendly explanation of why the issue happened.")
    fixed_code: str = Field(description="A corrected or improved version of the submitted code.")
    improvements: list[str] = Field(description="A list of optimization or readability improvements.")
    time_complexity: str = Field(description="A simple estimate of the code's time complexity.")


SUPPORTED_LANGUAGES = ["Python", "C", "C++", "Java", "JavaScript"]


def analyze_code_with_ai(code: str, language: str = "Python") -> dict:
    if not code:
        return _missing_code_response(language)

    selected_language = language if language in SUPPORTED_LANGUAGES else "Python"
    analysis_mode = _get_analysis_mode(code)
    local_context = _build_local_context(code, selected_language, analysis_mode)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return {
            "status": "Configuration required",
            "source": "Setup",
            "language": selected_language,
            "analysis_mode": analysis_mode,
            "error_type": "Missing API Key",
            "issue": "The website is not connected to OpenAI yet because `OPENAI_API_KEY` is missing.",
            "solution": "Add your OpenAI API key to the `.env` file or set it as an environment variable, then restart the Flask app.",
            "explanation": "The OpenAI Python SDK reads the API key from the environment before it can send a request.",
            "fixed_code": code,
            "improvements": [
                "Open `.env` and set `OPENAI_API_KEY=your_key_here`.",
                "Optionally set `OPENAI_MODEL=gpt-5.4-mini` or another supported model.",
            ],
            "time_complexity": "Not analyzed because the API request was not sent",
        }

    try:
        response = _get_client().responses.parse(
            model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
            input=[
                {"role": "system", "content": _load_prompt()},
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following {selected_language} code and return a structured debugging report.\n\n"
                        f"Local context:\n{local_context}\n\n"
                        f"Submitted code:\n{_prepare_code_for_model(code, analysis_mode)}"
                    ),
                },
            ],
            text_format=DebugAnalysis,
            max_output_tokens=int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "450")),
        )
        parsed = response.output_parsed
        if parsed is None:
            raise ValueError("The model response did not include parsed structured output.")
        result = parsed.model_dump()
        if not result.get("source"):
            result["source"] = "OpenAI Live"
        result["language"] = selected_language
        result["analysis_mode"] = analysis_mode
        return result
    except Exception as exc:
        fallback = _analyze_code_locally(code, selected_language, analysis_mode)
        fallback["status"] = "Fallback analysis complete"
        fallback["source"] = "Smart Fallback"
        fallback["solution"] = (
            "The live AI request did not finish successfully, so the assistant switched to its built-in analyzer. "
            "You can still use these results for your demo, then retry live mode after checking the API key, internet connection, and model name."
        )
        fallback["explanation"] = (
            "The project includes a backup analyzer so it can continue giving debugging help even if the live AI request is slow or unavailable."
        )
        fallback["improvements"].insert(0, f"Live mode note: {type(exc).__name__} occurred, so the backup analyzer handled this request.")
        return fallback


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    return OpenAI(
        timeout=float(os.getenv("OPENAI_TIMEOUT", "45")),
        max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "2")),
    )


@lru_cache(maxsize=1)
def _load_prompt() -> str:
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "prompts",
        "debug_prompt.txt",
    )
    with open(prompt_path, "r", encoding="utf-8") as prompt_file:
        return prompt_file.read().strip()


def _missing_code_response(language: str) -> dict:
    return {
        "status": "No input provided",
        "source": "Input Required",
        "language": language,
        "analysis_mode": "Standard",
        "error_type": "Missing Code",
        "issue": "No code was submitted for analysis.",
        "solution": f"Paste your {language} code into the editor and submit it again.",
        "explanation": "The assistant needs source code before it can analyze bugs, improvements, or complexity.",
        "fixed_code": f"// Paste your {language} code here" if language != "Python" else "# Paste your Python code here",
        "improvements": [
            "Provide a complete code snippet.",
            "Include imports if your logic depends on them.",
        ],
        "time_complexity": "Not available",
    }


def _analyze_code_locally(code: str, language: str, analysis_mode: str) -> dict:
    if language != "Python":
        return _non_python_fallback(code, language, analysis_mode)

    syntax_error = _check_python_syntax(code)
    if syntax_error:
        return syntax_error

    return {
        "status": "Analysis complete",
        "source": "Smart Fallback",
        "language": language,
        "analysis_mode": analysis_mode,
        "error_type": "No syntax errors detected",
        "issue": "The submitted code is syntactically valid.",
        "solution": "Review the suggestions below to improve readability, maintainability, and performance.",
        "explanation": "The code parsed successfully, so the local analyzer focused on quality improvements.",
        "fixed_code": code,
        "improvements": _collect_improvements(code),
        "time_complexity": _estimate_python_time_complexity(code),
    }


def _build_local_context(code: str, language: str, analysis_mode: str) -> str:
    line_count = len(code.splitlines())
    syntax_summary = "Local parser is only available for Python."
    complexity_hint = "Complexity will be estimated by the AI model."

    if language == "Python":
        syntax_error = _check_python_syntax(code)
        syntax_summary = syntax_error["issue"] if syntax_error else "No syntax error detected by the local parser."
        complexity_hint = _estimate_python_time_complexity(code) if syntax_error is None else "Not available until syntax is fixed."

    return (
        f"Language: {language}\n"
        f"Analysis mode: {analysis_mode}\n"
        f"Line count: {line_count}\n"
        f"Local syntax summary: {syntax_summary}\n"
        f"Local complexity hint: {complexity_hint}\n"
        "Use this context to answer faster, but rely on the submitted code as the source of truth."
    )


def _check_python_syntax(code: str) -> dict | None:
    try:
        ast.parse(code)
        return None
    except SyntaxError as exc:
        line = exc.lineno or "unknown"
        message = exc.msg or "Invalid Python syntax"
        return {
            "status": "Error detected",
            "source": "Smart Fallback",
            "language": "Python",
            "analysis_mode": _get_analysis_mode(code),
            "error_type": "Syntax Error",
            "issue": f"{message} on line {line}.",
            "solution": "Fix the syntax issue, then submit the code again for another pass.",
            "explanation": "Python could not parse the code, so execution would stop before the program starts.",
            "fixed_code": _mock_fixed_code(code),
            "improvements": [
                "Check for a missing colon after `if`, `for`, `while`, `def`, or `class`.",
                "Make sure brackets, quotes, and parentheses are closed.",
                "Verify indentation is consistent.",
            ],
            "time_complexity": "Not available until the code parses successfully",
        }


def _collect_improvements(code: str) -> list[str]:
    suggestions: list[str] = []
    lines = code.splitlines()

    if len(lines) > 25:
        suggestions.append("Break long logic into smaller helper functions.")

    if "print(" in code:
        suggestions.append("Replace debugging print statements with logging in larger projects.")

    if any(len(line) > 88 for line in lines):
        suggestions.append("Wrap long lines to make the code easier to read.")

    loop_count = sum(1 for line in lines if line.strip().startswith(("for ", "while ")))
    if loop_count > 1:
        suggestions.append("Review repeated loops and check whether some work can be combined.")

    duplicate_names = _find_repeated_variable_names(code)
    if duplicate_names:
        repeated_list = ", ".join(duplicate_names[:3])
        suggestions.append(f"Use more descriptive variable names instead of repeating names like {repeated_list}.")

    if not suggestions:
        suggestions.append("The code looks clean at a high level; the next step is testing edge cases.")

    return suggestions


def _find_repeated_variable_names(code: str) -> list[str]:
    tree = ast.parse(code)
    names: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.append(node.id)

    counts = Counter(names)
    return [name for name, count in counts.items() if count > 1]


def _estimate_python_time_complexity(code: str) -> str:
    loop_lines = [
        line for line in code.splitlines() if line.strip().startswith(("for ", "while "))
    ]
    if not loop_lines:
        return "Likely O(1) or dependent on built-in library behavior"

    indent_levels = [
        len(line) - len(line.lstrip())
        for line in code.splitlines()
        if line.strip().startswith(("for ", "while "))
    ]
    nested_loops = len(indent_levels) > 1 and len(set(indent_levels)) > 1

    if nested_loops:
        return "Likely O(n^2) in the worst case due to nested loops"

    return "Likely O(n) based on single-pass iteration"


def _mock_fixed_code(code: str) -> str:
    fixed_lines = []
    for line in code.splitlines():
        stripped = line.rstrip()
        if stripped.startswith(("if ", "for ", "while ", "def ", "class ")) and not stripped.endswith(":"):
            fixed_lines.append(f"{stripped}:")
        else:
            fixed_lines.append(line)
    return "\n".join(fixed_lines)


def _non_python_fallback(code: str, language: str, analysis_mode: str) -> dict:
    line_count = len(code.splitlines())
    long_lines = sum(1 for line in code.splitlines() if len(line) > 100)
    bracket_warning = _check_bracket_balance(code)
    improvements = [
        f"The local fallback has limited rules for {language}, so use live mode for deeper language-specific feedback.",
    ]
    if line_count > 40:
        improvements.append("Consider splitting this program into smaller functions or classes.")
    if long_lines:
        improvements.append("Some lines are very long; formatting them will improve readability.")
    if bracket_warning:
        improvements.append(bracket_warning)

    return {
        "status": "Analysis complete",
        "source": "Smart Fallback",
        "language": language,
        "analysis_mode": analysis_mode,
        "error_type": "General Code Review",
        "issue": f"The local fallback cannot fully parse {language} syntax, so this is a heuristic review.",
        "solution": "Use the structured suggestions below, or retry when live mode is available for a deeper language-aware response.",
        "explanation": f"The built-in fallback is strongest for Python. For {language}, it focuses on code size, formatting, and common structural risks.",
        "fixed_code": code,
        "improvements": improvements,
        "time_complexity": "Estimated by live mode for non-Python languages",
    }


def _check_bracket_balance(code: str) -> str | None:
    pairs = {"(": ")", "{": "}", "[": "]"}
    closing = {value: key for key, value in pairs.items()}
    stack: list[str] = []
    for char in code:
        if char in pairs:
            stack.append(char)
        elif char in closing:
            if not stack or stack[-1] != closing[char]:
                return "Check bracket and brace matching; an opening or closing symbol may be misplaced."
            stack.pop()
    if stack:
        return "Check bracket and brace matching; some opening symbols may not be closed."
    return None


def _get_analysis_mode(code: str) -> str:
    if len(code) > 4500 or len(code.splitlines()) > 140:
        return "Optimized Long-Code Mode"
    return "Standard"


def _prepare_code_for_model(code: str, analysis_mode: str) -> str:
    if analysis_mode == "Standard":
        return code

    lines = code.splitlines()
    if len(lines) <= 160:
        return code

    first_chunk = "\n".join(lines[:80])
    last_chunk = "\n".join(lines[-60:])
    return (
        "Large code detected. Prioritize structural review, major errors, and the most important fixes.\n\n"
        "Beginning of code:\n"
        f"{first_chunk}\n\n"
        "...\n\n"
        "End of code:\n"
        f"{last_chunk}"
    )

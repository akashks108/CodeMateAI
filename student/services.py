
import os
import requests


COMPILERS = {
    "python": "python-3.14",
    "java": "openjdk-25",
    "c": "gcc-15",
    "cpp": "g++-15",
    "php": "php-8.5",
}


def execute_code(language, source_code, user_input=""):
    language = language.lower()

    if language not in COMPILERS:
        return {
            "status": "error",
            "output": "",
            "error": "Unsupported programming language.",
        }

    api_key = os.getenv("ONLINECOMPILER_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "output": "",
            "error": "OnlineCompiler API key is not configured.",
        }

    url = "https://api.onlinecompiler.io/api/run-code-sync/"

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "compiler": COMPILERS[language],
        "code": source_code,
        "input": user_input,
        "time_limit": 10,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=35,
        )

        response.raise_for_status()

        result = response.json()

        return {
            "status": result.get("status", "error"),
            "output": result.get("output", ""),
            "error": result.get("error", ""),
            "exit_code": result.get("exit_code"),
            "time": result.get("time"),
            "memory": result.get("memory"),
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "output": "",
            "error": "Execution request timed out.",
        }

    except requests.exceptions.RequestException:
        return {
            "status": "error",
            "output": "",
            "error": "Unable to connect to the code execution service.",
        }

    except ValueError:
        return {
            "status": "error",
            "output": "",
            "error": "Invalid response received from the execution service.",
        }

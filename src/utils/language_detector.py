def detect_language(code: str):
    if "System.out" in code or "PreparedStatement" in code:
        return "java"
    elif "def " in code or "import os" in code:
        return "python"
    elif "document." in code or "innerHTML" in code:
        return "javascript"
    return "text"
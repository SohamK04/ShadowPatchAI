PROMPTS = {
    "sql_injection": """
You are a secure coding assistant.

The following code is vulnerable to SQL Injection.
Rewrite it securely using parameterized queries or prepared statements.
Preserve the original logic and variable intent.
Do NOT add extra functionality.

Vulnerable Code:
{code}

Return ONLY the patched code.
""",

    "xss": """
You are a secure coding assistant.

The following code is vulnerable to Cross-Site Scripting (XSS).
Rewrite it by properly escaping or sanitizing user input.
Preserve functionality.

Vulnerable Code:
{code}

Return ONLY the patched code.
""",

    "command_injection": """
You are a secure coding assistant.

The following code is vulnerable to Command Injection.
Rewrite it securely by validating inputs and avoiding shell execution where possible.

Vulnerable Code:
{code}

Return ONLY the patched code.
"""
}

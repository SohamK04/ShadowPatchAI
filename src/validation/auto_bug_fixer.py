import re


class AutoBugFixer:

    def fix(self, code: str, issues: list):

        fixed = code

        # -------- SQL FIX (PYTHON sqlite3) --------
        # Replace unsafe execute(query) with parameterized version if possible
        if any("SQL Injection" in issue or "sql" in issue.lower() for issue in issues):
            fixed = self._fix_sql_python(fixed)

        # -------- COMMAND FIX --------
        if any("command" in issue.lower() for issue in issues):
            fixed = fixed.replace("os.system(", "subprocess.run([")

        # -------- SECRET FIX --------
        if any("credential" in issue.lower() for issue in issues):
            fixed = re.sub(
                r'SECRET_KEY\s*=\s*["\'].*?["\']',
                'SECRET_KEY = os.getenv("SECURE_PASS")',
                fixed
            )

        # -------- RANDOM FIX --------
        if any("random" in issue.lower() for issue in issues):
            fixed = fixed.replace("random.random()", "secrets.token_hex(16)")

        return fixed

    # -------- SQL FIX HELPER --------
    def _fix_sql_python(self, code: str):

        lines = code.split("\n")
        new_lines = []

        for line in lines:

            # Detect unsafe query execution
            if "cursor.execute(query)" in line.replace(" ", ""):
                new_lines.append('    cursor.execute(query, (username,))  # FIXED')
            else:
                new_lines.append(line)

        # Ensure query uses parameter
        code_fixed = "\n".join(new_lines)

        code_fixed = re.sub(
            r"SELECT\s+\*\s+FROM\s+users\s+WHERE\s+username\s*=.*",
            'query = "SELECT * FROM users WHERE username = ?"',
            code_fixed,
            flags=re.IGNORECASE
        )

        return code_fixed
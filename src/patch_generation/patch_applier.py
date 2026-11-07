import re


class PatchApplier:

    def apply_patch(self, code, vulnerabilities):

        patched = code

        # =====================================================
        # SQL INJECTION FIX
        # =====================================================
        if "sql_injection" in vulnerabilities:

            patched = patched.replace(
                '''query = "SELECT * FROM players WHERE username = '" + user + "'"''',
                '''query = "SELECT * FROM players WHERE username = ?"'''
            )

            patched = patched.replace(
                '''update = "UPDATE players SET score = " + score + " WHERE username = '" + user + "'"''',
                '''update = "UPDATE players SET score = ? WHERE username = ?"'''
            )

            patched = patched.replace(
                '''q1 = "SELECT * FROM users WHERE name = '" + user + "'"''',
                '''q1 = "SELECT * FROM users WHERE name = ?"'''
            )

            patched = patched.replace(
                '''q2 = "DELETE FROM users WHERE name = '" + user + "'"''',
                '''q2 = "DELETE FROM users WHERE name = ?"'''
            )

            patched = patched.replace(
                "cursor.execute(query)",
                "cursor.execute(query, (user,))"
            )

            patched = patched.replace(
                "cursor.execute(update)",
                "cursor.execute(update, (score, user))"
            )

            patched = patched.replace(
                "cursor.execute(q1)",
                "cursor.execute(q1, (user,))"
            )

            patched = patched.replace(
                "cursor.execute(q2)",
                "cursor.execute(q2, (user,))"
            )

        # =====================================================
        # COMMAND INJECTION FIX
        # =====================================================
        if "command_injection" in vulnerabilities:

            patched = patched.replace(
                'os.system("echo " + user)',
                'subprocess.run(["echo", user], check=True)'
            )

            patched = patched.replace(
                'os.system("ping " + user)',
                'subprocess.run(["ping", user], check=True)'
            )

            patched = patched.replace(
                'os.system(cmd)',
                '# blocked unsafe command execution'
            )

            if "import subprocess" not in patched:
                patched = "import subprocess\n" + patched

        # =====================================================
        # XSS FIX
        # =====================================================
        if "xss" in vulnerabilities:

            if "import html" not in patched:
                patched = "import html\n" + patched

            patched = patched.replace(
                'return "<h1>Welcome " + user + "</h1>"',
                'return "<h1>Welcome " + html.escape(user) + "</h1>"'
            )

            patched = patched.replace(
                'return "<div>" + user + "</div>"',
                'return "<div>" + html.escape(user) + "</div>"'
            )

        # =====================================================
        # WEAK RANDOM FIX
        # =====================================================
        if "weak_random" in vulnerabilities:

            patched = patched.replace(
                "random.random()",
                'secrets.token_hex(16)'
            )

            if "import secrets" not in patched:
                patched = "import secrets\n" + patched

        # =====================================================
        # HARDCODED CREDENTIALS FIX
        # =====================================================
        if "hardcoded_credentials" in vulnerabilities:

            patched = patched.replace(
                'SECRET = "supersecret"',
                'SECRET = os.getenv("SECRET")'
            )

            patched = patched.replace(
                'API_KEY = "123456"',
                'API_KEY = os.getenv("API_KEY")'
            )

            patched = patched.replace(
                'pwd = "password123"',
                'pwd = os.getenv("PASSWORD")'
            )

        # =====================================================
        # PATH + FILE HANDLING FIX
        # =====================================================
        if "path_traversal" in vulnerabilities or "file_handling" in vulnerabilities:

            patched = patched.replace(
                'file = request.args.get("file")',
                '''
file = request.args.get("file")

safe_file = os.path.basename(file)

if ".." in safe_file or "/" in safe_file or "\\\\" in safe_file:
    return "Invalid file path"

if not safe_file.endswith(".txt"):
    return "Invalid file"
'''
            )

            patched = patched.replace(
                'with open(file, "r") as f:',
                'with open(safe_file, "r") as f:'
            )

        # =====================================================
        # UNSAFE EXECUTION FIX
        # =====================================================
        if "unsafe_execution" in vulnerabilities:

            patched = patched.replace("eval(", "# blocked eval(")
            patched = patched.replace("exec(", "# blocked exec(")

        return patched
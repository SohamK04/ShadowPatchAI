import ast


class ASTPatchApplier:

    def apply_patch(self, code: str, vulnerabilities: list):

        patched = code

        # -------- SQL FIX --------
        patched = patched.replace(
            'cursor.execute(query)',
            'cursor.execute(query, (user,))'
        )

        patched = patched.replace(
            '"+ user +"',
            '?'
        )

        # -------- COMMAND FIX --------
        patched = patched.replace(
            'os.system("ping " + user)',
            'subprocess.run(["ping", user], check=True)'
        )

        patched = patched.replace(
            'os.system("echo " + user)',
            'print(user)'
        )

        patched = patched.replace(
            'os.system(cmd)',
            'return "Blocked unsafe execution"'
        )

        # -------- XSS FIX --------
        patched = patched.replace(
            '"<h1>Welcome " + user + "</h1>"',
            'f"Welcome {html.escape(user)}"'
        )

        patched = patched.replace(
            '"<div>" + user + "</div>"',
            'f"{html.escape(user)}"'
        )

        # -------- RANDOM FIX --------
        patched = patched.replace(
            'random.random()',
            'secrets.token_hex(16)'
        )

        # -------- SECRET FIX --------
        patched = patched.replace(
            '"supersecret"',
            'os.getenv("SECRET")'
        )

        patched = patched.replace(
            '"password123"',
            'os.getenv("PASSWORD")'
        )

        # -------- PATH FIX --------
        if 'request.args.get("file")' in patched:
            patched = patched.replace(
                'file = request.args.get("file")',
                'file = request.args.get("file")\n    if not file or not file.isalnum(): return "Invalid file"'
            )

        return patched
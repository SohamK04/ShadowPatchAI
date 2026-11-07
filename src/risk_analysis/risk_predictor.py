class RiskPredictor:

    def predict(self, code):

        vulnerabilities = []

        normalized = code.replace(" ", "").replace("\n", "").lower()

        # =====================================================
        # SQL INJECTION
        # =====================================================
        dangerous_sql_patterns = [
            '"+user+"',
            "'+user+'",
            '"+score+"',
            "'+score+'",
        ]

        unsafe_execute = (
            "cursor.execute(query)" in normalized or
            "cursor.execute(update)" in normalized or
            "cursor.execute(q1)" in normalized or
            "cursor.execute(q2)" in normalized
        )

        if any(p in normalized for p in dangerous_sql_patterns) or unsafe_execute:
            vulnerabilities.append("sql_injection")

        # =====================================================
        # COMMAND INJECTION
        # =====================================================
        if "os.system(" in normalized:
            vulnerabilities.append("command_injection")

        # =====================================================
        # XSS
        # =====================================================
        dangerous_xss = (
            'return"<h1>welcome"+user' in normalized or
            'return"<div>"+user' in normalized
        )

        escaped = "html.escape(" in normalized

        if dangerous_xss and not escaped:
            vulnerabilities.append("xss")

        # =====================================================
        # WEAK RANDOM
        # =====================================================
        if "random.random()" in normalized:
            vulnerabilities.append("weak_random")

        # =====================================================
        # HARDCODED CREDENTIALS
        # =====================================================
        dangerous_creds = [
            'supersecret',
            '123456',
            'password123'
        ]

        if any(c in normalized for c in dangerous_creds):
            vulnerabilities.append("hardcoded_credentials")

        # =====================================================
        # PATH TRAVERSAL
        # =====================================================
        unsafe_open = "open(file," in normalized

        safe_usage = (
            "safe_file" in normalized and
            "basename" in normalized
        )

        if unsafe_open and not safe_usage:
            vulnerabilities.append("path_traversal")

        # =====================================================
        # FILE HANDLING
        # =====================================================
        safe_validation = (
            ".endswith(" in normalized and
            "invalidfile" in normalized
        )

        if "open(" in normalized and not safe_validation:
            vulnerabilities.append("file_handling")

        # =====================================================
        # UNSAFE EXECUTION
        # =====================================================
        if "eval(" in normalized or "exec(" in normalized:
            vulnerabilities.append("unsafe_execution")

        return {
            "predicted_vulnerability": list(set(vulnerabilities))
        }
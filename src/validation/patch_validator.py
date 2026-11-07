class PatchValidator:

    def validate(self, patched_code, vulnerabilities):

        results = []
        fixed_count = 0

        normalized = patched_code.replace(" ", "").replace("\n", "").lower()

        # =====================================================
        # SQL INJECTION
        # =====================================================
        if "sql_injection" in vulnerabilities:

            dangerous_patterns = [
                '"+user+"',
                "'+user+'",
                '"+score+"',
                "'+score+'",
            ]

            dangerous_sql = any(
                pattern in normalized
                for pattern in dangerous_patterns
            )

            unsafe_execute = (
                "cursor.execute(query)" in normalized or
                "cursor.execute(update)" in normalized or
                "cursor.execute(q1)" in normalized or
                "cursor.execute(q2)" in normalized
            )

            if dangerous_sql or unsafe_execute:
                results.append("sql_injection not fixed ❌")
            else:
                results.append("sql_injection fixed ✔")
                fixed_count += 1

        # =====================================================
        # COMMAND INJECTION
        # =====================================================
        if "command_injection" in vulnerabilities:

            if "os.system(" in normalized:
                results.append("command_injection not fixed ❌")
            else:
                results.append("command_injection fixed ✔")
                fixed_count += 1

        # =====================================================
        # XSS
        # =====================================================
        if "xss" in vulnerabilities:

            dangerous_return = (
                'return"<h1>welcome"+user' in normalized or
                'return"<div>"+user' in normalized
            )

            escaped = "html.escape(" in normalized

            if dangerous_return and not escaped:
                results.append("xss not fixed ❌")
            else:
                results.append("xss fixed ✔")
                fixed_count += 1

        # =====================================================
        # HARDCODED CREDENTIALS
        # =====================================================
        if "hardcoded_credentials" in vulnerabilities:

            dangerous = [
                'supersecret',
                '123456',
                'password123'
            ]

            if any(d in normalized for d in dangerous):
                results.append("hardcoded_credentials not fixed ❌")
            else:
                results.append("hardcoded_credentials fixed ✔")
                fixed_count += 1

        # =====================================================
        # PATH TRAVERSAL
        # =====================================================
        if "path_traversal" in vulnerabilities:

            unsafe_open = "open(file," in normalized

            safe_usage = (
                "safe_file" in normalized and
                "basename" in normalized
            )

            if unsafe_open or not safe_usage:
                results.append("path_traversal not fixed ❌")
            else:
                results.append("path_traversal fixed ✔")
                fixed_count += 1

        # =====================================================
        # FILE HANDLING
        # =====================================================
        if "file_handling" in vulnerabilities:

            safe_validation = (
                ".endswith(" in normalized and
                "invalidfile" in normalized
            )

            if not safe_validation:
                results.append("file_handling not fixed ❌")
            else:
                results.append("file_handling fixed ✔")
                fixed_count += 1

        # =====================================================
        # WEAK RANDOM
        # =====================================================
        if "weak_random" in vulnerabilities:

            if "random.random()" in normalized:
                results.append("weak_random not fixed ❌")
            else:
                results.append("weak_random fixed ✔")
                fixed_count += 1

        # =====================================================
        # UNSAFE EXECUTION
        # =====================================================
        if "unsafe_execution" in vulnerabilities:

            if "eval(" in normalized or "exec(" in normalized:
                results.append("unsafe_execution not fixed ❌")
            else:
                results.append("unsafe_execution fixed ✔")
                fixed_count += 1

        # =====================================================
        # FINAL SCORE
        # =====================================================
        total = len(vulnerabilities)

        score = fixed_count / total if total else 1

        return {
            "is_secure": fixed_count == total,
            "score": round(score, 2),
            "details": results
        }
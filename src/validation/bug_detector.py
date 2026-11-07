class BugDetector:

    def analyze(self, original_code: str, patched_code: str):

        issues = []

        full_code = patched_code.replace("\n", " ")

        # userId check
        if "userId" in full_code:
            if "int userId" not in full_code and "Integer.parseInt" not in full_code:
                issues.append("Possible undefined variable: userId")

        # validatedInput check
        if "validatedInput" in full_code:
            if "String validatedInput" not in full_code:
                issues.append("Possible undefined variable: validatedInput")

        # Syntax
        if patched_code.count("(") != patched_code.count(")"):
            issues.append("Unbalanced parentheses")

        if patched_code.count("{") != patched_code.count("}"):
            issues.append("Unbalanced curly braces")

        # SQL check
        if "SELECT" in full_code and "?" not in full_code:
            issues.append("SQL patch incomplete")

        # PreparedStatement execution
        if "PreparedStatement" in full_code and "execute" not in full_code:
            issues.append("PreparedStatement not executed")

        score = max(0, 1 - (len(issues) * 0.2))

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "confidence_score": round(score, 2)
        }
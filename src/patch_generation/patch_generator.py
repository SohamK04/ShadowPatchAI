class PatchGenerator:

    def __init__(self):
        pass

    def generate_patch(self, code: str, vulnerabilities: list):

        patches = []

        for vuln in vulnerabilities:

            if vuln == "sql_injection":
                patches.append(
                    "// SQL FIX\nUse PreparedStatement with parameterized queries"
                )

            elif vuln == "command_injection":
                patches.append(
                    "// COMMAND FIX\nUse ProcessBuilder instead of exec/system"
                )

            elif vuln == "xss":
                patches.append(
                    "// XSS FIX\nEscape user input or use safe rendering (textContent)"
                )

            elif vuln == "hardcoded_credentials":
                patches.append(
                    "// SECRET FIX\nUse environment variables (System.getenv)"
                )

            elif vuln == "weak_random":
                patches.append(
                    "// RANDOM FIX\nUse SecureRandom instead of Random"
                )

            elif vuln == "file_handling":
                patches.append(
                    "// FILE FIX\nValidate file paths and use try-with-resources"
                )

        if not patches:
            return "// Code is safe. No patch required."

        return "\n\n".join(patches)
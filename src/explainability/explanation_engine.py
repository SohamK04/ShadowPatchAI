class ExplanationEngine:

    def explain(self, vulnerabilities):

        explanations = []

        for vuln in vulnerabilities:

            if vuln == "sql_injection":
                explanations.append(
                    "SQL Injection allows attackers to manipulate database queries and access unauthorized data."
                )

            elif vuln == "command_injection":
                explanations.append(
                    "Command Injection allows execution of arbitrary system commands from user input."
                )

            elif vuln == "xss":
                explanations.append(
                    "Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages."
                )

            elif vuln == "hardcoded_credentials":
                explanations.append(
                    "Hardcoded credentials expose sensitive information and can be easily exploited."
                )

            elif vuln == "weak_random":
                explanations.append(
                    "Weak random number generation can be predicted and exploited."
                )

            elif vuln == "file_handling":
                explanations.append(
                    "Improper file handling can lead to unauthorized file access or data leakage."
                )

        if not explanations:
            return "Code is safe."

        return "\n\n".join(explanations)
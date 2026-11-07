CWE_MAP = {
    "sql_injection": {"cwe": "CWE-89", "severity": 9.0},
    "xss": {"cwe": "CWE-79", "severity": 6.5},
    "command_injection": {"cwe": "CWE-78", "severity": 9.5},
    "hardcoded_credentials": {"cwe": "CWE-798", "severity": 8.0},
    "safe": {"cwe": "None", "severity": 0.0}
}

def get_cwe_info(vuln_type):
    return CWE_MAP.get(vuln_type, {"cwe": "Unknown", "severity": 5.0})
import os
import csv

RAW_VULN_DIR = "data/raw/vulnerable_code"
OUTPUT_FILE = "data/processed/labeled_snippets.csv"

VULN_KEYWORDS = {
    "sql_injection": ["SELECT", "INSERT", "cursor.execute", "executeQuery"],
    "xss": ["<script>", "innerHTML", "document.write"],
    "command_injection": ["os.system", "Runtime.getRuntime", "exec"]
}

def detect_vuln_type(code):
    for vuln, keywords in VULN_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in code.lower():
                return vuln
    return "unknown"

def preprocess():
    rows = []

    for file in os.listdir(RAW_VULN_DIR):
        file_path = os.path.join(RAW_VULN_DIR, file)

        if not file.endswith(".txt"):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        vuln_type = detect_vuln_type(code)

        if vuln_type != "unknown":
            rows.append([code, vuln_type, "synthetic/owasp"])

    os.makedirs("data/processed", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["code_snippet", "vulnerability_type", "source"])
        writer.writerows(rows)

    print(f"[✔] Dataset created with {len(rows)} samples")

if __name__ == "__main__":
    preprocess()

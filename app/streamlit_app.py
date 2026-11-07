import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import difflib
import time
from io import BytesIO

from src.risk_analysis.risk_predictor import RiskPredictor
from src.patch_generation.patch_applier import PatchApplier
from src.validation.patch_validator import PatchValidator

predictor = RiskPredictor()
patcher = PatchApplier()
validator = PatchValidator()

st.set_page_config(layout="wide", page_title="ShadowPatch AI")

# ---------------- SESSION ----------------
if "selected_vuln" not in st.session_state:
    st.session_state.selected_vuln = None

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# ---------------- SEVERITY ----------------
severity = {
    "sql_injection":("🔥 High","CWE-89","SQL query manipulation","Use parameterized queries"),
    "command_injection":("🔥 High","CWE-78","OS command execution","Use subprocess safely"),
    "xss":("⚠️ Medium","CWE-79","HTML injection","Escape output"),
    "weak_random":("✔️ Low","CWE-330","Predictable randomness","Use secrets module"),
    "hardcoded_credentials":("🔥 High","CWE-798","Hardcoded secrets","Use environment variables"),
    "path_traversal":("🔥 High","CWE-22","Unauthorized file access","Validate file paths"),
    "unsafe_execution":("🔥 High","CWE-78","Dynamic execution","Avoid eval/exec"),
    "file_handling":("⚠️ Medium","CWE-73","Unsafe file operations","Restrict access")
}

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
body {background: linear-gradient(135deg,#0f172a,#020617);}

.metric-box {text-align:center;}
.diff-box {background:#020617;padding:10px;border-radius:10px;font-family:monospace;}
.add {color:#22c55e;}
.rem {color:#ef4444;}
.card {background:rgba(30,41,59,0.7);padding:15px;border-radius:12px;margin-bottom:10px;}
.popup {background:#1e293b;padding:20px;border-radius:12px;border:1px solid #334155;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ ShadowPatch AI")

# ---------------- INPUT ----------------
col1, col2 = st.columns([3,1])

with col1:
    code = st.text_area("💻 Paste Code", height=300)

with col2:
    uploaded = st.file_uploader("📂 Upload File", type=["py","txt"])
    if uploaded:
        code = uploaded.read().decode()

# ---------------- AI ASSISTANT ----------------
st.markdown("### 💬 Ask Security AI")
query = st.text_input("Ask about vulnerabilities or fixes")

def ai_response(q):
    q = q.lower()
    if "sql" in q:
        return "SQL Injection → use parameterized queries."
    elif "xss" in q:
        return "XSS → escape HTML output."
    elif "command" in q:
        return "Command Injection → avoid os.system."
    elif "random" in q:
        return "Weak randomness → use secrets module."
    return "Ask about SQL, XSS, command injection, etc."

if query:
    st.info(ai_response(query))

# ---------------- ANALYZE ----------------
if st.button("🚀 Analyze & Fix") and code:
    vulns = predictor.predict(code)["predicted_vulnerability"]
    fixed = patcher.apply_patch(code, vulns)
    validation = validator.validate(fixed, vulns)

    st.session_state.vulns = vulns
    st.session_state.fixed = fixed
    st.session_state.validation = validation
    st.session_state.analysis_done = True

# ---------------- OUTPUT ----------------
if st.session_state.analysis_done:

    vulns = st.session_state.vulns
    fixed = st.session_state.fixed
    validation = st.session_state.validation

    score = max(1 - 0.1*len(vulns), 0)

    # -------- TOP STRIP --------
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
    padding:18px;background:#1e293b;border-radius:12px;margin-bottom:15px;">
        <div class='metric-box'><div>⚡ Risk Score</div><b>{round(score,2)}</b></div>
        <div class='metric-box'><div>🐞 Issues</div><b>{len(vulns)}</b></div>
        <div class='metric-box'><div>🛡️ Status</div>
        <b style="color:{'#22c55e' if validation['is_secure'] else '#ef4444'};">
        {"Secure" if validation["is_secure"] else "Risk"}</b></div>
    </div>
    """, unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Detection","Patch","Validation","Bugs","Explanation"])

    # -------- DETECTION --------
    with tab1:
        for v in vulns:
            if st.button(v, key=f"v_{v}"):
                st.session_state.selected_vuln = v
        st.code(code)

    # -------- PATCH --------
    with tab2:
        st.code(fixed)
        st.markdown("### 🔄 Diff")

        diff = difflib.unified_diff(code.splitlines(), fixed.splitlines(), lineterm="")

        st.markdown("<div class='diff-box'>", unsafe_allow_html=True)
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                st.markdown(f"<span class='add'>{line}</span>", unsafe_allow_html=True)
            elif line.startswith("-") and not line.startswith("---"):
                st.markdown(f"<span class='rem'>{line}</span>", unsafe_allow_html=True)
            else:
                st.markdown(line)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button("⬇ Download Fixed Code", fixed)

    # -------- VALIDATION --------
    with tab3:
        st.progress(int(validation["score"]*100))
        for d in validation["details"]:
            st.write("✔️" if "fixed" in d else "❌", d)

    # -------- BUGS --------
    with tab4:
        if validation["is_secure"]:
            st.success("No Bugs Found")
        else:
            st.warning("Check fixes carefully")

    # -------- EXPLANATION --------
    with tab5:
        for v in vulns:
            sev,cwe,desc,fix = severity.get(v,("Unknown","","",""))
            color = "#ef4444" if "High" in sev else "#f59e0b" if "Medium" in sev else "#22c55e"

            st.markdown(f"""
            <div class='card' style="border-left:5px solid {color}">
                <b>{v}</b><br>
                <span style="color:{color}">{sev}</span><br>
                {cwe}<br><br>
                <b>Issue:</b> {desc}<br>
                <b>Fix:</b> {fix}
            </div>
            """, unsafe_allow_html=True)

# ---------------- POPUP ----------------
if st.session_state.selected_vuln:
    v = st.session_state.selected_vuln
    sev,cwe,desc,fix = severity.get(v,("","","",""))

    st.markdown(f"""
    <div class='popup'>
    <h3>{v}</h3>
    <b>{sev}</b><br>{cwe}<br><br>
    {desc}<br><b>Fix:</b> {fix}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Close"):
        st.session_state.selected_vuln = None
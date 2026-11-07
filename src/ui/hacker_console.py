import time
import streamlit as st

def hacker_typing(text, speed=0.01):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(f"```bash\n{output}```")
        time.sleep(speed)


def fake_attack_simulation():
    steps = [
        "[+] Initializing exploit...",
        "[+] Scanning input vectors...",
        "[+] Injecting payload: ' OR 1=1 --",
        "[+] Bypassing authentication...",
        "[!] Database access granted",
        "[!] Dumping sensitive records...",
        "[✔] Exploit Successful!"
    ]

    for step in steps:
        hacker_typing(step, 0.02)
        time.sleep(0.3)
import difflib

def generate_diff(original, patched):
    return "\n".join(difflib.unified_diff(
        original.splitlines(),
        patched.splitlines(),
        lineterm=""
    ))
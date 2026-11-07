import pandas as pd
import random

data = []

SAMPLES_PER_CLASS = 80   # total ~320 samples

# ---------------- SQL INJECTION ----------------
sql_samples = [
    'query = "SELECT * FROM users WHERE id = " + user_input',
    'sql = f"SELECT * FROM users WHERE id={user_id}"',
    'cursor.execute("SELECT * FROM users WHERE name=\'" + name + "\'")',
    'query = "SELECT * FROM users WHERE email = %s" % email',
    'db.query("SELECT * FROM users WHERE id=" + str(id))',
    'statement.executeQuery("SELECT * FROM users WHERE id=" + input)',
    'query = "SELECT * FROM products WHERE price < " + max_price'
]

# ---------------- XSS ----------------
xss_samples = [
    'element.innerHTML = user_input',
    'document.write(user_input)',
    'output = "<div>" + user_input + "</div>"',
    'html = f"<p>{user_input}</p>"',
    'res.send("<h1>" + user_input + "</h1>")'
]

# ---------------- COMMAND INJECTION ----------------
cmd_samples = [
    'os.system("ping " + user_input)',
    'subprocess.call("ls " + user_input, shell=True)',
    'os.popen("cat " + filename)',
    'Runtime.getRuntime().exec("cmd " + input)',
    'exec("ping " + ip)'
]

# ---------------- SAFE CODE ----------------
safe_samples = [
    'query = "SELECT * FROM users WHERE id = ?" ; stmt.setInt(1, userId)',
    'cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))',
    'element.textContent = user_input',
    'print(user_input)',
    'subprocess.run(["ping", user_input])',
    'html.escape(user_input)',
    'logger.info(user_input)',
    'return render_template("index.html", data=data)'
]

# ---------------- CROSS-CONFUSION SAMPLES ----------------
# looks safe but still risky OR looks risky but safe
cross_samples = [
    'query = "SELECT * FROM users WHERE id = ?" + user_input',   # mixed
    'element.innerHTML = sanitize(user_input)',                 # looks safe
    'subprocess.run("ping " + input, shell=True)',              # tricky
    'cursor.execute("SELECT * FROM users WHERE id = %s" + id)', # hybrid
    'print("<div>" + user_input + "</div>")'                    # maybe safe?
]


variables = ["user_input", "input", "data", "param", "value", "userId", "name", "id"]


def mutate(code):
    var = random.choice(variables)
    code = code.replace("user_input", var)

    noise = [
        "",
        " ",
        "\n",
        " # debug",
        " // test",
        " ;",
        " + ''"
    ]

    return code + random.choice(noise)


def generate(base, label, count):
    samples = []
    for _ in range(count):
        code = mutate(random.choice(base))
        samples.append({
            "code_snippet": code,
            "vulnerability_type": label,
            "source": "synthetic"
        })
    return samples


# ---------------- BUILD DATASET ----------------
data.extend(generate(sql_samples, "sql_injection", SAMPLES_PER_CLASS))
data.extend(generate(xss_samples, "xss", SAMPLES_PER_CLASS))
data.extend(generate(cmd_samples, "command_injection", SAMPLES_PER_CLASS))
data.extend(generate(safe_samples, "safe", SAMPLES_PER_CLASS))

# Cross confusion
data.extend(generate(cross_samples, "mixed", 40))


# ---------------- LABEL NOISE ----------------
for i in range(int(len(data) * 0.05)):   # 5% noise
    data[i]["vulnerability_type"] = random.choice(
        ["sql_injection", "xss", "command_injection", "safe"]
    )


# ---------------- SHUFFLE ----------------
random.shuffle(data)

df = pd.DataFrame(data)
df.to_csv("data/processed/labeled_snippets.csv", index=False)

print(f"Dataset generated with {len(df)} samples")
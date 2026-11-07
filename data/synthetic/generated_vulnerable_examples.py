def generate_sql_vuln():
    return """
    query = "SELECT * FROM users WHERE id = " + user_input
    cursor.execute(query)
    """

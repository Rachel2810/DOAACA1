def check_login(username, password):
    # Hardcoded for CA1 (can later integrate SQLite)
    return username == "admin" and password == "123"

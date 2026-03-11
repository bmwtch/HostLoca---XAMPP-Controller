# modules/user_manager.py
import subprocess
import os
import json

# Config in AppData\Roaming\HostLoca
CONFIG_PATH = os.path.join(os.getenv("APPDATA"), "HostLoca", "settings.json")

def load_settings():
    """
    Load settings from AppData\Roaming\HostLoca\settings.json.
    """
    defaults = {
        "xampp_path": "C:/xampp",
        "db_user": "root",
        "db_pass": ""
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = f.read().strip()
                if not data:
                    return defaults
                return json.loads(data)
        except Exception:
            return defaults
    return defaults

settings = load_settings()

XAMPP_PATH = settings.get("xampp_path", "C:/xampp")
MYSQL_BIN = os.path.join(XAMPP_PATH, "mysql", "bin", "mysql.exe")
PHPMYADMIN_CONFIG = os.path.join(XAMPP_PATH, "phpMyAdmin", "config.inc.php")

def _run_mysql_query(query, user="root", password=""):
    """
    Run a MySQL query using subprocess.
    """
    if password:
        cmd = f'"{MYSQL_BIN}" -u {user} -p{password} -e "{query}"'
    else:
        cmd = f'"{MYSQL_BIN}" -u {user} -e "{query}"'
    subprocess.run(cmd, shell=True, check=True)

def create_secure_user(username, password, root_pass=""):
    """
    Create a new secure MySQL user with full privileges.
    """
    _run_mysql_query(
        f"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}';",
        password=root_pass
    )
    _run_mysql_query(
        f"GRANT ALL PRIVILEGES ON *.* TO '{username}'@'localhost' WITH GRANT OPTION;",
        password=root_pass
    )
    _run_mysql_query("FLUSH PRIVILEGES;", password=root_pass)

def test_user_login(username, password):
    """
    Test login with new credentials by running a simple query.
    """
    try:
        cmd = f'"{MYSQL_BIN}" -u {username} -p{password} -e "SELECT 1;"'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def update_phpmyadmin_config(username, password):
    """
    Update phpMyAdmin config.inc.php with new credentials.
    """
    if not os.path.exists(PHPMYADMIN_CONFIG):
        raise FileNotFoundError("phpMyAdmin config.inc.php not found.")

    lines = []
    with open(PHPMYADMIN_CONFIG, "r") as f:
        for line in f:
            if "$cfg['Servers'][$i]['user']" in line:
                line = f"$cfg['Servers'][$i]['user'] = '{username}';\n"
            elif "$cfg['Servers'][$i]['password']" in line:
                line = f"$cfg['Servers'][$i]['password'] = '{password}';\n"
            lines.append(line)

    with open(PHPMYADMIN_CONFIG, "w") as f:
        f.writelines(lines)

def drop_default_users(root_pass=""):
    """
    Drop default MySQL accounts (root, anonymous).
    """
    defaults = [
        "DROP USER IF EXISTS 'root'@'localhost';",
        "DROP USER IF EXISTS 'root'@'127.0.0.1';",
        "DROP USER IF EXISTS ''@'localhost';",
        "DROP USER IF EXISTS ''@'127.0.0.1';"
    ]
    for query in defaults:
        _run_mysql_query(query, password=root_pass)
    _run_mysql_query("FLUSH PRIVILEGES;", password=root_pass)

def setup_secure_user(username, password, root_pass=""):
    """
    Full workflow: create > test > update phpMyAdmin > drop defaults.
    """
    create_secure_user(username, password, root_pass)

    if not test_user_login(username, password):
        raise RuntimeError("New user login failed. Aborting.")

    update_phpmyadmin_config(username, password)
    drop_default_users(root_pass)

    print(f"Secure user {username} set up successfully.")

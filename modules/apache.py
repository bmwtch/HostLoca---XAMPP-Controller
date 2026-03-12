# modules/apache.py
import os
import subprocess
import json

CONFIG_PATH = os.path.join(os.getenv("APPDATA"), "HostLoca", "settings.json")

def load_settings():
    """
    Load settings from settings.json in AppData.
    """
    defaults = {
        "xampp_path": "C:/xampp",
        "htdocs_path": "C:/xampp/htdocs"
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
HTTPD_CONF = os.path.join(XAMPP_PATH, "apache", "conf", "httpd.conf")
XAMPP_CONTROL = os.path.join(XAMPP_PATH, "xampp-control.exe")
APACHE_START = os.path.join(XAMPP_PATH, "apache_start.bat")
APACHE_STOP = os.path.join(XAMPP_PATH, "apache_stop.bat")

# def update_document_root(new_root):
#     """
#     Update Apache's httpd.conf to set a new DocumentRoot and Directory.
#     """
#     if not os.path.isdir(new_root):
#         raise ValueError(f"HTDOC folder {new_root} does not exist.")

#     if not os.path.exists(HTTPD_CONF):
#         raise FileNotFoundError("httpd.conf not found.")

#     lines = []
#     with open(HTTPD_CONF, "r") as f:
#         for line in f:
#             if line.strip().startswith("DocumentRoot"):
#                 line = f'DocumentRoot "{new_root.replace("\\", "/")}"\n'
#             elif line.strip().startswith("<Directory"):
#                 line = f'<Directory "{new_root.replace("\\", "/")}">\n'
#             lines.append(line)

#     with open(HTTPD_CONF, "w") as f:
#         f.writelines(lines)

#     print(f"DocumentRoot updated to {new_root}")

def update_document_root(new_root):
    """
    Update Apache's httpd.conf to set a new DocumentRoot and Directory.
    Also adds a wildcard <Directory> block to cover all subfolders.
    """
    if not os.path.isdir(new_root):
        raise ValueError(f"HTDOC folder {new_root} does not exist.")

    if not os.path.exists(HTTPD_CONF):
        raise FileNotFoundError("httpd.conf not found.")

    lines = []
    wildcard_block = (
        f'<Directory "{new_root.replace("\\", "/")}/*">\n'
        '    Options +FollowSymLinks +Indexes\n'
        '    AllowOverride All\n'
        '    Require all granted\n'
        '</Directory>\n'
    )

    with open(HTTPD_CONF, "r") as f:
        for line in f:
            if line.strip().startswith("DocumentRoot"):
                line = f'DocumentRoot "{new_root.replace("\\", "/")}"\n'
            elif line.strip().startswith("<Directory"):
                line = f'<Directory "{new_root.replace("\\", "/")}">\n'
            lines.append(line)

    if wildcard_block not in "".join(lines):
        lines.append("\n" + wildcard_block)

    with open(HTTPD_CONF, "w") as f:
        f.writelines(lines)

    print(f"DocumentRoot updated to {new_root} with wildcard directory access.")

def restart_apache():
    """
    Restart Apache service in XAMPP.
    """
    try:
        subprocess.run(APACHE_STOP, shell=True, check=True)
        subprocess.run(APACHE_START, shell=True, check=True)

        # Use xampp-control.exe with arguments (if supported)
        # subprocess.run(f'"{XAMPP_CONTROL}" restartapache', shell=True, check=True)

        print("Apache restarted successfully.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to restart Apache: {e}")

def set_htdocs(new_root):
    """
    Full workflow: update httpd.conf and restart Apache.
    """
    update_document_root(new_root)
    restart_apache()

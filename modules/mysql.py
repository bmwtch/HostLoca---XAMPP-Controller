# modules/mysql.py
import os
import subprocess
import gzip
import shutil
import json

CONFIG_PATH = os.path.join(os.getenv("APPDATA"), "HostLoca", "settings.json")

def load_settings():
    defaults = {
        "xampp_path": "C:/xampp",
        "db_user": "root",
        "db_pass": "",
        "db_host": "localhost"
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

DEFAULT_USER = settings.get("db_user", "root")
DEFAULT_PASS = settings.get("db_pass", "")
DEFAULT_HOST = settings.get("db_host", "localhost")

def _run_mysql_command(db_name, sql_file, user=DEFAULT_USER, password=DEFAULT_PASS, host=DEFAULT_HOST):
    """
    Run a MySQL import command for a given database and SQL file.
    """
    if password:
        cmd = f'"{MYSQL_BIN}" -u {user} -p{password} -h {host} {db_name} < "{sql_file}"'
    else:
        cmd = f'"{MYSQL_BIN}" -u {user} -h {host} {db_name} < "{sql_file}"'
    subprocess.run(cmd, shell=True, check=True)

def _create_database(db_name, user=DEFAULT_USER, password=DEFAULT_PASS, host=DEFAULT_HOST):
    """
    Create a database if it does not exist.
    """
    if password:
        cmd = f'"{MYSQL_BIN}" -u {user} -p{password} -h {host} -e "CREATE DATABASE IF NOT EXISTS {db_name};"'
    else:
        cmd = f'"{MYSQL_BIN}" -u {user} -h {host} -e "CREATE DATABASE IF NOT EXISTS {db_name};"'
    subprocess.run(cmd, shell=True, check=True)

def _decompress_gz(gz_file):
    """
    Decompress a .sql.gz file into a temporary .sql file.
    """
    sql_file = gz_file.replace(".gz", "")
    with gzip.open(gz_file, "rb") as f_in, open(sql_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    return sql_file

def import_sql_folder(sql_folder, user=DEFAULT_USER, password=DEFAULT_PASS, host=DEFAULT_HOST):
    """
    Scan a folder for .sql and .sql.gz files, create databases, and import them.
    """
    if not os.path.isdir(sql_folder):
        raise ValueError(f"SQL folder {sql_folder} does not exist.")

    for file in os.listdir(sql_folder):
        if file.endswith(".sql") or file.endswith(".sql.gz"):
            file_path = os.path.join(sql_folder, file)
            db_name = file.replace(".sql.gz", "").replace(".sql", "")
            print(f"Processing {file} → Database: {db_name}")
            _create_database(db_name, user, password, host)
            if file.endswith(".gz"):
                sql_file = _decompress_gz(file_path)
            else:
                sql_file = file_path

            _run_mysql_command(db_name, sql_file, user, password, host)

            print(f"Imported {file} into {db_name}")

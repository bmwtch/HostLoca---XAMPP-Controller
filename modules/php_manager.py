
# modules/php_manager.py

import os
import shutil
import zipfile
import json
import subprocess

def get_paths(settings):
    xampp_path = settings.get("xampp_path", "C:/xampp")
    loca_php = os.path.join(xampp_path, "LocaPHP")
    active_php = os.path.join(xampp_path, "php")
    config_file = os.path.join(loca_php, "versions.json")
    return xampp_path, loca_php, active_php, config_file

def detect_php_version(path):
    php_exe = os.path.join(path, "php.exe")
    if not os.path.exists(php_exe):
        return None
    try:
        output = subprocess.check_output([php_exe, "-v"], text=True)
        if output.startswith("PHP"):
            return output.split()[1]
    except Exception:
        return None
    return None

def install_php_zip(zip_path, settings):
    xampp_path, loca_php, active_php, config_file = get_paths(settings)
    os.makedirs(loca_php, exist_ok=True)
    temp_dir = os.path.join(loca_php, "temp_extract")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    version = detect_php_version(temp_dir)
    if not version:
        shutil.rmtree(temp_dir)
        raise Exception("Invalid or corrupted PHP ZIP")
    target_dir = os.path.join(loca_php, version)
    shutil.move(temp_dir, target_dir)
    register_version(version, target_dir, config_file)
    return version

def register_version(version, path, config_file):
    versions = {}
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            versions = json.load(f)
    versions[version] = path
    with open(config_file, "w") as f:
        json.dump(versions, f, indent=4)

def get_registered_versions(settings):
    _, _, _, config_file = get_paths(settings)
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return list(json.load(f).keys())
    return []

def switch_php_version(version, settings):
    xampp_path, loca_php, active_php, config_file = get_paths(settings)
    with open(config_file, "r") as f:
        versions = json.load(f)
    if version not in versions:
        raise Exception("Version is not installed")
    if os.path.exists(active_php):
        if os.path.islink(active_php):
            os.unlink(active_php)
        else:
            shutil.rmtree(active_php)
    try:
        os.symlink(versions[version], active_php)
    except OSError:
        shutil.copytree(versions[version], active_php)
    setup_php_ini(active_php, versions[version])
    return version

def setup_php_ini(active_php, version_path):
    ini_dev = os.path.join(version_path, "php.ini-development")
    ini_prod = os.path.join(version_path, "php.ini-production")
    ini_target = os.path.join(active_php, "php.ini")
    if os.path.exists(ini_prod):
        shutil.copy(ini_prod, ini_target)
    elif os.path.exists(ini_dev):
        shutil.copy(ini_dev, ini_target)
    with open(ini_target, "a") as f:
        f.write("\n; HostLoca overrides\n")
        f.write("extension_dir = \"ext\"\n")
        f.write("upload_max_filesize = 64M\n")

def check_fallback(settings):
    xampp_path, loca_php, active_php, config_file = get_paths(settings)
    if not os.path.exists(active_php):
        default_php = os.path.join(xampp_path, "php_default")
        if os.path.exists(default_php):
            shutil.copytree(default_php, active_php)
            shutil.copy(os.path.join(default_php, "php.ini"), os.path.join(active_php, "php.ini"))
            return "Fallback: Restored default XAMPP PHP"
    return None

from flask import Blueprint, current_app
from flask_login import login_required
import subprocess
from flask import current_app
import os
import shutil
from datetime import datetime

from utils.auth import admin_required

backup_bp = Blueprint(
    "backup",
    __name__,
    url_prefix="/backup"
)


@backup_bp.route("/")
@login_required
@admin_required
def index():
    return "<h2>Backup Module Working</h2>"



@backup_bp.route("/create")
@login_required
@admin_required
def create_backup():

    backup_folder = os.path.join(
        current_app.root_path,
        "backups"
    )

    os.makedirs(backup_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_file = os.path.join(
        backup_folder,
        f"esa_backup_{timestamp}.sql"
    )

    mysqldump = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

    command = [
        mysqldump,
        "-u", "root",
        "-pProperty48",
        "esa_db"
    ]

    with open(backup_file, "w", encoding="utf-8") as outfile:
        result = subprocess.run(
            command,
            stdout=outfile,
            stderr=subprocess.PIPE,
            text=True
        )

    if result.returncode != 0:
        return f"Backup failed:<br><pre>{result.stderr}</pre>"

    return (
        f"Backup created successfully!<br>"
        f"{os.path.basename(backup_file)}"
    )

    db_path = os.path.join(
        current_app.instance_path,
        "..",
        "esa.db"
    )

    db_path = os.path.abspath(db_path)

    backup_folder = os.path.join(
        current_app.root_path,
        "backups"
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = os.path.join(
        backup_folder,
        f"esa_backup_{timestamp}.db"
    )

    shutil.copy2(db_path, backup_file)

    return f"Backup created successfully:<br>{os.path.basename(backup_file)}"
import os
import subprocess
import time
from datetime import datetime


def create_backup(backup_dir):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{backup_dir}/backup_{timestamp}.sql"
    try:
        result = subprocess.run(
            [
                "pg_dump",
                "-h", "localhost",
                "-p", "30000",
                "-U", os.getenv("POSTGRES_USER"),
                "-d", os.getenv("POSTGRES_DB"),
                "-f", backup_file
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def cleanup_backups(backup_dir, max_backups):
    backups = sorted(os.listdir(backup_dir), key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
    if len(backups) > max_backups:
        for old_backup in backups[:-max_backups]:
            os.remove(os.path.join(backup_dir, old_backup))


if __name__ == "__main__":
    backup_interval_hours = int(os.getenv("BACKUP_INTERVAL_HOURS", 24))
    max_backups_to_keep = int(os.getenv("MAX_BACKUPS_TO_KEEP", 5))
    backup_dir = os.getenv("BACKUP_DIR", "/backups")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    while True:
        backup_file = create_backup(backup_dir)
        if backup_file:
            print(f"Created backup: {backup_file}")
            cleanup_backups(backup_dir, max_backups_to_keep)
            print("Cleaned up old backups.")
        else:
            print("Backup creation failed.")
        time.sleep(backup_interval_hours * 3600)

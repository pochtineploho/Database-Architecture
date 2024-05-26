import os
import subprocess
import time
from datetime import datetime

def create_backup(backup_dir):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{backup_dir}/backup_{timestamp}.sql"
    try:
        subprocess.run(
            ["pg_dump",
             "-h", "postgres",
             "-p", "5432",
             "-U", os.getenv("POSTGRES_USER"),
             "-d", os.getenv("POSTGRES_DB"),
             "-f", backup_file],
        env={"PGPASSWORD": os.getenv("POSTGRES_PASSWORD")},)
        return backup_file
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None


def cleanup_backups(backup_dir, max_backups):
    backups = sorted(os.listdir(backup_dir), key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
    if len(backups) > max_backups:
        for old_backup in backups[:-max_backups]:
            os.remove(os.path.join(backup_dir, old_backup))


if __name__ == "__main__":
    print("Starting backup script...")
    backup_interval_hours = int(os.getenv("BACKUP_INTERVAL", 3))
    max_backups_to_keep = int(os.getenv("MAX_BACKUPS", 3))
    backup_dir = os.getenv("BACKUP_DIR", "/backups")

    print(f"Backup interval: {backup_interval_hours} hours")
    print(f"Max backups to keep: {max_backups_to_keep}")
    print(f"Backup directory: {backup_dir}")
    print(f"Postgres DB: {os.getenv('POSTGRES_DB')}")
    print(f"Postgres User: {os.getenv('POSTGRES_USER')}")
    print(f"Postgres Port: {os.getenv('POSTGRES_PORT')}")
    print(f"Backup Dir exists: {os.path.exists(backup_dir)}")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}")

    print("Starting backups...")
    while True:
        backup_file = create_backup(backup_dir)
        if backup_file:
            print(f"Created backup: {backup_file}")
            cleanup_backups(backup_dir, max_backups_to_keep)
            print("Cleaned up old backups.")
        else:
            print("Backup creation failed.")
        time.sleep(backup_interval_hours * 3600)

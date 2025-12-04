import os
import subprocess
import datetime
import time
import sys

# ---------- CONFIGURATION ----------
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")
USER = os.getenv("DB_USER", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "password")

# Backup directory
BACKUP_DIR = "/backups"   # inside container but mounted to host

# Backup time
BACKUP_HOUR = 2   # 2 AM
BACKUP_MINUTE = 0


def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    BACKUP_FILE = f"{DB_NAME}_backup_{timestamp}.dump"
    BACKUP_PATH = os.path.join(BACKUP_DIR, BACKUP_FILE)

    os.environ["PGPASSWORD"] = PASSWORD

    dump_command = [
        "pg_dump",
        f"--host={HOST}",
        f"--port={PORT}",
        f"--username={USER}",
        "--format=custom",
        "--verbose",
        f"--file={BACKUP_PATH}",
        DB_NAME
    ]

    print(f"🚀 Running backup... {BACKUP_PATH}")
    result = subprocess.run(dump_command, text=True)

    if result.returncode == 0:
        print("✅ Backup created")
    else:
        print("❌ Backup failed")

    sys.exit(0)


def wait_until_backup_time():
    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=BACKUP_HOUR, minute=BACKUP_MINUTE,
                             second=0, microsecond=0)

        if now >= target:
            target += datetime.timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        print(f"⏳ Waiting {int(wait_seconds)} seconds for next backup…")
        time.sleep(wait_seconds)
        create_backup()


if __name__ == "__main__":
    wait_until_backup_time()

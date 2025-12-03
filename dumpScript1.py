import os
import subprocess
import datetime
import time
import sys

# ---------- CONFIGURATION ----------
HOST = "localhost"
PORT = "5432"
USER = "postgres"
DB_NAME = "logia360"
PASSWORD = "post@2000"  # agar environment variable nahi use karna

# Backup directory
BACKUP_DIR = r"C:\Users\Administrator\Desktop\New folder\Python"

# Backup time
BACKUP_HOUR = 2   # 2 AM
BACKUP_MINUTE = 0


def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    BACKUP_FILE = f"brickproduction_backup_{timestamp}.dump"
    BACKUP_PATH = os.path.join(BACKUP_DIR, BACKUP_FILE)

    # Set password
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

    print(f"🚀 Running backup... File will be saved at:\n{BACKUP_PATH}\n")

    result = subprocess.run(dump_command, text=True)

    if result.returncode == 0:
        print("✅ Backup created successfully!")
    else:
        print("❌ Backup failed!")

    print("🛑 Backup finished, script exiting.")
    sys.exit(0)  # backup ke baad script close ho jaye


def wait_until_backup_time():
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(
            hour=BACKUP_HOUR, minute=BACKUP_MINUTE, second=0, microsecond=0)

        # agar current time 2 AM ke baad hai, next day ka target set karo
        if now >= target_time:
            target_time += datetime.timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        print(f"⏳ Waiting {int(wait_seconds)} seconds until 2 AM backup...")
        time.sleep(wait_seconds)

        # Run backup at target time
        create_backup()


if __name__ == "__main__":
    wait_until_backup_time()

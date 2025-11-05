import os
import time
import requests
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MASTER_URL = os.getenv("SEAWEED_MASTER_URL", "http://master:9333")
FILER_URL = os.getenv("SEAWEED_VOLUME_URL", "http://filer:8888")
WATCH_DIR = "/watched"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            logger.info(f"New file detected: {file_path}")
            upload_file(file_path)
            log_storage_status()

def upload_file(file_path):
    """Upload a file via the SeaweedFS filer and log the FID/URL."""
    try:
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            resp = requests.post(f"{FILER_URL}/", files=files)
            if resp.status_code in [200, 201]:
                logger.info(f"Uploaded {filename} to filer: {FILER_URL}")
                try:
                    data = resp.json()
                    fid = data.get("fid")
                    if fid:
                        logger.info(f"File FID: {fid}")
                        logger.info(f"Direct download URL: {FILER_URL}/{fid}")
                except Exception:
                    logger.info(f"Filer response: {resp.text}")
            else:
                logger.error(f"Upload failed: {resp.status_code} {resp.text}")
    except Exception as e:
        logger.exception(f"Exception during upload: {e}")

def log_storage_status():
    """Query the SeaweedFS master for cluster status and log used storage."""
    try:
        resp = requests.get(f"{MASTER_URL}/cluster/status")
        if resp.status_code == 200:
            data = resp.json()
            total_used = 0
            for volume in data.get("Volumes", []):
                total_used += volume.get("Size", 0)
            logger.info(f"Total used storage: {total_used / 1024**3:.2f} GB")
        else:
            logger.error(f"Failed to query cluster: {resp.text}")
    except Exception as e:
        logger.exception(f"Exception querying cluster: {e}")

if __name__ == "__main__":
    logger.info("Starting SeaweedFS file monitor service...")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

import os, time,random
from datetime import datetime

WATCH_DIR = "watched"

def main():
    os.makedirs(WATCH_DIR, exist_ok=True)
    while True:
        filename = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(WATCH_DIR, filename)
        with open(filepath, "w") as f:
            f.write(f"Generated at {datetime.now()}\n")
        print(f"[HOST] Created new file: {filename}")
        sleep_time = random.randint(30, 60)
        time.sleep(sleep_time)

if __name__ == "__main__":
    print("[HOST] File generator started...")
    main()
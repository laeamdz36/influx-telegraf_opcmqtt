import os
import time
import random
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("INFLUX_URL")
TOKEN = os.getenv("INFLUX_TOKEN")
ORG = os.getenv("INFLUX_ORG")
BUCKET = os.getenv("INFLUX_BUCKET")
MEASUREMENT = os.getenv("MEASUREMENT", "random_sensor")
INTERVAL = int(os.getenv("WRITE_INTERVAL", "10"))

write_url = f"{URL}/api/v3/write?bucket={BUCKET}&org={ORG}&format=line"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "text/plain"
}


def run():
    while True:
        value = random.uniform(0, 100)
        line = f"{MEASUREMENT} value={value}"

        r = requests.post(write_url, data=line, headers=headers)
        if r.status_code in (200, 204):
            print(f"✅ {line}")
        else:
            print(f"❌ {r.status_code}: {r.text}")

        time.sleep(INTERVAL)

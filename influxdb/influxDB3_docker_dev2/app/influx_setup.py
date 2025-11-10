import os
import requests

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb3-core:8181")
ORG = os.getenv("INFLUX_ORG", "myorg")
BUCKET = os.getenv("INFLUX_BUCKET", "mybucket")
TOKEN = os.getenv("INFLUX_TOKEN")   # Si ya tienes token
ADMIN_TOKEN = os.getenv("INFLUX_ADMIN_TOKEN")  # Token inicial privilegiado

headers_admin = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}


def create_org():
    r = requests.post(f"{INFLUX_URL}/api/v3/orgs",
                      headers=headers_admin,
                      json={"name": ORG})
    if r.status_code in (200, 201, 409):
        print("✅ Org OK")
    else:
        print("❌ Org error:", r.text)


def create_bucket():
    r = requests.post(f"{INFLUX_URL}/api/v3/buckets?org={ORG}",
                      headers=headers_admin,
                      json={"name": BUCKET})
    if r.status_code in (200, 201, 409):
        print("✅ Bucket OK")
    else:
        print("❌ Bucket error:", r.text)


def create_token():
    r = requests.post(f"{INFLUX_URL}/api/v3/access_tokens",
                      headers=headers_admin,
                      json={"description": "writer", "status": "active"})
    if r.status_code in (200, 201):
        token = r.json().get("token")
        print(f"✅ Token creado: {token}")
        return token
    elif r.status_code == 409:
        print("✅ Token ya existe")
    else:
        print("❌ Token error:", r.text)


def influx_setup():
    print("🔧 Ejecutando setup InfluxDB 3…")
    create_org()
    create_bucket()
    create_token()

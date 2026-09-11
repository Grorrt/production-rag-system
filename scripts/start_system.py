"""
Starts the full RAG system locally for development.
Starts backend server and runs all endpoint tests.
"""

import sys, os, threading, time

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

print("=" * 60)
print("  Production RAG System — Starting...")
print("=" * 60)


def run_server():
    import sys
    sys.path.insert(0, PROJECT_ROOT)
    from backend.app.main import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

for i in range(10):
    time.sleep(1)
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:8000/api/health", timeout=2)
        if r.status_code == 200:
            print("  Server is ready!")
            break
    except Exception:
        if i < 9:
            print(f"  Waiting for server... ({i+1}/10)")
else:
    print("  Server failed to start!")
    sys.exit(1)

BASE = "http://127.0.0.1:8000"

print("\n1. Health Check:")
r = httpx.get(f"{BASE}/api/health")
print(f"   {r.status_code}: OK")

print("\n2. Register User:")
r = httpx.post(f"{BASE}/api/auth/register",
    json={"username": "demo", "password": "demo123456"})
print(f"   {r.status_code}: {r.json()['message']}")

print("\n3. Login:")
r = httpx.post(f"{BASE}/api/auth/login",
    json={"username": "demo", "password": "demo123456"})
token = r.json()["access_token"]
print(f"   {r.status_code}: Token obtained")

print("\n4. Ask Question:")
headers = {"Authorization": f"Bearer {token}"}
r = httpx.post(f"{BASE}/api/query/chat",
    json={"question": "What is React?", "stream": False},
    headers=headers, timeout=60)
print(f"   {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Answer: {data['answer'][:200]}...")
    print(f"   Sources: {data['source_count']}")
else:
    print(f"   Response: {r.text[:300]}")

print("\n5. API Docs:")
print(f"   Swagger UI: http://localhost:8000/docs")
print(f"   ReDoc:      http://localhost:8000/redoc")

print("\n" + "=" * 60)
print("  System is running on http://localhost:8000")
print("  Press Ctrl+C to stop")
print("=" * 60)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSystem stopped.")

#!/usr/bin/env python3
"""
Script để test routes của face_id module
"""
import requests
import sys

base_url = "http://localhost:8069"

routes_to_test = [
    "/face_checkin",
    "/face_checkout",
    "/face_register?nhan_vien_id=1",
]

print("Testing Face ID routes...")
print("=" * 50)

for route in routes_to_test:
    url = base_url + route
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)
        print(f"Route: {route}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Route is accessible")
        elif response.status_code == 302 or response.status_code == 303:
            print("→ Route redirects (may require login)")
        elif response.status_code == 404:
            print("✗ Route not found")
        else:
            print(f"→ Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to {base_url}")
        print("  Make sure Odoo server is running")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
    print("-" * 50)

print("\nNote: If routes return 404, you may need to:")
print("1. Restart Odoo server")
print("2. Upgrade the face_id module")
print("3. Check if website module is installed")

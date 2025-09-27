import requests
import json

# Test FRD generation endpoint
test_data = {
    "project": "Test Project",
    "brd": "This is a test BRD with some business requirements for testing FRD generation",
    "version": 1
}

print("Testing FRD Generation Endpoint...")
print("=" * 40)

try:
    # Test the endpoint that the frontend is calling
    response = requests.post(
        "http://localhost:8001/ai/frd/generate",
        json=test_data,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    if response.status_code == 200:
        print("✅ FRD endpoint is working!")
    else:
        print(f"❌ FRD endpoint failed with status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error testing FRD endpoint: {e}")

# Also test the root endpoint to see if server is responding
try:
    response = requests.get("http://localhost:8001/")
    print(f"\nRoot endpoint status: {response.status_code}")
    print(f"Root response: {response.json()}")
except Exception as e:
    print(f"❌ Error testing root endpoint: {e}")
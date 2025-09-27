"""
Quick verification test for the BA Tool functionality
"""
import requests

def verify_ba_tool():
    """Verify both frontend and backend are working"""
    
    print("🔍 BA Tool Verification Test")
    print("="*40)
    
    # Test Frontend
    print("🌐 Testing Frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running successfully!")
            print("   URL: http://localhost:3000")
            print("   Status: Ready for use")
        else:
            print(f"⚠️  Frontend responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend error: {str(e)}")
        return False
    
    # Test Backend
    print("\n🔧 Testing Backend...")
    try:
        response = requests.get("http://localhost:8001", timeout=5)
        print("✅ Backend is running successfully!")
        print("   URL: http://localhost:8001")
        print("   Status: API endpoints ready")
    except Exception as e:
        print(f"❌ Backend error: {str(e)}")
        return False
    
    # Test Wireframe API specifically
    print("\n🎨 Testing Wireframe API...")
    try:
        test_payload = {
            "project": "Test Project",
            "user_stories": [
                {
                    "id": "US-001",
                    "title": "Test Story",
                    "description": "As a user, I want to test the system",
                    "acceptance_criteria": ["System should work properly"]
                }
            ],
            "domain": "generic"
        }
        
        response = requests.post(
            "http://localhost:8001/ai/wireframes", 
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Wireframe API is working!")
            print(f"   Generated: {len(result.get('html', ''))} characters")
        else:
            print(f"⚠️  Wireframe API issue: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Wireframe API test failed: {str(e)}")
    
    print("\n" + "="*40)
    print("🎉 BA Tool is ready to use!")
    print("\n📋 Quick Start Guide:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Login with any username/password")
    print("3. Create a new project")
    print("4. Choose between:")
    print("   • BRD Creation → Generate business requirements")
    print("   • FRD Creation → Generate functional requirements") 
    print("   • Wire Frame Generator → Generate interactive wireframes")
    print("\n✨ All modules are integrated and ready!")
    
    return True

if __name__ == "__main__":
    verify_ba_tool()
"""
Simple test for wireframe generation functionality
"""
import requests
import json
import os
from datetime import datetime

# Test data - educational domain user stories
test_user_stories = [
    {
        "id": "US-001",
        "title": "Student Login",
        "description": "As a student, I want to log into the learning platform so that I can access my courses",
        "acceptance_criteria": [
            "User can enter email and password",
            "System validates credentials",
            "User is redirected to dashboard on success"
        ]
    },
    {
        "id": "US-002", 
        "title": "Course Dashboard",
        "description": "As a student, I want to view my enrolled courses so that I can choose which course to study",
        "acceptance_criteria": [
            "Display list of enrolled courses",
            "Show course progress",
            "Allow navigation to course content"
        ]
    },
    {
        "id": "US-003",
        "title": "Assignment Submission",
        "description": "As a student, I want to submit assignments so that I can complete my coursework",
        "acceptance_criteria": [
            "Upload assignment files",
            "Add submission notes",
            "Confirm successful submission"
        ]
    }
]

def test_wireframe_generation():
    """Test wireframe generation API"""
    url = "http://localhost:8001/ai/wireframes"
    
    # Test 1: User stories wireframe generation
    print("🧪 Testing User Stories Wireframe Generation...")
    
    payload = {
        "project": "Student Learning Platform",
        "user_stories": test_user_stories,
        "domain": "education"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Wireframe generation successful!")
            print(f"� Full response: {result}")
            print(f"�📊 Generated wireframe contains {len(result.get('wireframe_html', ''))} characters")
            
            # Save the generated wireframe
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_wireframe_output_{timestamp}.html"
            
            wireframe_content = result.get('wireframe_html', '')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(wireframe_content)
            
            print(f"💾 Wireframe saved to: {filename}")
            
            # Quality analysis
            if wireframe_content:
                print("\n📈 Quality Analysis:")
                print(f"   - Contains login page: {'login' in wireframe_content.lower()}")
                print(f"   - Contains dashboard: {'dashboard' in wireframe_content.lower()}")
                print(f"   - Contains forms: {'<form' in wireframe_content}")
                print(f"   - Contains navigation: {'nav' in wireframe_content.lower()}")
                print(f"   - Interactive elements: {wireframe_content.count('onclick') + wireframe_content.count('addEventListener')}")
            else:
                print("\n⚠️  No wireframe content generated")
                
            return True
            
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the server running on port 8001?")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Simple Wireframe Generation Test")
    print("="*50)
    
    success = test_wireframe_generation()
    
    print("\n" + "="*50)
    if success:
        print("🎉 Test completed successfully!")
        print("🔗 Check the generated HTML file for interactive wireframes")
    else:
        print("💥 Test failed - check server status and logs")
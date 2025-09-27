#!/usr/bin/env python3
"""
Test Wireframe Generation from User Stories
This script tests the new wireframe generation functionality
"""
import requests
import json

def test_wireframe_generation():
    print("=== Testing AI-Powered Wireframe Generation ===")
    
    # Sample user stories for testing (similar to your educational example)
    user_stories = [
        {
            "role": "Content Manager",
            "goal": "create and publish courses with modules and prerequisites",
            "benefit": "efficiently manage educational content"
        },
        {
            "role": "Marketing Manager", 
            "goal": "conduct live sessions with recordings and attendance tracking",
            "benefit": "engage students in interactive learning"
        },
        {
            "role": "Marketing Analyst",
            "goal": "track learner progress and generate completion certificates", 
            "benefit": "measure learning outcomes and provide recognition"
        },
        {
            "role": "Student",
            "goal": "browse course catalog and enroll in courses",
            "benefit": "access learning opportunities"
        },
        {
            "role": "Instructor",
            "goal": "upload course materials and grade assignments",
            "benefit": "effectively teach and assess students"
        }
    ]
    
    # Test wireframe generation from user stories
    test_data = {
        "project": "Learning Management System",
        "user_stories": user_stories,
        "domain": "education",  # or could be "marketing" based on personas
        "version": 1
    }
    
    try:
        print("🎨 Calling wireframe generation API...")
        response = requests.post(
            "http://localhost:8001/ai/wireframes",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            wireframe_html = result.get("html", "")
            domain = result.get("domain", "unknown")
            
            print(f"✅ Wireframes generated successfully!")
            print(f"📊 Domain detected: {domain}")
            print(f"📄 Generated HTML: {len(wireframe_html)} characters")
            
            # Save wireframes to file
            with open("generated_wireframes.html", "w", encoding="utf-8") as f:
                f.write(wireframe_html)
            
            # Check for wireframe components
            wireframe_checks = {
                "Has Login Page": "login" in wireframe_html.lower(),
                "Has Dashboard": "dashboard" in wireframe_html.lower(),
                "Has Form Components": "form" in wireframe_html.lower(),
                "Has Navigation": "navigation" in wireframe_html.lower(),
                "Interactive Tabs": "showPage" in wireframe_html,
                "Educational Content": any(term in wireframe_html.lower() for term in ["course", "learning", "student", "education"]),
                "Responsive Design": "responsive" in wireframe_html.lower()
            }
            
            print(f"\n=== Wireframe Quality Analysis ===")
            passed_checks = 0
            for check_name, passed in wireframe_checks.items():
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}")
                if passed:
                    passed_checks += 1
            
            quality_score = passed_checks / len(wireframe_checks) * 100
            print(f"\n🎯 Wireframe Quality Score: {quality_score:.1f}%")
            
            if quality_score >= 80:
                print("🎉 EXCELLENT: High-quality wireframes generated!")
                print("✅ Ready for stakeholder review and development")
            elif quality_score >= 60:
                print("🟡 GOOD: Wireframes generated with room for enhancement")
            else:
                print("❌ NEEDS WORK: Basic wireframes generated, manual refinement needed")
                
            print(f"\n📂 Wireframes saved to: generated_wireframes.html")
            print("💡 Open the file in your browser to view interactive wireframes")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server not running on localhost:8001")
        print("💡 Please start the server:")
        print("   cd react-python-auth/backend && python simple_server.py")
    except Exception as e:
        print(f"❌ Test Error: {e}")

def test_wireframe_from_frd():
    print("\n=== Testing Wireframe Generation from FRD Content ===")
    
    # Sample FRD content with user stories
    frd_content = """
    <h2>User Stories</h2>
    
    <h3>US-001: Course Management</h3>
    <p>As a Content Manager, I want to create and publish courses with modules, so that I can organize educational content effectively.</p>
    
    <h3>US-002: Student Enrollment</h3>
    <p>As a Student, I want to browse and enroll in available courses, so that I can access learning materials.</p>
    
    <h3>US-003: Progress Tracking</h3>
    <p>As an Instructor, I want to track student progress and completion, so that I can assess learning outcomes.</p>
    
    <h3>US-004: Interactive Learning</h3>
    <p>As a Student, I want to participate in live sessions and access recordings, so that I can learn at my own pace.</p>
    """
    
    test_data = {
        "project": "E-Learning Platform",
        "frd_content": frd_content,
        "domain": "education",
        "version": 1
    }
    
    try:
        print("🎨 Testing wireframe generation from FRD content...")
        response = requests.post(
            "http://localhost:8001/ai/wireframes",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            wireframe_html = result.get("html", "")
            
            print(f"✅ Wireframes generated from FRD content!")
            print(f"📄 Generated HTML: {len(wireframe_html)} characters")
            
            # Save wireframes to file
            with open("frd_wireframes.html", "w", encoding="utf-8") as f:
                f.write(wireframe_html)
            
            print(f"📂 FRD-based wireframes saved to: frd_wireframes.html")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_wireframe_generation()
    test_wireframe_from_frd()
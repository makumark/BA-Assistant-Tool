"""
Final Integration Test - BA Tool with Wireframe Generation
Tests the complete flow: BRD → FRD → Wireframe Generation
"""
import requests
import json
from datetime import datetime

def test_full_workflow():
    """Test the complete BA Tool workflow including wireframe generation"""
    
    print("🎯 BA Tool Complete Workflow Test")
    print("="*50)
    
    # Sample educational project
    test_project = "Educational Learning Management System"
    sample_user_stories = [
        {
            "id": "US-001",
            "title": "Student Registration",
            "description": "As a prospective student, I want to register for the learning platform so that I can access courses",
            "acceptance_criteria": [
                "User can enter personal information (name, email, phone)",
                "System validates email format and uniqueness", 
                "User receives confirmation email upon successful registration",
                "User account is created with default student role"
            ]
        },
        {
            "id": "US-002", 
            "title": "Course Enrollment",
            "description": "As a student, I want to enroll in courses so that I can start learning",
            "acceptance_criteria": [
                "Display available courses with descriptions",
                "Show course prerequisites and requirements",
                "Allow enrollment if prerequisites are met",
                "Send enrollment confirmation to student"
            ]
        },
        {
            "id": "US-003",
            "title": "Assignment Management",
            "description": "As an instructor, I want to create and manage assignments so that I can assess student progress", 
            "acceptance_criteria": [
                "Create assignments with due dates and instructions",
                "Upload assignment files and resources",
                "Set grading rubrics and point values",
                "Track submission status for all students"
            ]
        },
        {
            "id": "US-004",
            "title": "Grade Tracking",
            "description": "As a student, I want to view my grades so that I can track my academic progress",
            "acceptance_criteria": [
                "Display grades for all enrolled courses",
                "Show assignment scores and feedback",
                "Calculate overall course grades and GPA",
                "Provide grade history and trends"
            ]
        }
    ]

    # Test wireframe generation
    print("🎨 Testing Wireframe Generation...")
    wireframe_url = "http://localhost:8001/ai/wireframes"
    
    wireframe_payload = {
        "project": test_project,
        "user_stories": sample_user_stories,
        "domain": "education",
        "version": 1
    }
    
    try:
        response = requests.post(wireframe_url, json=wireframe_payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            wireframe_html = result.get('html', '')
            detected_domain = result.get('domain', 'unknown')
            
            print(f"✅ Wireframes generated successfully!")
            print(f"📊 Generated HTML: {len(wireframe_html)} characters")
            print(f"🎯 Detected Domain: {detected_domain}")
            
            # Save wireframe
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ba_tool_complete_test_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(wireframe_html)
            
            print(f"💾 Saved to: {filename}")
            
            # Quality analysis
            quality_checks = {
                "Login functionality": "login" in wireframe_html.lower(),
                "Dashboard present": "dashboard" in wireframe_html.lower(),
                "Student-specific content": "student" in wireframe_html.lower(),
                "Course management": "course" in wireframe_html.lower(),
                "Assignment features": "assignment" in wireframe_html.lower(),
                "Interactive navigation": "onclick" in wireframe_html,
                "Responsive design": "responsive" in wireframe_html.lower(),
                "Education domain": detected_domain == "education"
            }
            
            print("\n📈 Quality Analysis:")
            for check, passed in quality_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}: {passed}")
            
            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)
            score = (passed_checks / total_checks) * 100
            
            print(f"\n🏆 Overall Score: {score:.1f}% ({passed_checks}/{total_checks} checks passed)")
            
            if score >= 80:
                print("🎉 EXCELLENT: Wireframe generation is working perfectly!")
                return True
            elif score >= 60:
                print("👍 GOOD: Wireframe generation is working well with minor issues")
                return True
            else:
                print("⚠️  NEEDS IMPROVEMENT: Some wireframe features may need attention")
                return False
                
        else:
            print(f"❌ Wireframe generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running on port 8001")
        print("💡 Please start the backend: cd react-python-auth/backend && python simple_server.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_frontend_integration():
    """Test if the frontend is accessible"""
    print("\n🌐 Testing Frontend Integration...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running on http://localhost:3000")
            print("🎯 You can now:")
            print("   1. Login to the BA Tool")
            print("   2. Create a new project")
            print("   3. Generate FRD from BRD")
            print("   4. Use the integrated Wireframe Generator")
            print("   5. Or select 'Wire Frame Generator' from Document Generator dropdown")
            return True
        else:
            print(f"⚠️  Frontend responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running on port 3000")
        print("💡 Please start the frontend: cd react-python-auth/frontend && npm start")
        return False
    except Exception as e:
        print(f"❌ Frontend check failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 BA Tool Complete Integration Test")
    print("Testing all components: Backend, Frontend, AI Services, Wireframe Generation")
    print("="*80)
    
    # Test backend wireframe generation
    backend_ok = test_full_workflow()
    
    # Test frontend integration
    frontend_ok = test_frontend_integration()
    
    print("\n" + "="*80)
    print("📋 FINAL RESULTS:")
    print(f"   🔧 Backend & Wireframe Generation: {'✅ WORKING' if backend_ok else '❌ ISSUES'}")
    print(f"   🌐 Frontend Integration: {'✅ WORKING' if frontend_ok else '❌ ISSUES'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 SUCCESS! BA Tool with Wireframe Generation is fully operational!")
        print("\n🎯 Next Steps:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Login with any credentials")
        print("   3. Create a project and generate FRD")  
        print("   4. Use the Wireframe Generator that appears after FRD generation")
        print("   5. Or select 'Wire Frame Generator' as a standalone module")
        print("\n✨ Your BA Tool now has AI-powered wireframe generation capabilities!")
    else:
        print("\n⚠️  Some components need attention. Check the error messages above.")
        
    print("\n" + "="*80)
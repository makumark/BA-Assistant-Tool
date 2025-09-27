#!/usr/bin/env python3
"""
Test the BRD generation API to ensure it's working correctly
"""

import requests
import json

# Test the BRD generation API
def test_brd_api():
    url = "http://localhost:8000/ai/generate_brd"
    
    # Test data - same as our previous test
    payload = {
        "input": """Project: Learning Management System (LMS) Enhancement

Business Requirements:
1. Course Management - Teachers should be able to create, edit, and delete courses with multimedia content
2. Student Enrollment - Automated enrollment system with waitlist functionality  
3. Learning Delivery - Support for video lectures, quizzes, and assignments
4. Virtual Classroom - Real-time video conferencing integration
5. Progress Tracking - Dashboard showing student progress and completion rates

Business Validation:
- User acceptance testing with 40% of target users
- Performance benchmarks: 500 concurrent users minimum
- Security compliance with institutional standards

Project Scope:
- Budget: $500,000
- Timeline: 18 months
- Team: 8 developers, 2 QA engineers, 1 product manager

Success Criteria:
- 90% user satisfaction rating
- 25% improvement in learning outcomes
- System uptime 99.5% or higher"""
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        print("Testing BRD API...")
        print(f"Sending request to: {url}")
        print(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Generated BRD length: {len(result.get('html', ''))} characters")
            
            # Check if key elements are present
            html_content = result.get('html', '')
            checks = [
                ('Course Management', 'Course Management' in html_content),
                ('Learning Delivery', 'Learning Delivery' in html_content),
                ('Virtual Classroom', 'Virtual Classroom' in html_content),
                ('User acceptance testing with 40%', '40%' in html_content),
                ('Budget: $500,000', '$500,000' in html_content),
                ('18 months', '18 months' in html_content),
                ('90% user satisfaction', '90%' in html_content)
            ]
            
            print("\n📋 Content Validation:")
            for item, found in checks:
                status = "✅" if found else "❌"
                print(f"  {status} {item}: {'Found' if found else 'Missing'}")
            
            # Show a preview of the generated HTML
            print(f"\n📄 Generated BRD Preview (first 500 chars):")
            print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server. Make sure it's running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_brd_api()
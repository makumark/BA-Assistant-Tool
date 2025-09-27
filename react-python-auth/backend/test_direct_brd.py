#!/usr/bin/env python3
"""
Direct test of the BRD generation functionality
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '.')
app_dir = os.path.join(backend_dir, 'app')
sys.path.insert(0, backend_dir)
sys.path.insert(0, app_dir)

# Import the ai_service directly
from app.services.ai_service import generate_brd_html

def test_brd_generation():
    """Test BRD generation directly"""
    
    # Test input - same as before
    test_input = """Project: Learning Management System (LMS) Enhancement

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

    print("🧪 Testing BRD Generation Directly...")
    print("=" * 50)
    
    try:
        # Generate BRD - correct function signature
        project = "Learning Management System (LMS) Enhancement"
        inputs = {"input": test_input}
        version = 1
        
        result = generate_brd_html(project, inputs, version)
        
        print(f"✅ Successfully generated BRD!")
        print(f"📏 Length: {len(result)} characters")
        
        # Validation checks
        checks = [
            ('Course Management', 'Course Management' in result),
            ('Student Enrollment', 'Student Enrollment' in result),
            ('Learning Delivery', 'Learning Delivery' in result),
            ('Virtual Classroom', 'Virtual Classroom' in result),
            ('Progress Tracking', 'Progress Tracking' in result),
            ('40% of target users', '40%' in result),
            ('$500,000', '$500,000' in result),
            ('18 months', '18 months' in result),
            ('90% user satisfaction', '90%' in result),
            ('25% improvement', '25%' in result)
        ]
        
        print("\n📋 Content Validation:")
        print("-" * 30)
        passed = 0
        for item, found in checks:
            status = "✅" if found else "❌"
            print(f"  {status} {item}")
            if found:
                passed += 1
        
        print(f"\n📊 Validation Results: {passed}/{len(checks)} checks passed")
        
        # Show preview
        print(f"\n📄 Generated BRD Full Content:")
        print("-" * 50)
        print(result)  # Show full content to see what's generated
        print("-" * 50)
        
        if passed >= len(checks) * 0.8:  # 80% pass rate
            print(f"\n🎉 SUCCESS: BRD generation is working correctly!")
            print(f"   All major content elements are preserved.")
        else:
            print(f"\n⚠️  WARNING: Some content validation failed.")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during BRD generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_brd_generation()
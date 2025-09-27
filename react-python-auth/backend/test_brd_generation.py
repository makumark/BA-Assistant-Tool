"""
Test BRD generation to ensure it reflects user input accurately
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_service import generate_brd_html

# Test with user input
test_inputs = {
    "requirements": """
    Course management: Create and publish courses with modules and prerequisites
    Learning delivery: Video streaming, SCORM content, quizzes and assignments
    Virtual classroom: Live sessions with recordings and attendance tracking
    Learner experience: Progress tracking, certificates, and recommendations
    Collaboration: Discussion forums, messaging, and announcements
    Administration: User roles, content library, and analytics
    """,
    "validations": """
    Email format validation required
    Prerequisite checks before enrollment
    Quiz attempt limits (max 3 attempts)
    Assignment file type restrictions (PDF, DOC only)
    Certificate issued only after 70% score
    """,
    "scope": """
    In Scope: LMS platform with course management, learning delivery, virtual classrooms
    Out of Scope: Integration with external payment systems, mobile app development
    """,
    "objectives": """
    Increase learner engagement by 40%
    Reduce course creation time by 60%
    Achieve 95% system availability
    Support 10,000+ concurrent users
    """,
    "budget": "Estimated $500K for development and first-year support",
    "assumptions": "Users have reliable internet; content provided in digital formats; APIs available for integrations",
    "constraints": "6-month timeline; WCAG 2.1 compliance required; budget limitation of $500K"
}

print("🧪 Testing BRD Generation with User Input...")
print("=" * 60)

# Generate BRD
result = generate_brd_html("EdTech LMS Platform", test_inputs, 1)

# Check if result contains user input
print("✅ BRD Generated Successfully!")
print(f"📄 Document Length: {len(result)} characters")
print(f"🔍 Contains 'Course management': {'Course management' in result}")
print(f"🔍 Contains 'Learning delivery': {'Learning delivery' in result}")
print(f"🔍 Contains 'Virtual classroom': {'Virtual classroom' in result}")
print(f"🔍 Contains user objectives: {'40%' in result}")
print(f"🔍 Contains user budget: {'$500K' in result}")
print(f"🔍 Contains user scope: {'Out of Scope' in result}")
print(f"🔍 Contains validations: {'Quiz attempt limits' in result}")

# Show a snippet of the generated BRD
print("\n📋 BRD Snippet (first 500 chars):")
print("-" * 40)
print(result[:500] + "..." if len(result) > 500 else result)

print("\n" + "=" * 60)
print("🎉 BRD generation test completed!")
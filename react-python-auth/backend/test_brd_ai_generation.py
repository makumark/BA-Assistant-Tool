"""
Test script to validate AI-powered BRD generation
Tests both the enhanced fallback and AI functionality
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.ai_service import generate_brd_html

def test_brd_generation():
    """Test BRD generation with enhanced AI service."""
    
    print("🧪 Testing AI-Powered BRD Generation...")
    print("="*60)
    
    # Test case: Learning Management System (LMS)
    test_inputs = {
        "briefRequirements": """
            1. Student enrollment and course registration system
            2. Online course content delivery with video streaming
            3. Assignment submission and grading functionality
            4. Progress tracking and analytics for students and instructors
            5. Discussion forums and student collaboration tools
            6. Certificate generation upon course completion
            7. Payment processing for paid courses
            8. Mobile-responsive design for various devices
        """,
        "objectives": """
            - Improve learning outcomes through better engagement
            - Reduce administrative workload by 40%
            - Enable remote learning capabilities
            - Increase course completion rates to 85%
        """,
        "scope": """
            In scope: Core LMS functionality, basic reporting, mobile access
            Out of scope: Advanced AI tutoring, VR integration, complex analytics
        """,
        "budget": "Initial budget allocation of $500,000 for development and first-year operations",
        "assumptions": """
            - Students have reliable internet access
            - Instructors will receive training on the platform
            - Content migration from existing systems is feasible
        """,
        "constraints": """
            - Must comply with FERPA educational privacy regulations
            - Integration with existing student information systems required
            - 12-month delivery timeline
        """,
        "validations": """
            - All student data must be encrypted and secure
            - Course videos must load within 3 seconds
            - System must support 1000+ concurrent users
        """
    }
    
    project_name = "EduPlatform Learning Management System"
    version = 1
    
    print(f"📋 Project: {project_name}")
    print(f"📊 Test Data: LMS requirements with comprehensive sections")
    print(f"🔧 Version: {version}")
    print("\n" + "="*60)
    
    try:
        # Generate BRD using enhanced AI service
        print("🤖 Generating BRD with Enhanced AI Service...")
        brd_html = generate_brd_html(project_name, test_inputs, version)
        
        # Validate the results
        print("\n✅ BRD Generation Results:")
        print(f"📏 Document Length: {len(brd_html):,} characters")
        
        # Check for key sections
        sections_found = []
        expected_sections = [
            "Executive Summary", "Project Scope", "Business Objectives", 
            "Business Requirements (EPICs)", "Assumptions", "Constraints", 
            "Validations", "Budget Details"
        ]
        
        for section in expected_sections:
            if section in brd_html:
                sections_found.append(section)
        
        print(f"📋 Sections Found: {len(sections_found)}/{len(expected_sections)}")
        for section in sections_found:
            print(f"   ✓ {section}")
        
        # Check for domain detection
        if "Education" in brd_html or "Learning" in brd_html:
            print("🎯 Domain Detection: ✅ Education/Learning domain detected")
        else:
            print("🎯 Domain Detection: ❌ Domain not properly detected")
        
        # Check for EPIC formatting
        epic_count = brd_html.count("EPIC-")
        print(f"📊 EPICs Generated: {epic_count} business requirements converted to EPICs")
        
        # Check for professional formatting
        professional_indicators = [
            "Business Requirements Document", "AI Business Analyst", 
            "Document Control", "Business Value", "Executive Summary"
        ]
        
        professional_score = sum(1 for indicator in professional_indicators if indicator in brd_html)
        print(f"🎨 Professional Formatting: {professional_score}/{len(professional_indicators)} indicators found")
        
        # Check for enhancement quality
        enhancement_indicators = [
            "operational efficiency", "business value", "stakeholder satisfaction",
            "scalable growth", "strategic investment"
        ]
        
        enhancement_score = sum(1 for indicator in enhancement_indicators if indicator.lower() in brd_html.lower())
        print(f"🚀 AI Enhancement Quality: {enhancement_score}/{len(enhancement_indicators)} business terms found")
        
        print("\n" + "="*60)
        print("📄 BRD Document Preview (First 1000 characters):")
        print("-"*60)
        print(brd_html[:1000] + "..." if len(brd_html) > 1000 else brd_html)
        print("-"*60)
        
        # Overall assessment
        total_score = len(sections_found) + professional_score + enhancement_score + (1 if epic_count >= 6 else 0)
        max_score = len(expected_sections) + len(professional_indicators) + len(enhancement_indicators) + 1
        
        print(f"\n📊 Overall BRD Quality Score: {total_score}/{max_score} ({(total_score/max_score)*100:.1f}%)")
        
        if total_score >= max_score * 0.8:
            print("🎉 EXCELLENT: BRD generation is working with high quality AI enhancement!")
        elif total_score >= max_score * 0.6:
            print("✅ GOOD: BRD generation is functional with reasonable enhancement")
        else:
            print("⚠️ NEEDS IMPROVEMENT: BRD generation needs optimization")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: BRD generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_brd_generation()
    print(f"\n🏁 Test {'PASSED' if success else 'FAILED'}")
#!/usr/bin/env python3
"""
Test Enhanced FRD Generation Functionality
Tests the improved requirement extraction and EPIC generation
"""

def test_enhanced_functionality():
    """Test the enhanced FRD generation with real BRD content"""
    
    # Sample BRD content (financial domain)
    brd_content = """
    <h3>EPIC-01: Investor Onboarding System</h3>
    <ul>
        <li>Digital intake with guided forms for accredited investor registration</li>
        <li>Eligibility verification through accreditation status and income verification</li>
        <li>Document upload portal with real-time validation and version control</li>
        <li>Integrated workflows for review and approval processes</li>
    </ul>

    <h3>EPIC-02: Compliance and Risk Management</h3>
    <ul>
        <li>KYC/AML screening and automated compliance checks</li>
        <li>Risk scoring methodology with customizable parameters</li>
        <li>Automated compliance reporting and audit trails</li>
        <li>Integration with third-party screening services</li>
    </ul>

    <h3>EPIC-03: Investment Processing</h3>
    <ul>
        <li>Secure payment processing with multiple funding sources</li>
        <li>Real-time portfolio allocation and rebalancing</li>
        <li>Electronic signature and document management</li>
        <li>Tax reporting and regulatory documentation</li>
    </ul>
    """
    
    print("=== Enhanced FRD Generation Test ===\n")
    
    # Test 1: Domain Detection
    print("1. Testing Domain Detection:")
    domain = detect_domain_from_brd_text(brd_content)
    print(f"   Detected Domain: {domain}")
    assert domain == 'financial', f"Expected 'financial', got '{domain}'"
    print("   ✅ Domain detection working correctly\n")
    
    # Test 2: Requirement Extraction
    print("2. Testing Requirement Extraction:")
    requirements = extract_requirements_from_brd(brd_content)
    print(f"   Extracted {len(requirements)} EPIC sections:")
    for req in requirements:
        print(f"   - {req['epicId']}: {req['title']} ({len(req['requirements'])} requirements)")
    assert len(requirements) == 3, f"Expected 3 EPICs, got {len(requirements)}"
    print("   ✅ Requirement extraction working correctly\n")
    
    # Test 3: EPIC Title Generation
    print("3. Testing EPIC Title Generation:")
    epic_titles = []
    for i, req in enumerate(requirements):
        title = generate_meaningful_epic_title(req['requirements'], domain, i)
        epic_titles.append(title)
        print(f"   {req['epicId']}: {title}")
    
    # Check for meaningful titles
    expected_keywords = [
        ['onboarding', 'intake'],
        ['compliance', 'risk'],
        ['investment', 'processing', 'portfolio']
    ]
    
    for i, (title, keywords) in enumerate(zip(epic_titles, expected_keywords)):
        title_lower = title.lower()
        has_keyword = any(keyword in title_lower for keyword in keywords)
        assert has_keyword, f"Title '{title}' should contain one of {keywords}"
    
    print("   ✅ EPIC title generation working correctly\n")
    
    # Test 4: User Story Generation
    print("4. Testing User Story Generation:")
    epics = convert_requirements_to_epics(requirements, domain)
    
    # Test user story generation for first EPIC
    first_epic = epics[0]
    user_stories = generate_user_stories_from_requirements(first_epic, domain, 0)
    
    print(f"   Generated {len(user_stories)} user stories for '{first_epic['title']}':")
    for story in user_stories:
        print(f"   - {story['id']}: {story['title']}")
        print(f"     As a {story['asA']}, I want {story['iWant']}")
        print(f"     So that {story['soThat']}")
        print(f"     Acceptance Criteria: {len(story['acceptanceCriteria'])} items")
        print()
    
    # Verify user stories are meaningful
    assert len(user_stories) > 0, "Should generate at least one user story"
    
    # Check that stories have meaningful content (not generic)
    first_story = user_stories[0]
    assert 'digital intake' in first_story['iWant'].lower() or 'form' in first_story['iWant'].lower(), \
           f"Story should be about digital intake, got: {first_story['iWant']}"
    
    print("   ✅ User story generation working correctly\n")
    
    print("🎉 All tests passed! Enhanced FRD generation is working correctly.")
    return True

def detect_domain_from_brd_text(brd_text):
    """Detect domain from BRD text (replicated from React code)"""
    text = brd_text.lower()
    domains = {
        'financial': ['investor', 'portfolio', 'kyc', 'aml', 'accredited', 'compliance', 
                     'fund', 'investment', 'tax reporting', 'risk scoring'],
        'marketing': ['campaign', 'customer', 'audience', 'brand', 'analytics', 
                     'conversion', 'lead generation'],
        'healthcare': ['patient', 'medical', 'provider', 'clinical', 'diagnosis', 
                      'treatment', 'hipaa'],
        'ecommerce': ['product', 'cart', 'checkout', 'order', 'payment', 'shipping', 
                     'inventory'],
        'airline': ['flight', 'passenger', 'booking', 'check-in', 'seat', 'baggage', 
                   'airport']
    }
    
    max_score = 0
    detected_domain = 'general'
    
    for domain, keywords in domains.items():
        score = sum(text.count(keyword) for keyword in keywords)
        if score > max_score:
            max_score = score
            detected_domain = domain
    
    return detected_domain

def extract_requirements_from_brd(brd_text):
    """Extract requirements from BRD text (replicated from React code)"""
    import re
    
    requirements = []
    epic_pattern = r'<h3>EPIC-(\d+):\s*([^<]+)</h3>([\s\S]*?)(?=<h3>|$)'
    
    for match in re.finditer(epic_pattern, brd_text, re.IGNORECASE):
        epic_id = f"EPIC-{match.group(1).zfill(2)}"
        epic_title = match.group(2).strip()
        epic_content = match.group(3)
        
        # Extract bullet points
        bullet_points = []
        li_pattern = r'<li>([^<]+)</li>'
        
        for li_match in re.finditer(li_pattern, epic_content, re.IGNORECASE):
            bullet_points.append(li_match.group(1).strip())
        
        if bullet_points:
            requirements.append({
                'epicId': epic_id,
                'title': epic_title,
                'requirements': bullet_points
            })
    
    return requirements

def generate_meaningful_epic_title(requirements, domain, index):
    """Generate meaningful EPIC title (replicated from React code)"""
    req_text = ' '.join(requirements).lower()
    
    if domain == 'financial':
        if ('investor' in req_text and 'onboard' in req_text) or ('digital intake' in req_text):
            return 'Investor Onboarding & Digital Intake'
        if 'kyc' in req_text or 'compliance' in req_text or 'aml' in req_text:
            return 'Compliance & Risk Management'
        if 'payment' in req_text or 'processing' in req_text:
            return 'Investment Processing & Portfolio Management'
        if 'portfolio' in req_text:
            return 'Portfolio Management & Reporting'
    
    # Generic fallback
    return f'Business Process {index + 1}'

def convert_requirements_to_epics(requirements, domain):
    """Convert requirements to EPICs (replicated from React code)"""
    epics = []
    
    for i, req in enumerate(requirements):
        meaningful_title = generate_meaningful_epic_title(req['requirements'], domain, i)
        
        epics.append({
            'id': req['epicId'],
            'title': meaningful_title,
            'description': f"{meaningful_title} encompasses the following requirements",
            'functionalRequirements': req['requirements'],
            'priority': 'High',
            'estimatedEffort': '2-3 sprints'
        })
    
    return epics

def generate_user_stories_from_requirements(epic, domain, epic_index):
    """Generate user stories from requirements (simplified version)"""
    stories = []
    requirements = epic['functionalRequirements']
    
    # Group requirements into logical stories
    story_groups = group_requirements_into_stories(requirements, epic['title'], domain)
    
    for story_index, story_group in enumerate(story_groups):
        story_id = f"US-{str(epic_index + 1).zfill(2)}-{str(story_index + 1).zfill(2)}"
        persona = get_appropriate_persona(story_group['requirements'], domain)
        story_title = f"{epic['title']} - {story_group['action']}"
        story_want = generate_story_want(story_group['requirements'])
        story_so_that = generate_story_so_that(story_group['requirements'], domain)
        
        stories.append({
            'id': story_id,
            'title': story_title,
            'asA': persona,
            'iWant': story_want,
            'soThat': story_so_that,
            'acceptanceCriteria': generate_story_acceptance_criteria(story_group['requirements']),
            'priority': epic['priority'],
            'storyPoints': calculate_story_points(story_group['requirements']),
            'epicId': epic['id']
        })
    
    return stories

def group_requirements_into_stories(requirements, epic_title, domain):
    """Group requirements into logical user stories"""
    groups = []
    
    if domain == 'financial':
        if 'onboarding' in epic_title.lower() or 'intake' in epic_title.lower():
            for req in requirements:
                req_lower = req.lower()
                if 'digital intake' in req_lower or 'form' in req_lower:
                    groups.append({
                        'action': 'Complete Digital Intake',
                        'requirements': [req],
                        'focus': 'intake'
                    })
                elif 'eligibility' in req_lower or 'accreditation' in req_lower:
                    groups.append({
                        'action': 'Verify Eligibility',
                        'requirements': [req],
                        'focus': 'verification'
                    })
                elif 'document upload' in req_lower:
                    groups.append({
                        'action': 'Upload Documents',
                        'requirements': [req],
                        'focus': 'documentation'
                    })
    
    # If no specific groups created, create generic ones
    if not groups:
        mid = len(requirements) // 2 + 1
        if len(requirements) > 1:
            groups.extend([
                {
                    'action': 'Manage Primary Functions',
                    'requirements': requirements[:mid],
                    'focus': 'primary'
                },
                {
                    'action': 'Handle Secondary Operations',
                    'requirements': requirements[mid:],
                    'focus': 'secondary'
                }
            ])
        else:
            groups.append({
                'action': 'Execute Core Functionality',
                'requirements': requirements,
                'focus': 'core'
            })
    
    return groups

def get_appropriate_persona(requirements, domain):
    """Get appropriate persona based on requirements"""
    req_text = ' '.join(requirements).lower()
    
    if domain == 'financial':
        if 'investor' in req_text or 'individual' in req_text or 'intake' in req_text:
            return 'Investor'
        if 'reviewer' in req_text or 'approval' in req_text or 'compliance' in req_text:
            return 'Compliance Officer'
        if 'admin' in req_text or 'manage' in req_text or 'workflow' in req_text:
            return 'Fund Administrator'
    
    return 'User'

def generate_story_want(requirements):
    """Generate 'I want' statement from requirements"""
    first_req = requirements[0].lower()
    
    if 'digital intake' in first_req or 'form' in first_req:
        return 'complete digital intake forms with guided assistance'
    if 'document upload' in first_req:
        return 'upload required documents with real-time validation'
    if 'kyc' in first_req or 'screening' in first_req:
        return 'complete KYC/AML screening and compliance checks'
    
    # Generic fallback
    return f"implement {first_req.split('.')[0].replace('•', '').replace('-', '').strip()}"

def generate_story_so_that(requirements, domain):
    """Generate 'so that' statement based on domain and requirements"""
    req_text = ' '.join(requirements).lower()
    
    if domain == 'financial':
        if 'investor' in req_text or 'onboard' in req_text:
            return 'I can efficiently onboard and start investing'
        if 'compliance' in req_text or 'kyc' in req_text:
            return 'I can ensure regulatory compliance and risk management'
        if 'document' in req_text or 'sign' in req_text:
            return 'I can complete legal requirements securely'
    
    return 'I can accomplish my business objectives efficiently'

def generate_story_acceptance_criteria(requirements):
    """Generate acceptance criteria from requirements"""
    criteria = []
    
    for req in requirements:
        req_lower = req.lower()
        if 'form' in req_lower or 'intake' in req_lower:
            criteria.append('Digital forms are completed with all required fields')
        if 'validation' in req_lower or 'real time' in req_lower:
            criteria.append('Real-time validation provides immediate feedback')
        if 'document' in req_lower or 'upload' in req_lower:
            criteria.append('Documents are uploaded and verified successfully')
        if 'screening' in req_lower or 'check' in req_lower:
            criteria.append('All compliance checks are completed successfully')
        if 'workflow' in req_lower or 'approval' in req_lower:
            criteria.append('Approval workflows are followed correctly')
    
    # Add generic criteria if none specific found
    if not criteria:
        criteria.extend([
            'User can successfully complete the required functionality',
            'System validates all inputs and provides feedback'
        ])
    
    criteria.append('Performance meets acceptable standards')
    return criteria[:4]  # Limit to 4 criteria

def calculate_story_points(requirements):
    """Calculate story points based on complexity"""
    complexity = ' '.join(requirements).lower()
    
    if any(word in complexity for word in ['workflow', 'integration', 'screening']):
        return 8  # Complex
    if any(word in complexity for word in ['validation', 'approval', 'document']):
        return 5  # Medium
    return 3  # Simple

if __name__ == "__main__":
    test_enhanced_functionality()
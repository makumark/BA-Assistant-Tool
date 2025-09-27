import json

# Simple test data to verify EPIC generation logic
test_data = {
    "project": "Test System",
    "scope": """
    Included:
    • User authentication and authorization
    • Data management and storage
    • Reporting and analytics dashboard
    • Email notification system
    
    Excluded:
    • Third-party integrations
    • Advanced reporting features
    """,
    "objectives": """
    • Improve system efficiency by 30%
    • Reduce manual processing time
    • Enhance user experience
    • Streamline business operations
    """,
    "budget": "₹25 lakhs covering development and licenses",
    "assumptions": "Users will receive adequate training"
}

print("Test Data for Domain-Agnostic EPIC Generation:")
print("=" * 50)
print("Project:", test_data["project"])
print("\nScope (Included):")
for line in test_data["scope"].split('\n'):
    if 'included:' in line.lower() or line.strip().startswith('•'):
        print(line)

print("\nObjectives:")
for line in test_data["objectives"].split('\n'):
    if line.strip().startswith('•') or line.strip():
        print(line)

print("\nBudget (should NOT appear in EPICs):", test_data["budget"])
print("\nExpected Result: EPICs should only be generated from Included scope + Objectives")
print("Budget details should be completely excluded from EPIC generation.")

# Save as JSON for manual testing
with open('test_data.json', 'w') as f:
    json.dump(test_data, f, indent=2)

print("\n✅ Test data saved to test_data.json")
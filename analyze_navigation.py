#!/usr/bin/env python3

def analyze_navigation_duplicates():
    """Analyze the generated prototype to find duplicate navigation headers"""
    
    try:
        with open('fresh_working_prototype.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 Analyzing prototype for duplicate navigation headers...")
        
        # Count navigation sections
        nav_count = content.count('prototype-navigation')
        print(f"📊 Total 'prototype-navigation' occurrences: {nav_count}")
        
        # Find all navigation HTML blocks
        nav_sections = content.split('<div class="prototype-navigation">')
        print(f"📊 Actual navigation div blocks: {len(nav_sections) - 1}")
        
        # Show each navigation section
        for i, section in enumerate(nav_sections[1:], 1):
            end_div = section.find('</div>')
            if end_div != -1:
                nav_content = section[:end_div]
                print(f"\n=== Navigation Block {i} ===")
                print(nav_content[:300] + ("..." if len(nav_content) > 300 else ""))
        
        # Check for specific navigation patterns
        patterns = [
            "Generic Dashboard",
            "Browse Products", 
            "Checkout",
            "Ecommerce Dashboard"
        ]
        
        print(f"\n🔍 Navigation button analysis:")
        for pattern in patterns:
            count = content.count(pattern)
            if count > 0:
                print(f"  '{pattern}': {count} occurrences")
        
        # Check if there are duplicate navigation buttons
        checkout_buttons = content.count('onclick="showPage(\'checkout\')"')
        dashboard_buttons = content.count('onclick="showPage(\'dashboard\')"')
        browse_buttons = content.count('"Browse Products"')
        
        print(f"\n📱 Button duplication check:")
        print(f"  Checkout buttons: {checkout_buttons}")
        print(f"  Dashboard buttons: {dashboard_buttons}")
        print(f"  Browse Products buttons: {browse_buttons}")
        
        if checkout_buttons > 1 or dashboard_buttons > 1 or browse_buttons > 1:
            print("❌ FOUND DUPLICATE NAVIGATION BUTTONS!")
        else:
            print("✅ No duplicate navigation buttons found")
            
    except FileNotFoundError:
        print("❌ Fresh prototype file not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_navigation_duplicates()
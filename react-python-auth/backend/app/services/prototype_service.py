"""
Prototype Generation Service
AI-powered interactive prototype generation from user stories and FRD content
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

def generate_prototype_from_user_stories(project_name: str, user_stories: List[Dict], domain: str = "generic") -> str:
    """
    Generate interactive HTML prototype based on user stories and domain
    """
    print(f"🎯 Generating interactive prototype for {project_name} in {domain} domain")
    
    # Analyze user stories to determine prototype structure
    pages = _analyze_stories_for_prototype_pages(user_stories, domain)
    
    # Generate interactive prototype HTML
    prototype_html = _generate_prototype_html(project_name, pages, domain)
    
    return prototype_html

def generate_prototype_from_frd(project_name: str, frd_content: str, domain: str = "generic") -> str:
    """
    Generate prototype from FRD content by extracting user stories
    """
    print(f"🎯 Extracting user stories from FRD for prototype generation")
    
    # Extract user stories from FRD
    user_stories = _extract_user_stories_from_frd(frd_content)
    
    # Generate prototype
    return generate_prototype_from_user_stories(project_name, user_stories, domain)

def _analyze_stories_for_prototype_pages(user_stories: List[Dict], domain: str) -> List[Dict]:
    """
    Analyze user stories to determine what prototype pages are needed
    """
    pages = []
    created_page_ids = set()
    
    # Always include a dashboard/home page
    dashboard_page = _create_prototype_dashboard(domain)
    pages.append(dashboard_page)
    created_page_ids.add(dashboard_page["page_id"])
    
    # Analyze each user story for specific page types
    for story in user_stories:
        story_text = f"{story.get('role', '')} {story.get('goal', '')} {story.get('benefit', '')}".lower()
        
        if any(keyword in story_text for keyword in ['login', 'sign in', 'authenticate', 'access']) and 'login' not in created_page_ids:
            page = _create_prototype_login_page(story, domain)
            pages.append(page)
            created_page_ids.add(page["page_id"])
        
        if any(keyword in story_text for keyword in ['browse', 'search', 'view products', 'catalog']) and 'products' not in created_page_ids:
            page = _create_prototype_product_listing(story, domain)
            pages.append(page)
            created_page_ids.add(page["page_id"])
            
        if any(keyword in story_text for keyword in ['checkout', 'payment', 'order', 'cart', 'shopping']) and 'checkout' not in created_page_ids:
            page = _create_prototype_checkout_page(story, domain)
            pages.append(page)
            created_page_ids.add(page["page_id"])
            
        if any(keyword in story_text for keyword in ['profile', 'account', 'settings']) and 'profile' not in created_page_ids:
            page = _create_prototype_profile_page(story, domain)
            pages.append(page)
            created_page_ids.add(page["page_id"])
    
    return pages

def _create_prototype_dashboard(domain: str) -> Dict:
    """Create dashboard prototype page"""
    return {
        "page_id": "dashboard",
        "title": f"{domain.title()} Dashboard",
        "components": _get_dashboard_components(domain),
        "navigation": True,
        "interactive_elements": ["search", "filters", "quick_actions"]
    }

def _create_prototype_login_page(story: Dict, domain: str) -> Dict:
    """Create login prototype page"""
    return {
        "page_id": "login",
        "title": "Login / Sign In",
        "components": [
            {"type": "form", "fields": ["email", "password"], "action": "login"},
            {"type": "button", "text": "Sign In", "primary": True},
            {"type": "link", "text": "Forgot Password?"},
            {"type": "divider"},
            {"type": "button", "text": "Sign Up", "secondary": True}
        ],
        "navigation": False,
        "interactive_elements": ["form_validation", "password_toggle"]
    }

def _create_prototype_product_listing(story: Dict, domain: str) -> Dict:
    """Create product listing prototype page"""
    products = _get_domain_sample_products(domain)
    return {
        "page_id": "products",
        "title": "Browse Products",
        "components": [
            {"type": "search_bar", "placeholder": f"Search {domain} products..."},
            {"type": "filters", "options": _get_domain_filters(domain)},
            {"type": "product_grid", "products": products},
            {"type": "pagination", "pages": 5}
        ],
        "navigation": True,
        "interactive_elements": ["search", "filter", "sort", "add_to_cart"]
    }

def _create_prototype_shopping_cart(story: Dict, domain: str) -> Dict:
    """Create shopping cart prototype page"""
    return {
        "page_id": "cart",
        "title": "Shopping Cart",
        "components": [
            {"type": "cart_items", "count": 3},
            {"type": "quantity_controls"},
            {"type": "price_summary"},
            {"type": "promo_code"},
            {"type": "button", "text": "Proceed to Checkout", "primary": True}
        ],
        "navigation": True,
        "interactive_elements": ["quantity_change", "remove_item", "promo_apply"]
    }

def _create_prototype_checkout_page(story: Dict, domain: str) -> Dict:
    """Create checkout prototype page"""
    return {
        "page_id": "checkout",
        "title": "Checkout",
        "components": [
            {"type": "progress_indicator", "steps": ["Cart", "Shipping", "Payment", "Confirmation"]}
        ],
        "navigation": True,
        "interactive_elements": ["form_validation", "step_navigation", "checkout_flow"]
    }

def _create_prototype_profile_page(story: Dict, domain: str) -> Dict:
    """Create user profile prototype page"""
    return {
        "page_id": "profile",
        "title": "My Profile",
        "components": [
            {"type": "avatar_upload"},
            {"type": "form", "fields": ["name", "email", "phone", "address"]},
            {"type": "preferences", "domain": domain},
            {"type": "order_history"},
            {"type": "button", "text": "Save Changes", "primary": True}
        ],
        "navigation": True,
        "interactive_elements": ["file_upload", "form_validation", "preferences_toggle"]
    }

def _get_dashboard_components(domain: str) -> List[Dict]:
    """Get dashboard components based on domain"""
    domain_components = {
        "ecommerce": [
            {"type": "stats", "metrics": ["Total Orders", "Revenue", "Products", "Customers"]},
            {"type": "recent_orders"},
            {"type": "popular_products"},
            {"type": "quick_actions", "actions": ["Add Product", "View Orders", "Customer Support"]}
        ],
        "financial": [
            {"type": "stats", "metrics": ["Portfolio Value", "Returns", "Active Investments", "Risk Score"]},
            {"type": "portfolio_chart"},
            {"type": "recent_transactions"},
            {"type": "quick_actions", "actions": ["New Investment", "Transfer Funds", "View Reports"]}
        ],
        "healthcare": [
            {"type": "stats", "metrics": ["Total Patients", "Appointments Today", "Available Beds", "Staff On Duty"]},
            {"type": "upcoming_appointments"},
            {"type": "patient_alerts"},
            {"type": "quick_actions", "actions": ["Schedule Appointment", "Add Patient", "View Records"]}
        ]
    }
    return domain_components.get(domain, domain_components["ecommerce"])

def _get_domain_sample_products(domain: str) -> List[Dict]:
    """Get sample products based on domain"""
    domain_products = {
        "ecommerce": [
            {"name": "Wireless Headphones", "price": "$99.99", "rating": 4.5, "image": "headphones.jpg"},
            {"name": "Smart Watch", "price": "$299.99", "rating": 4.8, "image": "smartwatch.jpg"},
            {"name": "Laptop Stand", "price": "$49.99", "rating": 4.2, "image": "laptop-stand.jpg"},
            {"name": "Bluetooth Speaker", "price": "$79.99", "rating": 4.6, "image": "speaker.jpg"}
        ],
        "financial": [
            {"name": "Growth Fund", "return": "12.5%", "risk": "Medium", "minimum": "$1000"},
            {"name": "Index Fund", "return": "8.2%", "risk": "Low", "minimum": "$500"},
            {"name": "Tech Stocks", "return": "15.7%", "risk": "High", "minimum": "$2000"},
            {"name": "Bonds Portfolio", "return": "4.1%", "risk": "Very Low", "minimum": "$100"}
        ]
    }
    return domain_products.get(domain, domain_products["ecommerce"])

def _get_domain_filters(domain: str) -> List[str]:
    """Get filter options based on domain"""
    domain_filters = {
        "ecommerce": ["Category", "Price Range", "Brand", "Rating", "Availability"],
        "financial": ["Asset Type", "Risk Level", "Minimum Investment", "Returns", "Duration"],
        "healthcare": ["Department", "Availability", "Experience", "Specialization", "Location"]
    }
    return domain_filters.get(domain, domain_filters["ecommerce"])

def _extract_user_stories_from_frd(frd_content: str) -> List[Dict]:
    """Extract user stories from FRD HTML content"""
    user_stories = []
    
    # Use regex to find user story patterns
    story_patterns = [
        r'As a ([^,]+), I want ([^,]+), so that ([^.]+)',
        r'As an? ([^,]+), I want ([^,]+), so that ([^.]+)',
        r'User Story.*?As a ([^,]+).*?want ([^,]+).*?so that ([^.]+)'
    ]
    
    for pattern in story_patterns:
        matches = re.findall(pattern, frd_content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            if len(match) == 3:
                user_stories.append({
                    "role": match[0].strip(),
                    "goal": match[1].strip(),
                    "benefit": match[2].strip()
                })
    
    # If no formal user stories found, extract from generic content
    if not user_stories:
        # Extract requirements and convert to user stories
        requirement_patterns = [
            r'([A-Z][^.]+(?:manage|create|view|process|handle|track|generate|provide)[^.]*)',
            r'The system (?:shall|must|should) ([^.]+)',
            r'Users (?:can|should be able to|must be able to) ([^.]+)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, frd_content, re.MULTILINE)
            for i, req in enumerate(matches[:10]):  # Limit to 10 requirements
                user_stories.append({
                    "role": "User",
                    "goal": f"be able to {req.lower()}",
                    "benefit": "accomplish business objectives efficiently"
                })
    
    return user_stories[:10]  # Limit to 10 user stories

def _generate_prototype_html(project_name: str, pages: List[Dict], domain: str) -> str:
    """Generate interactive prototype HTML"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Interactive Prototype</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc;
            color: #2d3748;
        }}
        
        .prototype-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .prototype-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            text-align: center;
        }}
        
        .prototype-navigation {{
            background: #2d3748;
            padding: 0;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .nav-button {{
            background: none;
            border: none;
            color: white;
            padding: 1rem 2rem;
            cursor: pointer;
            transition: background-color 0.3s;
            font-size: 14px;
        }}
        
        .nav-button:hover,
        .nav-button.active {{
            background: #4a5568;
        }}
        
        .prototype-page {{
            display: none;
            padding: 2rem;
            min-height: 500px;
        }}
        
        .prototype-page.active {{
            display: block;
        }}
        
        .page-title {{
            color: #2d3748;
            margin-bottom: 2rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #4299e1;
        }}
        
        /* Component Styles */
        .component {{
            margin-bottom: 2rem;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: white;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .form-group {{
            margin-bottom: 1rem;
        }}
        
        .form-label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #4a5568;
        }}
        
        .form-input {{
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            font-size: 1rem;
        }}
        
        .form-input:focus {{
            outline: none;
            border-color: #4299e1;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }}
        
        .btn {{
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
            margin-right: 1rem;
            margin-bottom: 0.5rem;
        }}
        
        .btn-primary {{
            background: #4299e1;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #3182ce;
        }}
        
        .btn-secondary {{
            background: #e2e8f0;
            color: #4a5568;
        }}
        
        .btn-secondary:hover {{
            background: #cbd5e0;
        }}
        
        .product-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }}
        
        .product-card {{
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1rem;
            background: white;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .product-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .product-image {{
            width: 100%;
            height: 150px;
            background: #f7fafc;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            color: #a0aec0;
        }}
        
        .search-bar {{
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        
        .filters {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}
        
        .filter-select {{
            padding: 0.5rem 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            background: white;
        }}
        
        .progress-indicator {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            padding: 1rem 0;
        }}
        
        .progress-step {{
            flex: 1;
            text-align: center;
            padding: 0.5rem;
            background: #e2e8f0;
            margin-right: 1rem;
            border-radius: 4px;
            position: relative;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .progress-step:hover {{
            background: #cbd5e0;
        }}
        
        .progress-step.active {{
            background: #4299e1;
            color: white;
        }}
        
        .step-content {{
            margin-top: 2rem;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: white;
        }}
        
        .cart-items-list {{
            margin: 1rem 0;
        }}
        
        .cart-item {{
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #f7fafc;
        }}
        
        .cart-total {{
            font-weight: bold;
            font-size: 1.2rem;
            margin: 1rem 0;
            text-align: right;
        }}
        
        .confirmation-details {{
            text-align: center;
            padding: 2rem;
        }}
        
        .confirmation-details p {{
            margin: 1rem 0;
            font-size: 1.1rem;
        }}
        
        input[type="text"], input[type="email"] {{
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #e2e8f0;
            border-radius: 4px;
            font-size: 1rem;
        }}
        
        input[type="text"]:focus, input[type="email"]:focus {{
            border-color: #4299e1;
            outline: none;
        }}
            align-items: center;
            padding: 1rem;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .quantity-controls {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .quantity-btn {{
            width: 30px;
            height: 30px;
            border: 1px solid #e2e8f0;
            background: white;
            cursor: pointer;
            border-radius: 4px;
        }}
        
        .interactive-demo {{
            background: #f0fff4;
            border: 2px solid #68d391;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
        }}
        
        .demo-message {{
            color: #2f855a;
            font-weight: 500;
        }}
        
        @media (max-width: 768px) {{
            .prototype-navigation {{
                flex-direction: column;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .product-grid {{
                grid-template-columns: 1fr;
            }}
            
            .filters {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="prototype-container">
        <div class="prototype-header">
            <h1>🎯 {project_name} - Interactive Prototype</h1>
            <p>Domain: {domain.title()} | Generated: {timestamp}</p>
        </div>
        
        <div class="prototype-navigation">
            {_generate_navigation_buttons(pages)}
        </div>
        
        {_generate_page_content(pages, domain)}
    </div>
    
    <script>
        // Interactive prototype functionality
        function showPage(pageId) {{
            // Hide all pages
            const pages = document.querySelectorAll('.prototype-page');
            pages.forEach(page => page.classList.remove('active'));
            
            // Show selected page
            const selectedPage = document.getElementById(pageId);
            if (selectedPage) {{
                selectedPage.classList.add('active');
            }}
            
            // Update navigation
            const navButtons = document.querySelectorAll('.nav-button');
            navButtons.forEach(btn => btn.classList.remove('active'));
            
            const activeBtn = document.querySelector(`[onclick="showPage('${{pageId}}')"]`);
            if (activeBtn) {{
                activeBtn.classList.add('active');
            }}
        }}
        
        // Checkout step functionality
        function showCheckoutStep(step) {{
            const steps = ['cart', 'shipping', 'payment', 'confirmation'];
            const stepButtons = document.querySelectorAll('.checkout-step');
            const stepContents = document.querySelectorAll('.step-content');
            
            // Update step buttons
            stepButtons.forEach((btn, index) => {{
                btn.classList.remove('active');
                if (steps[index] === step) {{
                    btn.classList.add('active');
                }}
            }});
            
            // Show step content
            stepContents.forEach(content => {{
                content.style.display = 'none';
            }});
            
            const activeContent = document.getElementById(`step-${{step}}`);
            if (activeContent) {{
                activeContent.style.display = 'block';
            }}
        }}
        
        // Cart to shipping navigation
        function proceedToShipping() {{
            showNotification('Proceeding to shipping...');
            showCheckoutStep('shipping');
        }}
        
        // Form submission handlers
        function processShipping() {{
            const form = document.getElementById('shippingForm');
            if (form && validateForm(form)) {{
                showNotification('Shipping information saved!');
                showCheckoutStep('payment');
            }} else {{
                showNotification('Please fill in all shipping details', 'error');
            }}
        }}
        
        function processPayment() {{
            const form = document.getElementById('paymentForm');
            if (form && validateForm(form)) {{
                showNotification('Processing payment...');
                setTimeout(() => {{
                    showNotification('Payment successful!');
                    showCheckoutStep('confirmation');
                }}, 2000);
            }} else {{
                showNotification('Please fill in payment details', 'error');
            }}
        }}
        
        function validateForm(form) {{
            const inputs = form.querySelectorAll('input[required], select[required]');
            let isValid = true;
            
            inputs.forEach(input => {{
                if (!input.value.trim()) {{
                    input.style.borderColor = '#f44336';
                    isValid = false;
                }} else {{
                    input.style.borderColor = '#ddd';
                }}
            }});
            
            return isValid;
        }}
        
        function showNotification(message, type = 'success') {{
            const notification = document.createElement('div');
            notification.className = `notification ${{type}}`;
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed; top: 20px; right: 20px; z-index: 1000;
                padding: 15px 20px; border-radius: 5px; color: white;
                background: ${{type === 'success' ? '#4CAF50' : '#f44336'}};
                animation: slideIn 0.3s ease-out;
            `;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);
        }}

        // Initialize first page as active
        document.addEventListener('DOMContentLoaded', function() {{
            const firstPage = document.querySelector('.prototype-page');
            if (firstPage) {{
                firstPage.classList.add('active');
                const firstBtn = document.querySelector('.nav-button');
                if (firstBtn) {{
                    firstBtn.classList.add('active');
                }}
            }}
        }});
        
        // Interactive elements
        function handleLogin() {{
            showDemo('Login successful! Redirecting to dashboard...');
            setTimeout(() => showPage('dashboard'), 2000);
        }}
        
        function addToCart(productName) {{
            showDemo(`Added ${{productName}} to cart!`);
        }}
        
        function updateQuantity(change) {{
            showDemo(`Quantity updated! ${{change > 0 ? 'Increased' : 'Decreased'}} by ${{Math.abs(change)}}`);
        }}
        
        function processPayment() {{
            showDemo('Processing payment... Order confirmed!');
        }}
        
        function showDemo(message) {{
            const demoDiv = document.createElement('div');
            demoDiv.className = 'interactive-demo';
            demoDiv.innerHTML = `<div class="demo-message">✅ ${{message}}</div>`;
            
            const container = document.querySelector('.prototype-page.active');
            if (container) {{
                container.insertBefore(demoDiv, container.firstChild);
                setTimeout(() => demoDiv.remove(), 3000);
            }}
        }}
        
        // Search functionality
        function handleSearch(query) {{
            if (query.trim()) {{
                showDemo(`Searching for "${{query}}"... Found 12 results!`);
            }}
        }}
        
        // Form validation
        function validateForm(formId) {{
            showDemo('Form validated successfully!');
            return false; // Prevent actual submission
        }}
    </script>
</body>
</html>
    """
    
    return html_content

def _generate_navigation_buttons(pages: List[Dict]) -> str:
    """Generate navigation buttons for prototype pages"""
    buttons = []
    for page in pages:
        page_id = page.get('page_id', 'page')
        title = page.get('title', 'Page')
        buttons.append(f'<button class="nav-button" onclick="showPage(\'{page_id}\')">{title}</button>')
    
    return '\n            '.join(buttons)

def _generate_page_content(pages: List[Dict], domain: str) -> str:
    """Generate HTML content for all prototype pages"""
    content = []
    
    for page in pages:
        page_id = page.get('page_id', 'page')
        title = page.get('title', 'Page')
        components = page.get('components', [])
        
        page_html = f'''
        <div id="{page_id}" class="prototype-page">
            <h2 class="page-title">{title}</h2>
            {_generate_components_html(components, page_id, domain)}
        </div>'''
        
        content.append(page_html)
    
    return '\n'.join(content)

def _generate_components_html(components: List[Dict], page_id: str, domain: str) -> str:
    """Generate HTML for page components"""
    html_parts = []
    
    for component in components:
        comp_type = component.get('type', 'text')
        
        if comp_type == 'stats':
            metrics = component.get('metrics', [])
            stats_html = '<div class="stats-grid">'
            for metric in metrics:
                stats_html += f'''
                <div class="stat-card">
                    <div class="stat-value">{'$125K' if 'revenue' in metric.lower() else '1,234' if 'total' in metric.lower() else '89%'}</div>
                    <div>{metric}</div>
                </div>'''
            stats_html += '</div>'
            html_parts.append(stats_html)
            
        elif comp_type == 'form':
            fields = component.get('fields', [])
            action = component.get('action', 'submit')
            form_html = f'<div class="component"><form onsubmit="return validateForm(\'{page_id}-form\')">'
            
            for field in fields:
                field_type = 'password' if 'password' in field else 'email' if 'email' in field else 'text'
                form_html += f'''
                <div class="form-group">
                    <label class="form-label">{field.replace('_', ' ').title()}</label>
                    <input type="{field_type}" class="form-input" placeholder="Enter {field.replace('_', ' ')}" required>
                </div>'''
            
            if action == 'login':
                form_html += '<button type="button" class="btn btn-primary" onclick="handleLogin()">Sign In</button>'
            else:
                form_html += '<button type="submit" class="btn btn-primary">Submit</button>'
            
            form_html += '</form></div>'
            html_parts.append(form_html)
            
        elif comp_type == 'search_bar':
            placeholder = component.get('placeholder', 'Search...')
            search_html = f'''
            <div class="component">
                <input type="search" class="search-bar" placeholder="{placeholder}" 
                       onkeypress="if(event.key==='Enter') handleSearch(this.value)">
                <button class="btn btn-primary" onclick="handleSearch(document.querySelector('.search-bar').value)">Search</button>
            </div>'''
            html_parts.append(search_html)
            
        elif comp_type == 'product_grid':
            products = component.get('products', [])
            grid_html = '<div class="component"><div class="product-grid">'
            
            for product in products:
                grid_html += f'''
                <div class="product-card">
                    <div class="product-image">📦 Product Image</div>
                    <h3>{product.get('name', 'Product Name')}</h3>
                    <p>Price: {product.get('price', '$99.99')}</p>
                    <p>Rating: {'⭐' * int(float(product.get('rating', 4.0)))}</p>
                    <button class="btn btn-primary" onclick="addToCart('{product.get('name', 'Product')}')">Add to Cart</button>
                </div>'''
                
            grid_html += '</div></div>'
            html_parts.append(grid_html)
            
        elif comp_type == 'button':
            text = component.get('text', 'Button')
            btn_class = 'btn-primary' if component.get('primary') else 'btn-secondary'
            button_html = f'<div class="component"><button class="btn {btn_class}">{text}</button></div>'
            html_parts.append(button_html)
            
        elif comp_type == 'progress_indicator':
            steps = component.get('steps', [])
            progress_html = '<div class="component"><div class="progress-indicator">'
            
            for i, step in enumerate(steps):
                step_id = step.lower()
                active_class = 'active' if i == 0 else ''
                progress_html += f'<div class="progress-step checkout-step {active_class}" onclick="showCheckoutStep(\'{step_id}\')">{step}</div>'
                
            progress_html += '</div>'
            
            # Add step content areas
            progress_html += '''
            <div class="step-content" id="step-cart" style="display: block;">
                <h3>Shopping Cart</h3>
                <div class="cart-items-list">
                    <div class="cart-item">Sample Product 1 - $29.99</div>
                    <div class="cart-item">Sample Product 2 - $39.99</div>
                </div>
                <div class="cart-total">Total: $69.98</div>
                <button class="btn btn-primary" onclick="proceedToShipping()">Place Order</button>
            </div>
            
            <div class="step-content" id="step-shipping" style="display: none;">
                <h3>Shipping Information</h3>
                <form id="shippingForm">
                    <input type="text" placeholder="Full Name" required style="width: 100%; margin: 10px 0; padding: 10px;">
                    <input type="text" placeholder="Address" required style="width: 100%; margin: 10px 0; padding: 10px;">
                    <input type="text" placeholder="City" required style="width: 100%; margin: 10px 0; padding: 10px;">
                    <input type="text" placeholder="Postal Code" required style="width: 100%; margin: 10px 0; padding: 10px;">
                </form>
                <button class="btn btn-primary" onclick="processShipping()">Continue to Payment</button>
            </div>
            
            <div class="step-content" id="step-payment" style="display: none;">
                <h3>Payment Information</h3>
                <form id="paymentForm">
                    <input type="text" placeholder="Card Number" required style="width: 100%; margin: 10px 0; padding: 10px;">
                    <input type="text" placeholder="Expiry Date (MM/YY)" required style="width: 100%; margin: 10px 0; padding: 10px;">
                    <input type="text" placeholder="CVV" required style="width: 100%; margin: 10px 0; padding: 10px;">
                </form>
                <button class="btn btn-primary" onclick="processPayment()">Place Order</button>
            </div>
            
            <div class="step-content" id="step-confirmation" style="display: none;">
                <h3>Order Confirmation</h3>
                <div class="confirmation-details">
                    <p>✅ Your order has been placed successfully!</p>
                    <p>Order Number: #ORD-2025-001</p>
                    <p>Total: $69.98</p>
                    <p>You will receive a confirmation email shortly.</p>
                </div>
            </div>
            </div>'''
            html_parts.append(progress_html)
            
        elif comp_type == 'cart_items':
            count = component.get('count', 3)
            cart_html = '<div class="component"><h3>Cart Items</h3>'
            
            for i in range(count):
                cart_html += f'''
                <div class="cart-item">
                    <div>Product {i+1}</div>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="updateQuantity(-1)">-</button>
                        <span>1</span>
                        <button class="quantity-btn" onclick="updateQuantity(1)">+</button>
                    </div>
                    <div>$99.99</div>
                </div>'''
                
            cart_html += '</div>'
            html_parts.append(cart_html)
    
    return '\n'.join(html_parts)
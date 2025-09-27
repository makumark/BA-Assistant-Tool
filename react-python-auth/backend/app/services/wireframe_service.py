"""
Wireframe Generation Service
AI-powered wireframe generation based on user stories and functional requirements
"""
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class WireframeComponent:
    type: str
    label: str
    position: str
    properties: Dict[str, Any]

@dataclass
class WireframePage:
    page_name: str
    page_type: str
    components: List[WireframeComponent]
    layout: str

def generate_wireframe_from_user_stories(project_name: str, user_stories: List[Dict], domain: str = "generic") -> str:
    """
    Generate HTML wireframes based on user stories and domain
    """
    print(f"🎨 Generating wireframes for {project_name} in {domain} domain")
    
    # Analyze user stories to determine page types needed
    pages = _analyze_user_stories_for_pages(user_stories, domain)
    
    # Generate wireframe HTML
    wireframe_html = _generate_wireframe_html(project_name, pages, domain)
    
    return wireframe_html

def generate_wireframe_from_frd(project_name: str, frd_content: str, domain: str = "generic") -> str:
    """
    Generate wireframes from FRD content by extracting user stories
    """
    print(f"🎨 Extracting user stories from FRD for wireframe generation")
    
    # Extract user stories from FRD
    user_stories = _extract_user_stories_from_frd(frd_content)
    
    # Generate wireframes
    return generate_wireframe_from_user_stories(project_name, user_stories, domain)

def _analyze_user_stories_for_pages(user_stories: List[Dict], domain: str) -> List[WireframePage]:
    """
    Analyze user stories to determine what pages and components are needed
    """
    pages = []
    
    # Always start with common pages
    pages.append(_create_login_page())
    pages.append(_create_dashboard_page(domain))
    
    # Analyze user stories for specific pages
    for story in user_stories:
        story_text = f"{story.get('goal', '')} {story.get('benefit', '')}".lower()
        role = story.get('role', '').lower()
        
        # Determine page types based on story content
        if any(keyword in story_text for keyword in ['form', 'create', 'add', 'register', 'input']):
            pages.append(_create_form_page(story, domain))
        
        if any(keyword in story_text for keyword in ['list', 'view', 'browse', 'search', 'manage']):
            pages.append(_create_list_page(story, domain))
        
        if any(keyword in story_text for keyword in ['detail', 'edit', 'update', 'profile']):
            pages.append(_create_detail_page(story, domain))
        
        if any(keyword in story_text for keyword in ['report', 'analytics', 'dashboard', 'chart']):
            pages.append(_create_report_page(story, domain))
    
    # Remove duplicates and return unique pages
    unique_pages = []
    seen_names = set()
    for page in pages:
        if page.page_name not in seen_names:
            unique_pages.append(page)
            seen_names.add(page.page_name)
    
    return unique_pages[:8]  # Limit to 8 pages for clarity

def _create_login_page() -> WireframePage:
    """Create login page wireframe"""
    components = [
        WireframeComponent("header", "App Logo", "top-center", {"size": "large"}),
        WireframeComponent("form", "Login Form", "center", {
            "fields": ["Email/Username", "Password"],
            "buttons": ["Sign In", "Forgot Password"],
            "links": ["Create Account"]
        }),
        WireframeComponent("footer", "Footer Links", "bottom", {"links": ["Terms", "Privacy", "Support"]})
    ]
    return WireframePage("Login", "authentication", components, "centered")

def _create_dashboard_page(domain: str) -> WireframePage:
    """Create main dashboard page wireframe"""
    components = [
        WireframeComponent("navigation", "Main Navigation", "top", {"items": ["Home", "Manage", "Reports", "Settings"]}),
        WireframeComponent("breadcrumb", "Breadcrumb", "top-left", {"path": "Home > Dashboard"}),
        WireframeComponent("stats", "Key Metrics", "top-row", {"metrics": _get_domain_metrics(domain)}),
        WireframeComponent("chart", "Main Chart/Graph", "center-left", {"type": "line", "title": "Trends"}),
        WireframeComponent("list", "Recent Items", "center-right", {"title": "Recent Activity", "items": 5}),
        WireframeComponent("actions", "Quick Actions", "bottom", {"buttons": _get_domain_actions(domain)})
    ]
    return WireframePage("Dashboard", "dashboard", components, "grid")

def _create_form_page(story: Dict, domain: str) -> WireframePage:
    """Create form page based on user story"""
    story_text = f"{story.get('goal', '')} {story.get('benefit', '')}".lower()
    role = story.get('role', '').lower()
    
    # Determine form type and fields based on story
    form_title = "Create New Item"
    fields = ["Name", "Description", "Status"]
    
    if any(keyword in story_text for keyword in ['course', 'learning', 'education']):
        form_title = "Create Course"
        fields = ["Course Name", "Description", "Duration", "Prerequisites", "Learning Objectives"]
    elif any(keyword in story_text for keyword in ['customer', 'contact', 'lead']):
        form_title = "Add Customer/Contact" 
        fields = ["Full Name", "Email", "Phone", "Company", "Lead Source", "Notes"]
    elif any(keyword in story_text for keyword in ['product', 'catalog', 'inventory']):
        form_title = "Add Product"
        fields = ["Product Name", "SKU", "Price", "Category", "Description", "Images"]
    elif any(keyword in story_text for keyword in ['order', 'purchase', 'checkout']):
        form_title = "Create Order"
        fields = ["Customer", "Products", "Quantity", "Shipping Address", "Payment Method"]
    
    components = [
        WireframeComponent("navigation", "Main Navigation", "top", {"items": ["Back", "Save", "Cancel"]}),
        WireframeComponent("header", form_title, "top-center", {"size": "large"}),
        WireframeComponent("form", "Input Form", "center", {
            "fields": fields,
            "buttons": ["Save", "Save & Continue", "Cancel"],
            "validation": True
        }),
        WireframeComponent("help", "Help/Tips", "right-sidebar", {"content": "Form guidance and tips"})
    ]
    return WireframePage(form_title.replace(" ", "_"), "form", components, "form-layout")

def _create_list_page(story: Dict, domain: str) -> WireframePage:
    """Create list/table page based on user story"""
    story_text = f"{story.get('goal', '')} {story.get('benefit', '')}".lower()
    
    # Determine list type based on story
    list_title = "Item List"
    columns = ["Name", "Status", "Date", "Actions"]
    
    if any(keyword in story_text for keyword in ['course', 'learning']):
        list_title = "Course Catalog"
        columns = ["Course Name", "Category", "Duration", "Enrolled", "Status", "Actions"]
    elif any(keyword in story_text for keyword in ['customer', 'contact', 'lead']):
        list_title = "Customer/Contact List"
        columns = ["Name", "Email", "Company", "Lead Score", "Last Contact", "Actions"]
    elif any(keyword in story_text for keyword in ['product', 'catalog']):
        list_title = "Product Catalog"
        columns = ["Product Name", "SKU", "Price", "Stock", "Category", "Actions"]
    elif any(keyword in story_text for keyword in ['order', 'transaction']):
        list_title = "Order History"
        columns = ["Order ID", "Customer", "Total", "Status", "Date", "Actions"]
    
    components = [
        WireframeComponent("navigation", "Main Navigation", "top", {"items": ["Home", "Add New", "Import", "Export"]}),
        WireframeComponent("search", "Search & Filters", "top-right", {"filters": ["Status", "Category", "Date Range"]}),
        WireframeComponent("table", list_title, "center", {
            "columns": columns,
            "pagination": True,
            "sorting": True,
            "actions": ["Edit", "Delete", "View"]
        }),
        WireframeComponent("summary", "Summary Stats", "bottom", {"stats": ["Total Items", "Active", "Inactive"]})
    ]
    return WireframePage(list_title.replace(" ", "_"), "list", components, "table-layout")

def _create_detail_page(story: Dict, domain: str) -> WireframePage:
    """Create detail/profile page based on user story"""
    story_text = f"{story.get('goal', '')} {story.get('benefit', '')}".lower()
    
    detail_title = "Item Details"
    if any(keyword in story_text for keyword in ['course', 'learning']):
        detail_title = "Course Details"
    elif any(keyword in story_text for keyword in ['customer', 'contact', 'profile']):
        detail_title = "Customer Profile"
    elif any(keyword in story_text for keyword in ['product']):
        detail_title = "Product Details"
    elif any(keyword in story_text for keyword in ['order']):
        detail_title = "Order Details"
    
    components = [
        WireframeComponent("navigation", "Breadcrumb Navigation", "top", {"path": "Home > List > Details"}),
        WireframeComponent("header", detail_title, "top-center", {"actions": ["Edit", "Delete", "Share"]}),
        WireframeComponent("info", "Basic Information", "left-column", {"fields": ["Name", "Description", "Status", "Created Date"]}),
        WireframeComponent("details", "Additional Details", "center-column", {"tabs": ["Overview", "History", "Related"]}),
        WireframeComponent("actions", "Quick Actions", "right-column", {"buttons": ["Edit", "Duplicate", "Archive"]}),
        WireframeComponent("activity", "Activity Timeline", "bottom", {"timeline": True, "expandable": True})
    ]
    return WireframePage(detail_title.replace(" ", "_"), "detail", components, "detail-layout")

def _create_report_page(story: Dict, domain: str) -> WireframePage:
    """Create report/analytics page based on user story"""
    components = [
        WireframeComponent("navigation", "Report Navigation", "top", {"items": ["Dashboard", "Custom Reports", "Scheduled"]}),
        WireframeComponent("filters", "Report Filters", "top-right", {"filters": ["Date Range", "Category", "Status"]}),
        WireframeComponent("kpi", "Key Performance Indicators", "top-row", {"metrics": 4}),
        WireframeComponent("chart1", "Primary Chart", "center-left", {"type": "bar", "title": "Performance Metrics"}),
        WireframeComponent("chart2", "Secondary Chart", "center-right", {"type": "pie", "title": "Distribution"}),
        WireframeComponent("table", "Detailed Data", "bottom", {"export": True, "pagination": True})
    ]
    return WireframePage("Reports_Analytics", "report", components, "analytics-layout")

def _get_domain_metrics(domain: str) -> List[str]:
    """Get relevant metrics based on domain"""
    domain_metrics = {
        "marketing": ["Total Leads", "Conversion Rate", "Campaign Performance", "ROI"],
        "ecommerce": ["Total Orders", "Revenue", "Cart Abandonment", "Top Products"],
        "healthcare": ["Patient Count", "Appointments Today", "Satisfaction Score", "Wait Time"],
        "education": ["Active Students", "Course Completion", "Enrollment Rate", "Engagement"],
        "financial": ["Portfolio Value", "Risk Score", "Returns", "Active Trades"],
        "generic": ["Total Records", "Active Users", "Completion Rate", "Growth Rate"]
    }
    return domain_metrics.get(domain, domain_metrics["generic"])

def _get_domain_actions(domain: str) -> List[str]:
    """Get relevant quick actions based on domain"""
    domain_actions = {
        "marketing": ["Create Campaign", "Add Lead", "Schedule Email", "View Analytics"],
        "ecommerce": ["Add Product", "Process Order", "Update Inventory", "View Sales"],
        "healthcare": ["Schedule Appointment", "Add Patient", "View Records", "Generate Report"],
        "education": ["Create Course", "Enroll Student", "Grade Assignment", "View Progress"],
        "financial": ["New Investment", "Portfolio Review", "Risk Assessment", "Generate Statement"],
        "generic": ["Add New", "Generate Report", "Update Settings", "View All"]
    }
    return domain_actions.get(domain, domain_actions["generic"])

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
        # Look for requirement-like content
        requirement_pattern = r'([A-Z][^.]+(?:manage|create|view|process|handle|track|generate|provide)[^.]*)'
        requirements = re.findall(requirement_pattern, frd_content, re.MULTILINE)
        
        for i, req in enumerate(requirements[:10]):  # Limit to 10 requirements
            user_stories.append({
                "role": "User",
                "goal": f"have {req.lower()}",
                "benefit": "accomplish business objectives efficiently"
            })
    
    return user_stories[:10]  # Limit to 10 user stories

def _generate_wireframe_html(project_name: str, pages: List[WireframePage], domain: str) -> str:
    """Generate complete HTML wireframe with interactive navigation"""
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 Wireframes: {project_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc;
            color: #1a202c;
        }}
        
        .wireframe-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .wireframe-header {{
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 24px;
            text-align: center;
        }}
        
        .wireframe-header h1 {{
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 28px;
        }}
        
        .domain-badge {{
            background: #4299e1;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            display: inline-block;
        }}
        
        .page-navigation {{
            background: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .page-nav-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .page-tab {{
            padding: 8px 16px;
            background: #e2e8f0;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }}
        
        .page-tab:hover {{
            background: #cbd5e0;
        }}
        
        .page-tab.active {{
            background: #4299e1;
            color: white;
        }}
        
        .wireframe-page {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 24px;
            overflow: hidden;
            display: none;
        }}
        
        .wireframe-page.active {{
            display: block;
        }}
        
        .page-header {{
            background: #edf2f7;
            padding: 16px 24px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        .page-title {{
            font-size: 20px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 4px;
        }}
        
        .page-type {{
            font-size: 12px;
            color: #718096;
            text-transform: uppercase;
        }}
        
        .wireframe-canvas {{
            padding: 24px;
            min-height: 600px;
            position: relative;
        }}
        
        .wireframe-component {{
            border: 2px dashed #cbd5e0;
            background: #f7fafc;
            margin-bottom: 16px;
            padding: 16px;
            border-radius: 8px;
            position: relative;
            transition: all 0.2s;
        }}
        
        .wireframe-component:hover {{
            border-color: #4299e1;
            background: #ebf8ff;
        }}
        
        .component-label {{
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .component-icon {{
            width: 16px;
            height: 16px;
            background: #4299e1;
            border-radius: 3px;
        }}
        
        .component-details {{
            font-size: 12px;
            color: #718096;
            line-height: 1.4;
        }}
        
        .layout-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        
        .layout-centered {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 400px;
        }}
        
        .layout-sidebar {{
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 16px;
        }}
        
        .form-fields {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 12px;
        }}
        
        .form-field {{
            border: 1px solid #e2e8f0;
            height: 36px;
            border-radius: 4px;
            background: white;
            padding: 8px 12px;
            font-size: 14px;
            color: #a0aec0;
        }}
        
        .form-buttons {{
            display: flex;
            gap: 8px;
            margin-top: 16px;
        }}
        
        .form-button {{
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            background: #f7fafc;
            font-size: 14px;
            color: #4a5568;
        }}
        
        .form-button.primary {{
            background: #4299e1;
            color: white;
            border-color: #4299e1;
        }}
        
        .table-mockup {{
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            margin-top: 12px;
        }}
        
        .table-header {{
            background: #edf2f7;
            padding: 12px;
            font-weight: 600;
            font-size: 14px;
            color: #4a5568;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .table-row {{
            padding: 12px;
            border-bottom: 1px solid #f7fafc;
            font-size: 14px;
            color: #718096;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 12px;
        }}
        
        .stat-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 16px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #718096;
            text-transform: uppercase;
            margin-top: 4px;
        }}
        
        .navigation-bar {{
            background: #2d3748;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 16px;
        }}
        
        .nav-item {{
            color: #e2e8f0;
            font-size: 14px;
            text-decoration: none;
            padding: 6px 12px;
            border-radius: 4px;
            transition: background 0.2s;
        }}
        
        .nav-item:hover {{
            background: #4a5568;
            color: white;
        }}
        
        .chart-placeholder {{
            background: #f7fafc;
            border: 2px dashed #cbd5e0;
            height: 200px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #718096;
            margin-top: 12px;
        }}
        
        .responsive-note {{
            background: #fff5cd;
            border: 1px solid #f6e05e;
            border-radius: 6px;
            padding: 12px;
            margin-top: 20px;
            font-size: 12px;
            color: #744210;
        }}
    </style>
</head>
<body>
    <div class="wireframe-container">
        <div class="wireframe-header">
            <h1>🎨 Interactive Wireframes</h1>
            <h2>{project_name}</h2>
            <div class="domain-badge">{domain.upper()} DOMAIN</div>
            <div style="margin-top: 12px; font-size: 14px; color: #718096;">
                Generated from user stories • Click tabs to navigate between pages
            </div>
        </div>
        
        <div class="page-navigation">
            <div class="page-nav-tabs">
                {_generate_page_tabs(pages)}
            </div>
        </div>
        
        {_generate_all_pages_html(pages)}
        
        <div class="responsive-note">
            <strong>📱 Responsive Design Note:</strong> These wireframes represent desktop layouts. 
            Mobile versions would stack components vertically and optimize for touch interaction.
        </div>
    </div>
    
    <script>
        function showPage(pageId) {{
            // Hide all pages
            document.querySelectorAll('.wireframe-page').forEach(page => {{
                page.classList.remove('active');
            }});
            
            // Hide all tabs
            document.querySelectorAll('.page-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected page
            document.getElementById(pageId).classList.add('active');
            
            // Activate selected tab
            document.querySelector(`[onclick="showPage('${{pageId}}')"]`).classList.add('active');
        }}
        
        // Show first page by default
        document.addEventListener('DOMContentLoaded', function() {{
            const firstPage = document.querySelector('.wireframe-page');
            const firstTab = document.querySelector('.page-tab');
            if (firstPage && firstTab) {{
                firstPage.classList.add('active');
                firstTab.classList.add('active');
            }}
        }});
    </script>
</body>
</html>
"""
    return html

def _generate_page_tabs(pages: List[WireframePage]) -> str:
    """Generate navigation tabs for pages"""
    tabs = []
    for i, page in enumerate(pages):
        page_id = f"page_{i}"
        display_name = page.page_name.replace("_", " ")
        tabs.append(f'<button class="page-tab" onclick="showPage(\'{page_id}\')">{display_name}</button>')
    return "\n".join(tabs)

def _generate_all_pages_html(pages: List[WireframePage]) -> str:
    """Generate HTML for all wireframe pages"""
    pages_html = []
    
    for i, page in enumerate(pages):
        page_id = f"page_{i}"
        page_html = f"""
        <div class="wireframe-page" id="{page_id}">
            <div class="page-header">
                <div class="page-title">{page.page_name.replace("_", " ")}</div>
                <div class="page-type">{page.page_type}</div>
            </div>
            <div class="wireframe-canvas {_get_layout_class(page.layout)}">
                {_generate_components_html(page.components, page.page_type)}
            </div>
        </div>
        """
        pages_html.append(page_html)
    
    return "\n".join(pages_html)

def _get_layout_class(layout: str) -> str:
    """Get CSS class for layout"""
    layout_classes = {
        "grid": "layout-grid",
        "centered": "layout-centered", 
        "sidebar": "layout-sidebar",
        "form-layout": "",
        "table-layout": "",
        "detail-layout": "layout-grid",
        "analytics-layout": ""
    }
    return layout_classes.get(layout, "")

def _generate_components_html(components: List[WireframeComponent], page_type: str) -> str:
    """Generate HTML for wireframe components"""
    components_html = []
    
    for component in components:
        component_html = f"""
        <div class="wireframe-component">
            <div class="component-label">
                <div class="component-icon"></div>
                {component.label}
            </div>
            <div class="component-details">
                {_generate_component_content(component)}
            </div>
        </div>
        """
        components_html.append(component_html)
    
    return "\n".join(components_html)

def _generate_component_content(component: WireframeComponent) -> str:
    """Generate content for specific component types"""
    if component.type == "form":
        fields_html = []
        for field in component.properties.get("fields", []):
            fields_html.append(f'<input class="form-field" placeholder="{field}" readonly>')
        
        buttons_html = []
        for button in component.properties.get("buttons", []):
            btn_class = "primary" if "save" in button.lower() or "submit" in button.lower() else ""
            buttons_html.append(f'<button class="form-button {btn_class}">{button}</button>')
        
        return f"""
        <div class="form-fields">
            {''.join(fields_html)}
        </div>
        <div class="form-buttons">
            {''.join(buttons_html)}
        </div>
        """
    
    elif component.type == "table":
        columns = component.properties.get("columns", [])
        columns_html = " | ".join(columns)
        return f"""
        <div class="table-mockup">
            <div class="table-header">{columns_html}</div>
            <div class="table-row">Sample data row 1...</div>
            <div class="table-row">Sample data row 2...</div>
            <div class="table-row">Sample data row 3...</div>
        </div>
        """
    
    elif component.type == "stats":
        metrics = component.properties.get("metrics", [])
        if isinstance(metrics, list):
            stats_html = []
            for metric in metrics:
                stats_html.append(f"""
                <div class="stat-card">
                    <div class="stat-value">1,234</div>
                    <div class="stat-label">{metric}</div>
                </div>
                """)
            return f'<div class="stats-grid">{"".join(stats_html)}</div>'
    
    elif component.type == "navigation":
        nav_items = component.properties.get("items", [])
        nav_html = []
        for item in nav_items:
            nav_html.append(f'<a href="#" class="nav-item">{item}</a>')
        return f'<div class="navigation-bar">{"".join(nav_html)}</div>'
    
    elif component.type == "chart":
        chart_type = component.properties.get("type", "line")
        title = component.properties.get("title", "Chart")
        return f'<div class="chart-placeholder">📊 {title} ({chart_type.upper()} CHART)</div>'
    
    # Default content for other component types
    return f"Component Type: {component.type.upper()}<br>Position: {component.position}<br>Properties: {len(component.properties)} items"
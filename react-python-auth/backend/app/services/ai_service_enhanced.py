from typing import Dict, Any, List, Optional
import os
import re
import logging

logger = logging.getLogger(__name__)

try:
    import openai
except Exception:
    openai = None


def _safe(x: Any) -> str:
    return "" if x is None else str(x).strip()


def _expand_common_abbreviations(text: str) -> str:
    """Expand common abbreviations for clarity in fund management and financial domains."""
    if not text:
        return text
    
    expanded_text = text
    
    # Handle compound abbreviations first (exact matches)
    compound_replacements = {
        'KYC/AML': 'Know Your Customer/Anti-Money Laundering (KYC/AML)',
        'UI/UX': 'User Interface (UI)/User Experience (UX)',
        'AI/ML': 'Artificial Intelligence (AI)/Machine Learning (ML)'
    }
    
    for abbr, expansion in compound_replacements.items():
        if abbr in expanded_text and expansion not in expanded_text:
            expanded_text = expanded_text.replace(abbr, expansion)
    
    # Then handle single abbreviations (word boundary matches)
    single_abbreviations = {
        'KYC': 'Know Your Customer (KYC)',
        'AML': 'Anti-Money Laundering (AML)', 
        'e-sign': 'electronic signature (e-sign)',
        'NAV': 'Net Asset Value (NAV)',
        'LP': 'Limited Partner (LP)',
        'GP': 'General Partner (GP)',
        'API': 'Application Programming Interface (API)',
        'CRM': 'Customer Relationship Management (CRM)',
        'UI': 'User Interface (UI)',
        'UX': 'User Experience (UX)',
        'MVP': 'Minimum Viable Product (MVP)',
        'GDPR': 'General Data Protection Regulation (GDPR)',
        'SSO': 'Single Sign-On (SSO)',
        'MFA': 'Multi-Factor Authentication (MFA)',
        'RBAC': 'Role-Based Access Control (RBAC)',
        'AWS': 'Amazon Web Services (AWS)',
        'AI': 'Artificial Intelligence (AI)',
        'ML': 'Machine Learning (ML)',
        'BI': 'Business Intelligence (BI)',
        'ROI': 'Return on Investment (ROI)',
        'SLA': 'Service Level Agreement (SLA)',
        'ESG': 'Environmental, Social, and Governance (ESG)',
        'SEC': 'Securities and Exchange Commission (SEC)'
    }
    
    for abbr, expansion in single_abbreviations.items():
        pattern = r'\b' + re.escape(abbr) + r'\b'
        # Only expand if the expansion isn't already in the text
        if re.search(pattern, expanded_text, re.IGNORECASE) and expansion not in expanded_text:
            expanded_text = re.sub(pattern, expansion, expanded_text, flags=re.IGNORECASE)
    
    return expanded_text


def _merge_requirements(inputs: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key in ("briefRequirements", "requirements", "req", "scope", "objectives", "budget", "assumptions", "constraints"):
        v = _safe(inputs.get(key))
        if v:
            parts.append(v)
    return "\n".join(parts)


def _split_items(text: str) -> List[str]:
    if not text:
        return []
    items = re.split(r'\r?\n|;|\u2022|\t|\r', text)
    out: List[str] = []
    for i in items:
        s = i.strip()
        if not s:
            continue
        s = re.sub(r'^[0-9\.\)\-]+\s*', '', s)
        out.append(s)
    if len(out) == 1 and ("," in out[0] or ";" in out[0]):
        parts = re.split(r',|;', out[0])
        return [p.strip() for p in parts if p.strip()]
    return out


def _to_requirement_sentence(item: str) -> str:
    s = item.strip()
    if not s:
        return ""
    if re.match(r'(?i)the system shall', s):
        return s if s.endswith(".") else s + "."
    s = re.sub(r'^[Tt]o\s+', '', s)
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    s = re.sub(r'\bability to\b', 'be able to', s, flags=re.I)
    s = re.sub(r'\bshall included\b', 'shall include', s, flags=re.I)
    return "The system shall " + s.rstrip(".") + "."


def _generate_exec_summary(project: str, req_text: str) -> str:
    lead = f"{project} BRD: " if project else "This BRD: "
    core = req_text.split("\n", 1)[0] if req_text else "define core features such as secure login and payments"
    core = core if len(core) < 220 else core[:217] + "..."
    return lead + core


def _derive_objectives(req_text: str) -> List[str]:
    objs: List[str] = []
    m = re.search(r'(\d+%|\d+\s*percent)', req_text)
    if m:
        objs.append(f"Increase digital adoption to {m.group(1)}.")
    objs.extend([
        "Reduce manual customer support inquiries related to balances and statements.",
        "Improve payment straight-through-processing and reduce failed transactions.",
    ])
    return objs[:4]


def _derive_budget(inputs: Dict[str, Any]) -> str:
    b = _safe(inputs.get("budget"))
    if b:
        return b
    merged = _merge_requirements(inputs)
    m = re.search(r'(INR|Rs\.?|₹|\$|USD)\s*([0-9,]+(?:\.\d+)?)', merged, re.IGNORECASE)
    if m:
        return f"Estimated budget: {m.group(1)} {m.group(2)}"
    return ""


def _local_fallback(project: str, inputs: Dict[str, Any], version: int) -> str:
    req_text = _merge_requirements(inputs)
    val_text = _safe(inputs.get("validations") or inputs.get("validation") or "")
    req_items = _split_items(req_text)
    val_items = _split_items(val_text)

    exec_summary = _generate_exec_summary(project, req_text)
    scope = _safe(inputs.get("scope") or "")
    objectives = _derive_objectives(req_text)
    budget = _derive_budget(inputs)
    assumptions = _safe(inputs.get("assumptions") or "Core systems available; test environments mirror production.")
    constraints = _safe(inputs.get("constraints") or "")

    brd_list_html = ""
    if req_items:
        for it in req_items:
            sentence = _to_requirement_sentence(it)
            if sentence:
                brd_list_html += f"<li>{sentence}</li>\n"
    else:
        brd_list_html = "<li>The system shall implement secure customer authentication and account overview.</li>"

    val_list_html = ""
    if val_items:
        for it in val_items:
            txt = it.rstrip(".")
            if not re.match(r'(?i)(enforce|validate|require)', txt):
                txt = "Enforce " + txt
            val_list_html += f"<li>{txt.rstrip('.') }.</li>\n"
    else:
        val_list_html = "<li>Enforce strong authentication and integrity of audit logs.</li>"

    html = f"""
<div style="font-family:Arial,Helvetica,sans-serif;color:#111827;padding:18px;">
  <h1 style="text-align:center;margin-bottom:6px;">Business Requirement Document (BRD)</h1>
  <h2 style="text-align:center;margin-top:2px;">{project} - BRD Version-{version}</h2>
  <hr/>
  <h3>Executive Summary</h3>
  <p>{exec_summary}</p>

  <h3>Project Scope</h3>
  <p>{scope or 'In scope: Retail internet banking features for account overview, payments and beneficiary management.'}</p>

  <h3>Business Objectives</h3>
  <ul>
    {''.join(f'<li>{o}</li>' for o in objectives) if objectives else '<li>Deliver secure, reliable and user-friendly services.</li>'}
  </ul>

  <h3>Budget Details</h3>
  <p>{budget or 'Budget to be estimated. Provide CAPEX/OPEX estimates during solution design.'}</p>

  <h3>Business Requirements</h3>
  <ol>
    {brd_list_html}
  </ol>

  <h3>Assumptions</h3>
  <p>{assumptions}</p>

  <h3>Constraints</h3>
  <p>{constraints or 'Standard regulatory, integration and schedule constraints apply.'}</p>

  <h3>Validations & Acceptance Criteria</h3>
  <ol>
    {val_list_html}
  </ol>

  <h3>Appendices</h3>
  <p>Appendix A: Glossary<br/>Appendix B: References</p>

  <hr/><p style="font-size:11px;color:#6b7280;">Generated by BA Assistant Tool (fallback)</p>
</div>
"""
    return html


def _use_openai_legacy() -> bool:
    return bool(openai and getattr(openai, "ChatCompletion", None))


def _strip_code_fences(text: str) -> str:
    if not text:
        return text
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def _call_openai_chat(messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not (openai and api_key):
        return None
    try:
        if _use_openai_legacy():
            openai.api_key = api_key
            resp = openai.ChatCompletion.create(
                model=model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = resp.choices[0].message.content if hasattr(resp.choices[0].message, "content") else resp.choices[0].text
            return _strip_code_fences(content.strip())
        else:
            # try new OpenAI client (if installed)
            try:
                from openai import OpenAI  # type: ignore
                client = OpenAI(api_key=api_key)
                resp = client.chat.completions.create(
                    model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                # try to access content safely
                choices = getattr(resp, "choices", None)
                if choices and len(choices) > 0:
                    msg = choices[0].get("message") if isinstance(choices[0], dict) else choices[0].message
                    content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", None)
                    if content:
                        return _strip_code_fences(str(content).strip())
            except Exception:
                return None
    except Exception as e:
        logger.exception("OpenAI call failed: %s", e)
    return None


def generate_brd_html(project: str, inputs: Dict[str, Any], version: int) -> str:
    """Generate BRD HTML with EPICs structure for any domain."""
    req_text = _merge_requirements(inputs)
    val_text = _safe(inputs.get("validations") or inputs.get("validation") or "")

    # Enhanced system prompt for EPICs-based BRD
    system = (
        "You are a senior Business Analyst expert. Generate a comprehensive Business Requirements Document (BRD) "
        "using EPICs methodology. Structure Business Requirements as EPICs (EPIC-01, EPIC-02, etc.) where each "
        "EPIC represents a major business capability. CRITICAL CONSTRAINTS FOR EPICs: "
        "1. Source ONLY from Business Objectives and items explicitly marked 'Included' in scope "
        "2. NEVER include: Budget amounts, Cost estimates, Environment details (sandbox/production), "
        "   Items marked 'Excluded', Assumptions, Validations, Technical environments "
        "3. Each EPIC must be a complete business capability (4+ words), not fragments or cost details "
        "4. Maximum 8 EPICs representing major business functions only. "
        "Make it domain-agnostic but professional. Output clean HTML with proper headings and formatting."
    )
    
    user_prompt = (
        f"Project: {project}\nVersion: {version}\n\n"
        "Requirements Input:\n"
        f"{req_text}\n\nValidations:\n{val_text}\n\n"
        "Generate a BRD with these sections:\n"
        "1. Executive Summary (2-3 sentences about initiative value)\n"
        "2. Project Scope (In scope / Out of scope)\n"
        "3. Business Objectives (3-5 measurable goals)\n"
        "4. Budget Details (structure if not provided)\n"
        "5. Business Requirements (EPICs) - Format as 'EPIC-XX [Name]: [Description]'\n"
        "6. Assumptions\n"
        "7. Constraints\n"
        "8. Validations & Acceptance Criteria\n\n"
        "IMPORTANT EPIC GENERATION RULES: "
        "- Create EPICs ONLY from Business Objectives and items explicitly marked 'Included' in scope "
        "- NEVER include in EPICs: Budget amounts (₹60-₹110 Lakh), Environment details (sandbox/production), "
        "  Items marked 'Excluded', Assumptions, Validations, Cost estimates, Technical environments "
        "- Each EPIC must represent a complete business capability (not fragments like 'Excluded — Full') "
        "- Maximum 8 EPICs representing major business functions derived from objectives and included scope only "
        "Create 6-10 meaningful EPICs that align with the stated objectives and scope. Be comprehensive yet concise."
    )

    html = _call_openai_chat(
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user_prompt}],
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.7,
        max_tokens=2500,
    )

    if html and "<" in html and "EPIC" in html:
        return html

    # Enhanced fallback for EPICs-based BRD
    return _generate_epics_fallback_brd(project, inputs, version)


def _extract_included_scope_only(scope_text: str) -> List[str]:
    """Extract only the included scope items, excluding anything under 'Excluded'."""
    if not scope_text:
        return []
    
    included_items = []
    lines = scope_text.split('\n')
    
    in_included_section = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if we're entering included section
        if line.lower().startswith('included'):
            in_included_section = True
            continue
            
        # Check if we're entering excluded section - stop processing
        if line.lower().startswith('excluded'):
            break
            
        # If we're in included section, collect items
        if in_included_section and line:
            # Clean up bullet points and numbering
            clean_line = re.sub(r'^[\u2022\-\*•]+\s*', '', line)
            clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
            
            if clean_line and len(clean_line.split()) > 2:  # Only meaningful phrases
                included_items.append(clean_line)
    
    return included_items


def _extract_business_objectives(objectives_text: str) -> List[str]:
    """Extract business objectives as complete sentences/phrases."""
    if not objectives_text:
        return []
    
    objectives = []
    lines = objectives_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Clean up bullet points and numbering
        clean_line = re.sub(r'^[\u2022\-\*•]+\s*', '', line)
        clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
        
        # Only include meaningful objectives (not fragments)
        if clean_line and len(clean_line.split()) > 3:
            objectives.append(clean_line)
    
    return objectives


def _create_epics_from_business_capabilities(included_scope: List[str], objectives: List[str]) -> List[Dict[str, str]]:
    """Create EPICs from business capabilities, grouping related items."""
    epics = []
    
    # Keywords to exclude from EPIC generation
    exclude_keywords = [
        'excluded', 'budget', 'cost', 'environment', 'sandbox', 'production',
        'accounting replacement', 'valuation', 'registrar', 'transfer agent',
        'tax pack', 'automation', 'assumptions', 'validation', 'criteria'
    ]
    
    # Combine scope and objectives
    all_capabilities = included_scope + objectives
    
    # Filter and group capabilities into EPICs
    epic_counter = 1
    for capability in all_capabilities:
        # Skip if contains excluded keywords
        if any(keyword in capability.lower() for keyword in exclude_keywords):
            continue
            
        # Skip very short or fragment-like items
        if len(capability.split()) < 4:
            continue
            
        # Create EPIC title from first few words
        words = capability.split()
        title = ' '.join(words[:4]).title()
        
        # Expand abbreviations in the description
        description = _expand_common_abbreviations(capability)
        
        epics.append({
            'id': f'EPIC-{epic_counter:02d}',
            'title': title,
            'description': description
        })
        
        epic_counter += 1
        
        # Limit to 8 EPICs maximum
        if epic_counter > 8:
            break
    
    return epics


def _generate_epics_fallback_brd(project: str, inputs: Dict[str, Any], version: int) -> str:
    """Generate fallback BRD with EPICs structure when AI fails."""
    req_text = _merge_requirements(inputs)
    val_text = _safe(inputs.get("validations") or inputs.get("validation") or "")
    
    # Extract only Business Objectives and INCLUDED Scope for EPIC generation
    objectives_text = _safe(inputs.get("objectives") or "")
    scope_text = _safe(inputs.get("scope") or "")
    
    # Extract basic information from inputs
    domain = detect_domain(req_text) if req_text else "General Business"
    
    # Extract included scope items and business objectives
    included_scope = _extract_included_scope_only(scope_text)
    business_objectives = _extract_business_objectives(objectives_text)
    
    # Create EPICs from business capabilities only
    epics = _create_epics_from_business_capabilities(included_scope, business_objectives)
    
    # Generate EPICs HTML
    epics_html = ""
    
    if not epics:
        # Default EPICs when no valid capabilities found
        epics_html = """
        <ul style="list-style-type: none; padding-left: 0;">
          <li style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6;">
            <strong>EPIC-01 Business Process Optimization:</strong> Core business operations aligned with organizational objectives and strategic goals.
          </li>
          <li style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6;">
            <strong>EPIC-02 User Experience Enhancement:</strong> Improved user interfaces and workflows to meet business objectives and scope requirements.
          </li>
          <li style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6;">
            <strong>EPIC-03 Data Management & Analytics:</strong> Information management capabilities within defined scope to support business objectives.
          </li>
        </ul>
        """
    else:
        epics_html = '<ul style="list-style-type: none; padding-left: 0;">'
        for epic in epics:
            epics_html += f"""
            <li style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6;">
              <strong>{epic['id']} {epic['title']}:</strong> {epic['description']}
            </li>
            """
        epics_html += '</ul>'
    
    # Continue with existing logic
    if not epics:
            # Fallback to default EPICs if no valid items found
            epics_html = """
            <ul style="list-style-type: none; padding-left: 0;">
              <li style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6;">
                <strong>EPIC-01 Objective-Driven Operations:</strong> Core business capabilities to achieve stated objectives within defined scope.
              </li>
              <li style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6;">
                <strong>EPIC-02 Scope-Aligned Features:</strong> Essential features and functionalities aligned with project scope boundaries.
              </li>
            </ul>
            """
    
    # Validation items
    val_list = _br_to_list(val_text) if val_text else []
    val_html = ""
    if val_list:
        for i, val in enumerate(val_list, start=1):
            val_html += f"<li><strong>V-{i:03d}:</strong> {val.strip()}</li>\n"
    else:
        val_html = """
        <li><strong>Field Validations:</strong> Required field validation, format checking, data type and range validations, business rule validations</li>
        <li><strong>Business Validations:</strong> Process workflow validations, authorization checks, data integrity and consistency validations</li>
        <li><strong>Acceptance Criteria:</strong> All core functionality operates as specified, security requirements met, performance standards achieved</li>
        """

    return f"""
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #111827; padding: 24px; max-width: 1200px; line-height: 1.6;">
  <header style="text-align: center; margin-bottom: 32px; border-bottom: 2px solid #e5e7eb; padding-bottom: 16px;">
    <h1 style="color: #1f2937; margin-bottom: 8px; font-size: 28px;">Business Requirements Document (BRD)</h1>
    <h2 style="color: #6b7280; margin: 0; font-size: 20px; font-weight: normal;">{project} - Version {version}</h2>
    <p style="color: #9ca3af; margin: 8px 0 0 0; font-style: italic;">Domain: {domain.title()}</p>
  </header>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📋 Executive Summary</h3>
    <p>This initiative aims to deliver a comprehensive {domain.lower()} solution that addresses core operational requirements, enhances user experience, and drives business value through systematic implementation of essential capabilities across multiple business domains.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🎯 Project Scope</h3>
    <p><strong>In Scope:</strong> Core business functionality and user interfaces, essential integrations and data management, security and compliance features, basic reporting and analytics capabilities, mobile and web-based access.</p>
    <p><strong>Out of Scope (Initial Release):</strong> Advanced analytics and AI/ML features, third-party marketplace integrations, legacy system migrations (beyond data import), complex workflow automation.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🚀 Business Objectives</h3>
    <ul style="list-style-type: disc; padding-left: 24px;">
      <li>Improve operational efficiency and reduce manual processes by 40%</li>
      <li>Enhance user experience and satisfaction with modern interfaces</li>
      <li>Ensure compliance with industry standards and regulations</li>
      <li>Enable scalable growth and future enhancements</li>
      <li>Reduce operational costs and improve ROI within 18 months</li>
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">💰 Budget Details</h3>
    <p>Estimated budget range based on scope and complexity, covering UX/UI design, development, testing, deployment, integrations, security, and first-year support. Phased delivery approach recommended: MVP (core EPICs) followed by enhancement EPICs.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📊 Business Requirements (EPICs)</h3>
    <ul style="list-style-type: none; padding-left: 0;">
      {epics_html}
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📝 Assumptions</h3>
    <ul style="list-style-type: disc; padding-left: 24px;">
      <li>Required infrastructure and development resources are available</li>
      <li>Stakeholders will provide timely feedback and approvals</li>
      <li>Third-party services and integrations are accessible and reliable</li>
      <li>Security and compliance requirements are clearly defined</li>
      <li>APIs and data sources are available for integrations</li>
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">⚠️ Constraints</h3>
    <ul style="list-style-type: disc; padding-left: 24px;">
      <li>Budget and timeline limitations enforce phased delivery</li>
      <li>Technical infrastructure and platform constraints</li>
      <li>Regulatory and compliance requirements must be met</li>
      <li>Resource availability and technical expertise limitations</li>
      <li>Dependency on third-party providers for certain capabilities</li>
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">✅ Validations & Acceptance Criteria</h3>
    <ul style="list-style-type: none; padding-left: 0;">
      {val_html}
    </ul>
  </section>
</div>
"""


def detect_domain(text: str) -> str:
    """Detect the business domain from the text."""
    if not text:
        return "General Business"
    
    text_lower = text.lower()
    
    # Healthcare domain indicators
    if any(keyword in text_lower for keyword in ['patient', 'medical', 'healthcare', 'hospital', 'clinic', 'doctor', 'nurse', 'treatment', 'diagnosis']):
        return "Healthcare"
    
    # E-commerce domain indicators
    if any(keyword in text_lower for keyword in ['product', 'cart', 'checkout', 'payment', 'order', 'shipping', 'inventory', 'catalog', 'ecommerce', 'e-commerce']):
        return "E-commerce"
    
    # Banking/Finance domain indicators
    if any(keyword in text_lower for keyword in ['account', 'transaction', 'banking', 'finance', 'loan', 'credit', 'payment', 'money', 'currency']):
        return "Banking & Finance"
    
    # Education domain indicators
    if any(keyword in text_lower for keyword in ['student', 'course', 'education', 'learning', 'school', 'university', 'teacher', 'curriculum']):
        return "Education"
    
    # Manufacturing domain indicators
    if any(keyword in text_lower for keyword in ['manufacturing', 'production', 'factory', 'assembly', 'quality', 'supply chain', 'warehouse']):
        return "Manufacturing"
    
    # HR domain indicators
    if any(keyword in text_lower for keyword in ['employee', 'payroll', 'hr', 'human resources', 'recruitment', 'performance', 'training']):
        return "Human Resources"
    
    return "General Business"


def _extract_section(text: str, heading: str) -> str:
    """Extract a section from text based on heading."""
    pattern = rf"(?im)^\s*{re.escape(heading)}\s*(?:\n|:)\s*(.*?)(?=\n[A-Z][\w &/()\-\.:]{{2,}}(?:\n|:)|\Z)"
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else ""


def _generate_user_stories_fallback_frd(project: str, brd_text: str, version: int) -> str:
    """Generate User Stories-based FRD when AI fails."""
    # Extract domain and basic information
    detected_domain = detect_domain(brd_text)
    
    # Extract sections from BRD
    exec_summary = _extract_section(brd_text, "Executive Summary") or _safe(brd_text).split("\n", 1)[0]
    scope = _extract_section(brd_text, "Project Scope") or ""
    objectives = _extract_section(brd_text, "Business Objectives") or ""
    budget = _extract_section(brd_text, "Budget Details") or ""
    assumptions = _extract_section(brd_text, "Assumptions") or ""
    constraints = _extract_section(brd_text, "Constraints") or ""
    
    # Extract EPICs from BRD and convert to User Stories
    # CRITICAL: Only use EPICs that are derived from Business Objectives and Scope
    epics_section = _extract_section(brd_text, "Business Requirements") or exec_summary
    br_list = _br_to_list(epics_section) if epics_section else []
    
    # Filter EPICs to exclude budget details and out-of-scope items
    filtered_br_list = []
    if br_list:
        for epic in br_list:
            epic_lower = epic.lower()
            # Exclude budget-related EPICs and out-of-scope items
            if not any(keyword in epic_lower for keyword in [
                'budget', 'cost', 'financial', 'price', 'expense', 'payment processing',
                'out of scope', 'excluded', 'not included', 'future release', 
                'advanced analytics', 'ai/ml', 'artificial intelligence', 'machine learning',
                'third-party marketplace', 'marketplace integrations', 'legacy system',
                'automated trading', 'complex automation', 'migration'
            ]):
                # Additional filtering for specific exclusions
                epic_words = epic_lower.split()
                excluded_phrases = [
                    'out', 'scope', 'excluded', 'future', 'advanced', 'ai', 'ml', 
                    'marketplace', 'trading', 'migration', 'budget', 'cost'
                ]
                
                # Only include if not predominantly excluded terms
                excluded_word_count = sum(1 for word in epic_words if word in excluded_phrases)
                total_words = len(epic_words)
                
                if total_words == 0 or excluded_word_count / total_words < 0.5:
                    # Expand abbreviations for clarity
                    epic_expanded = _expand_common_abbreviations(epic)
                    filtered_br_list.append(epic_expanded)
    
    br_list = filtered_br_list
    
    # Domain-specific stakeholders
    stakeholder_mapping = {
        "Healthcare": "Patients, Healthcare providers, Medical staff, Administrators, IT Support, Compliance officers",
        "E-commerce": "Shoppers, Registered customers, Customer support, Merchandisers, Operations team, Finance team",
        "Banking & Finance": "Account holders, Bank staff, Loan officers, Compliance team, IT administrators, Auditors",
        "Education": "Students, Teachers, Administrators, Parents, IT Support, Academic staff",
        "Manufacturing": "Production staff, Quality control, Managers, Suppliers, IT Support, Compliance team",
        "Human Resources": "Employees, HR staff, Managers, Payroll team, IT Support, Executives"
    }
    
    stakeholders = stakeholder_mapping.get(detected_domain, "End users, Business users, Administrators, IT Support, Management team")
    
    # Generate User Stories HTML
    user_stories_html = ""
    
    if not br_list or len(br_list) < 3:
        # Default User Stories for any domain
        default_stories = [
            ("User Authentication & Access", "a user", "secure login and access control", "I can safely access the system and my data is protected"),
            ("Data Management", "a business user", "to create, read, update, and delete core business data", "I can manage information efficiently"),
            ("Search & Filter", "a user", "to search and filter information", "I can quickly find what I need"),
            ("Reporting & Analytics", "a manager", "to view reports and analytics", "I can make informed business decisions"),
            ("Notifications & Alerts", "a user", "to receive important notifications", "I stay informed about relevant updates"),
            ("Integration Management", "an administrator", "to manage system integrations", "data flows correctly between systems"),
            ("Security & Compliance", "a compliance officer", "comprehensive audit trails and security controls", "regulatory requirements are met"),
            ("System Configuration", "an administrator", "to configure system settings", "the system operates according to business rules")
        ]
        
        for i, (title, user_type, capability, value) in enumerate(default_stories, start=1):
            fr_code = f"FR-{i:03d}"
            user_stories_html += f"""
            <div style="margin-bottom: 20px; padding: 16px; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb;">
                <h4 style="margin: 0 0 12px 0; color: #1f2937; font-size: 18px;">{fr_code} {title}</h4>
                <p style="margin: 8px 0;"><strong>User Story:</strong> As {user_type}, I need {capability} so that {value}.</p>
                <p style="margin: 8px 0;"><strong>Acceptance Criteria:</strong> 
                    • Feature functions as specified with appropriate validation
                    • User interface is intuitive and responsive
                    • Data integrity is maintained throughout the process
                    • Proper error handling and user feedback is provided
                </p>
                <p style="margin: 8px 0;"><strong>Validation:</strong> Input validation, business rule enforcement, security checks, and error handling as appropriate for the functionality.</p>
            </div>
            """
    else:
        # Generate User Stories from actual EPICs
        for i, epic in enumerate(br_list[:10], start=1):  # Limit to 10 user stories
            fr_code = f"FR-{i:03d}"
            
            # Parse EPIC format (EPIC-XX Name: Description)
            if ":" in epic:
                title_part, desc_part = epic.split(":", 1)
                title = title_part.strip().replace("EPIC-", "").strip("0123456789- ")
                description = desc_part.strip()
            else:
                title = epic[:50] + "..." if len(epic) > 50 else epic
                description = epic
            
            # Generate user story components based on common patterns
            user_type = "a user"
            if any(keyword in title.lower() for keyword in ["admin", "manage", "config"]):
                user_type = "an administrator"
            elif any(keyword in title.lower() for keyword in ["report", "analytic", "dashboard"]):
                user_type = "a manager"
            elif any(keyword in title.lower() for keyword in ["customer", "client", "patient"]):
                user_type = "a customer"
            
            capability = description.lower().strip()
            value = "I can accomplish my business objectives efficiently"
            
            user_stories_html += f"""
            <div style="margin-bottom: 20px; padding: 16px; border: 1px solid #e5e7eb; border-radius: 8px; background: #f9fafb;">
                <h4 style="margin: 0 0 12px 0; color: #1f2937; font-size: 18px;">{fr_code} {title}</h4>
                <p style="margin: 8px 0;"><strong>User Story:</strong> As {user_type}, I need {capability} so that {value}.</p>
                <p style="margin: 8px 0;"><strong>Acceptance Criteria:</strong> 
                    • All functionality described in the EPIC is implemented correctly
                    • User interface follows design standards and is accessible
                    • Performance requirements are met (response time < 3 seconds)
                    • Proper validation and error handling is implemented
                    • Integration with other system components works correctly
                </p>
                <p style="margin: 8px 0;"><strong>Validation:</strong> 
                    • Input validation for all user-entered data
                    • Business rule validation according to domain requirements
                    • Security validation and authorization checks
                    • Data integrity and consistency validation
                </p>
            </div>
            """

    return f"""
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #111827; padding: 24px; max-width: 1200px; line-height: 1.6;">
  <header style="text-align: center; margin-bottom: 32px; border-bottom: 2px solid #e5e7eb; padding-bottom: 16px;">
    <h1 style="color: #1f2937; margin-bottom: 8px; font-size: 28px;">Functional Requirements Document (FRD)</h1>
    <h2 style="color: #6b7280; margin: 0; font-size: 20px; font-weight: normal;">{project} - Version {version}</h2>
    <p style="color: #9ca3af; margin: 8px 0 0 0; font-style: italic;">Domain: {detected_domain.title()}</p>
  </header>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🎯 Scope & Context</h3>
    <p><strong>In scope:</strong> {scope or 'Core business functionality as defined in the BRD EPICs, user interfaces, essential integrations, and compliance requirements.'}</p>
    <p><strong>Out of scope:</strong> Advanced analytics features, third-party marketplace integrations, legacy system migrations beyond data import, and complex automation workflows not specified in EPICs.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">👥 Stakeholders</h3>
    <p>{stakeholders}</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📋 Assumptions and Constraints</h3>
    <p><strong>Assumptions:</strong> {assumptions or 'Required infrastructure and development resources are available; stakeholders provide timely feedback; third-party services are accessible; security requirements are clearly defined.'}</p>
    <p><strong>Constraints:</strong> {constraints or 'Budget and timeline limitations; regulatory compliance requirements; technical infrastructure constraints; dependency on third-party providers.'}</p>
    {f'<p><strong>Budget:</strong> {budget}</p>' if budget else ''}
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">⚡ Non-functional Requirements (NFRs)</h3>
    <ul style="list-style-type: none; padding-left: 0;">
      <li style="margin-bottom: 8px; padding: 8px; background: #f8fafc; border-left: 4px solid #10b981;">• <strong>Security & Privacy:</strong> Data encryption in transit and at rest, role-based access control, audit logging, PII protection.</li>
      <li style="margin-bottom: 8px; padding: 8px; background: #f8fafc; border-left: 4px solid #3b82f6;">• <strong>Performance & Availability:</strong> Response times under 3 seconds, 99.5% availability, scalable architecture supporting expected user load.</li>
      <li style="margin-bottom: 8px; padding: 8px; background: #f8fafc; border-left: 4px solid #f59e0b;">• <strong>Usability & Accessibility:</strong> Intuitive user interface, mobile-responsive design, WCAG 2.1 AA compliance, keyboard navigation support.</li>
      <li style="margin-bottom: 8px; padding: 8px; background: #f8fafc; border-left: 4px solid #ef4444;">• <strong>Reliability & Resilience:</strong> Graceful degradation, automatic error recovery, data backup and disaster recovery capabilities.</li>
      <li style="margin-bottom: 8px; padding: 8px; background: #f8fafc; border-left: 4px solid #8b5cf6;">• <strong>Observability:</strong> Comprehensive logging, monitoring dashboards, alerting on system health and performance metrics.</li>
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🔌 Interfaces and Integrations</h3>
    <p>External APIs and third-party integrations as required by the business EPICs, including authentication services, payment gateways, messaging systems, and data synchronization with existing business systems. All integrations will follow RESTful API standards with proper error handling and retry mechanisms.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📚 Functional Requirements (User Stories with Validation)</h3>
    {user_stories_html}
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">✅ Field-level Validations</h3>
    <ul style="list-style-type: disc; padding-left: 24px;">
      <li><strong>Input Validation:</strong> Required fields, data format validation, length restrictions, special character handling</li>
      <li><strong>Business Rule Validation:</strong> Domain-specific business logic, cross-field validation, workflow state validation</li>
      <li><strong>Security Validation:</strong> Input sanitization, SQL injection prevention, cross-site scripting protection</li>
      <li><strong>Data Integrity:</strong> Referential integrity, data consistency checks, duplicate prevention</li>
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🔄 Workflow Scenarios (High-level)</h3>
    <ul style="list-style-type: disc; padding-left: 24px;">
      <li><strong>Primary Workflow:</strong> User authentication → Main dashboard → Core business process execution → Results/confirmation</li>
      <li><strong>Data Management Workflow:</strong> Access data interface → Search/filter → Create/update/delete operations → Validation → Save/confirmation</li>
      <li><strong>Reporting Workflow:</strong> Navigate to reports → Select parameters → Generate report → View/export results</li>
      <li><strong>Administrative Workflow:</strong> Admin login → System configuration → User management → Audit review → System monitoring</li>
    </ul>
  </section>
</div>
"""


def _br_to_list(text: str) -> List[str]:
    if not text:
        return []
    lines: List[str] = []
    for line in re.split(r"\r?\n|\u2022|\t", text):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'^[0-9\.\)\-]+\s*', '', line)
        lines.append(line)
    if len(lines) == 1 and ("," in lines[0] or ";" in lines[0]):
        parts = re.split(r",|;", lines[0])
        return [p.strip() for p in parts if p.strip()]
    return lines


def _fr_from_br_item(idx: int, item: str) -> Dict[str, str]:
    code = f"FR-{idx:03d}"
    s = item.strip()
    s = re.sub(r'^\W+', '', s)
    if not re.match(r'(?i)the system shall', s):
        if s and s[0].islower():
            s = s[0].upper() + s[1:]
        s = "The system shall " + s.rstrip(".") + "."
    else:
        if not s.endswith("."):
            s = s + "."
    return {"id": code, "text": s}


def _generate_enhanced_fallback_frd(project: str, brd_text: str, version: int) -> str:
    """
    Enhanced fallback FRD generation with better domain detection and structure.
    """
    # Extract sections from BRD
    exec_summary = _extract_section(brd_text, "Executive Summary") or _safe(brd_text).split("\n", 1)[0]
    scope = _extract_section(brd_text, "Project Scope") or ""
    objectives = _extract_section(brd_text, "Business Objectives") or ""
    budget = _extract_section(brd_text, "Budget Details") or ""
    assumptions = _extract_section(brd_text, "Assumptions") or ""
    constraints = _extract_section(brd_text, "Constraints") or ""
    validations = (
        _extract_section(brd_text, "Validations & Acceptance Criteria")
        or _extract_section(brd_text, "Validations")
        or _extract_section(brd_text, "Acceptance Criteria")
    )
    
    # Extract business requirements
    br_items = _extract_section(brd_text, "Business Requirements") or exec_summary
    br_list = _br_to_list(br_items)
    
    # Detect domain based on keywords
    domain_keywords = {
        "healthcare": ["patient", "medical", "health", "hospital", "clinical", "physician", "diagnosis", "treatment", "hipaa", "ehr", "phr"],
        "banking": ["account", "payment", "transaction", "banking", "financial", "credit", "debit", "loan", "interest", "compliance"],
        "ecommerce": ["product", "order", "cart", "checkout", "inventory", "catalog", "shipping", "customer", "purchase"],
        "education": ["student", "course", "grade", "enrollment", "academic", "faculty", "curriculum", "learning"],
        "insurance": ["policy", "claim", "premium", "coverage", "underwriting", "actuarial", "risk assessment"]
    }
    
    detected_domain = "general"
    brd_lower = brd_text.lower()
    max_matches = 0
    
    for domain, keywords in domain_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in brd_lower)
        if matches > max_matches:
            max_matches = matches
            detected_domain = domain
    
    # Domain-specific configurations
    if detected_domain == "healthcare":
        stakeholders = "Patients, Front-desk staff, Clinicians, Billing staff, IT/Compliance, Payers; primary channels: web and desktop in clinic."
        data_model = "Core entities: Patient, Appointment, Provider, Encounter, Medical History Entry, Document, Invoice, Insurance Policy, Claim, Payment; key relationships: Patient–Appointment (1‑M), Invoice–Claim (1‑M), Patient–Insurance Policy (1‑M)."
        interfaces = "EHR: HL7 v2/FHIR (Patient, Encounter, Observation, MedicationStatement, DocumentReference) for demographics, history, and updates; Payer/clearinghouse: X12 270/271 eligibility, 837 claim submit, 835 remittance; payment gateway for card/ACH processing."
        nfrs = [
            "Security and privacy: PHI encrypted at rest and in transit; role-based access; audit logging; HIPAA-aligned retention and breach notification processes.",
            "Performance and availability: Appointment search < 2s p95; patient record open < 3s p95; 99.5% monthly availability; claims submission batch within 15 minutes.",
            "Usability and accessibility: WCAG 2.1 AA for patient-facing screens; form inline validation; keyboard navigation for clinical workflows."
        ]
    elif detected_domain == "banking":
        stakeholders = "Account holders, Branch staff, Relationship managers, Operations team, Compliance officers, IT/Security; primary channels: web, mobile, ATM, branch."
        data_model = "Core entities: Customer, Account, Transaction, Beneficiary, Payment, Statement, Card; key relationships: Customer–Account (1‑M), Account–Transaction (1‑M), Customer–Beneficiary (1‑M)."
        interfaces = "Core banking systems: Account management APIs; Payment rails: NEFT/IMPS/RTGS/UPI; Regulatory reporting: CKYC, AML, CFT systems; Third-party: Credit bureaus, payment gateways."
        nfrs = [
            "Security: Multi-factor authentication, encryption in transit and at rest, fraud detection, regulatory compliance (RBI guidelines).",
            "Performance: Transaction processing < 3s, account balance inquiry < 1s, 99.9% uptime during business hours.",
            "Compliance: PCI DSS for card data, audit trails, transaction monitoring, regulatory reporting capabilities."
        ]
    else:
        stakeholders = "End users, Business users, Operations team, IT/Support, Management; primary channels: web and mobile applications."
        data_model = "Core entities and relationships based on business domain requirements; data integrity and consistency maintained across all modules."
        interfaces = "External APIs, third-party integrations, database connections, and messaging systems as per business requirements."
        nfrs = [
            "Security: Role-based access control, data encryption, secure authentication, audit logging.",
            "Performance: Response times under 3 seconds, 99.5% availability, scalable architecture.",
            "Usability: Intuitive user interface, mobile-responsive design, accessibility compliance."
        ]
    
    # Generate functional requirements HTML
    fr_items_html = ""
    for i, item in enumerate(br_list, start=1):
        fr_code = f"FR-{i:03d}"
        
        # Clean up the requirement text
        original_req = item.strip()
        
        # Ensure we have a proper functional requirement format
        if original_req.startswith("The system shall"):
            description = original_req
            # Extract title from the part after "The system shall"
            title_text = original_req[16:].strip()
        else:
            # If it doesn't start with "The system shall", add it
            description = f"The system shall {original_req}"
            title_text = original_req
        
        # Ensure description ends with a period
        if not description.endswith('.'):
            description += '.'
        
        # Extract a meaningful title from the requirement text
        title_words = title_text.split()[:4]
        title = " ".join(title_words).rstrip(".,;:")
        
        # If title is too short or empty, use a portion of the original requirement
        if len(title) < 5:
            # Use first 30 characters of the original requirement text
            title_text_clean = title_text or original_req
            title = title_text_clean[:30] + "..." if len(title_text_clean) > 30 else title_text_clean
            
        # Ensure title is properly formatted
        if title:
            title = title.title()
        else:
            title = f"Requirement {i}"
            
        fr_items_html += f"""
        <div style="margin-bottom: 16px; border-left: 3px solid #3b82f6; padding-left: 12px;">
            <h4 style="margin: 0 0 8px 0; color: #1f2937;">{fr_code} {title}</h4>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Roles:</strong> Business users, Operations team.</p>
            <p><strong>Acceptance:</strong> Feature functions as specified with proper validation and error handling.</p>
            <p><strong>Traceability:</strong> Links to business objectives and project scope requirements.</p>
        </div>
        """
    
    # Generate validation items
    val_list = _br_to_list(validations)
    val_html = ""
    for i, val in enumerate(val_list, start=1):
        val_text = val.strip()
        if not val_text.startswith("Enforce"):
            val_text = "Enforce " + val_text
        if not val_text.endswith('.'):
            val_text += '.'
        val_html += f"<li><strong>V-{i:03d}:</strong> {val_text}</li>\n"
    
    if not val_html:
        val_html = "<li><strong>V-001:</strong> Enforce data validation and integrity checks.</li><li><strong>V-002:</strong> Enforce proper authentication and authorization.</li>"

    html = f"""
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #111827; padding: 24px; max-width: 1200px; line-height: 1.6;">
  <header style="text-align: center; margin-bottom: 32px; border-bottom: 2px solid #e5e7eb; padding-bottom: 16px;">
    <h1 style="color: #1f2937; margin-bottom: 8px; font-size: 28px;">Functional Requirements Document (FRD)</h1>
    <h2 style="color: #6b7280; margin: 0; font-size: 20px; font-weight: normal;">{project} - Version {version}</h2>
    <p style="color: #9ca3af; margin: 8px 0 0 0; font-style: italic;">Domain: {detected_domain.title()}</p>
  </header>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🎯 Scope and Context</h3>
    <p><strong>In scope:</strong> {scope or 'Core business functionality as defined in the BRD requirements.'}</p>
    <p><strong>Out of scope:</strong> Advanced integrations and third-party services not explicitly mentioned in the BRD.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">👥 Stakeholders</h3>
    <p>{stakeholders}</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📋 Assumptions and Constraints</h3>
    <p><strong>Assumptions:</strong> {assumptions or 'Standard infrastructure available; users have appropriate access rights; existing systems can integrate as required.'}</p>
    <p><strong>Constraints:</strong> {constraints or 'Regulatory compliance requirements; integration capabilities; project timeline and budget constraints.'}</p>
    {f'<p><strong>Budget:</strong> {budget}</p>' if budget else ''}
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">⚡ Non-functional Requirements (NFRs)</h3>
    <ul style="list-style-type: none; padding-left: 0;">
      {''.join(f'<li style="margin-bottom: 8px; padding: 8px; background: #f8fafc; border-left: 4px solid #10b981;">• {nfr}</li>' for nfr in nfrs)}
    </ul>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🗃️ Data Model Highlights</h3>
    <p>{data_model}</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🔗 Interfaces and Integrations</h3>
    <p>{interfaces}</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">⚙️ Functional Requirements</h3>
    {fr_items_html or '<div style="padding: 16px; background: #fef3c7; border: 1px solid #f59e0b; border-radius: 6px;"><p><strong>Note:</strong> No specific functional requirements found in BRD. Please provide detailed business requirements for more comprehensive FRD generation.</p></div>'}
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">✅ Field-level Validations</h3>
    <ol style="padding-left: 20px;">
      {val_html}
    </ol>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🔄 Workflow Scenarios (High-level)</h3>
    <p><strong>Primary Workflows:</strong> User registration → Authentication → Core functionality access → Data processing → Results/Output generation → Audit logging.</p>
    <p><strong>Exception Handling:</strong> Error validation → User notification → Retry mechanisms → Escalation procedures → Recovery processes.</p>
  </section>

  <section style="margin-bottom: 24px;">
    <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📊 Acceptance Criteria Summary</h3>
    <p>All functional requirements must be traceable to business objectives, measurable through specific acceptance criteria, and validated through comprehensive testing scenarios.</p>
  </section>

  <footer style="border-top: 1px solid #e5e7eb; padding-top: 16px; margin-top: 32px;">
    <p style="font-size: 12px; color: #6b7280; margin: 0;">
      Generated by BA Assistant AI Agent • Domain: {detected_domain.title()} • 
      <span style="color: #3b82f6;">Functional Requirements: {len(br_list)}</span> • 
      <span style="color: #10b981;">Validations: {len(val_list) if val_list else 2}</span>
    </p>
  </footer>
</div>
"""
    return html


def generate_frd_html_from_brd(project: str, brd_text: str, version: int) -> str:
    """Generate a comprehensive FRD from BRD using intelligent User Stories with detailed acceptance criteria."""
    
    # Enhanced system prompt for intelligent User Stories-based FRD generation
    system_prompt = """You are a world-class Senior Systems Analyst and Product Owner with deep expertise in Agile methodologies, User Story creation, and business analysis. Your specialty is converting Business Requirements Documents (BRDs) with EPICs into detailed, actionable Functional Requirements Documents (FRDs) using intelligent User Stories.

CRITICAL INSTRUCTIONS:

1. **ANALYZE EPICs DEEPLY**: Extract EPICs ONLY from Business Objectives and Scope sections, filtering out budget details, payment processing, and out-of-scope items. Understand business context, user types, and functional scope within defined boundaries.

2. **CREATE SPECIFIC USER STORIES**: For each VALID EPIC (excluding budget/excluded scope), generate 2-4 detailed User Stories that:
   - Map directly to EPIC functionality (not financial/budget details)
   - Use specific user personas (not generic "user")
   - Define exact capabilities needed within scope
   - Explain clear business value
   - Expand abbreviations for clarity (KYC/AML, e-sign, etc.)

3. **WRITE INTELLIGENT ACCEPTANCE CRITERIA**: Each User Story must have 3-6 specific, testable acceptance criteria that:
   - Are measurable and verifiable
   - Include performance requirements (timing, throughput)
   - Address edge cases and error scenarios within scope
   - Define UI/UX behavior
   - Specify business rules (excluding budget processing)

4. **CREATE DETAILED VALIDATIONS**: Each User Story must have specific validation rules that:
   - Define input validation (formats, lengths, patterns)
   - Specify business rule validation
   - Include security validation requirements
   - Address data integrity rules
   - Define error handling and messages

5. **ENSURE EPIC TRACEABILITY**: Clearly map each User Story back to its source EPIC.

USER STORY FORMAT:
**FR-XXX [Descriptive Title] (EPIC-XX Reference)**

User Story: As a [specific persona], I need [exact capability] so that [specific business value].

Acceptance Criteria:
1. [Specific, measurable criterion with timing/performance]
2. [Edge case or error handling scenario]
3. [UI/UX behavior specification]
4. [Business rule implementation]
5. [Integration or data requirement]

Validation:
1. [Input format/length validation]
2. [Business rule validation]
3. [Security/permission validation]
4. [Data integrity validation]

DOMAIN INTELLIGENCE: Automatically detect the business domain (CRM, E-commerce, Healthcare, Banking, etc.) and apply domain-specific knowledge to create contextually relevant User Stories with industry-appropriate validation rules.

Generate professional HTML with proper headings, formatting, and clear structure."""
    
    user_prompt = f"""
Based on the following Business Requirements Document (BRD), generate a comprehensive Functional Requirements Document (FRD) using intelligent User Stories methodology:

Project: {project}
Version: {version}

BRD Content:
{brd_text}

ANALYSIS REQUIREMENTS:
1. Extract and analyze ONLY EPICs from Business Objectives and Scope sections - ignore budget details, out-of-scope items, and excluded functionality
2. Filter out any EPICs related to budget, cost, financial processing, or items marked as "out of scope" or "excluded"
3. Identify the business domain and user personas
4. For each VALID EPIC, create 2-4 specific User Stories with:
   - Direct functional mapping to EPIC scope (excluding budget/financial details)
   - Specific user personas (Sales Rep, Customer Service Agent, Marketing Manager, etc.)
   - Detailed acceptance criteria (3-6 criteria per story)
   - Comprehensive validation rules (4-5 validation rules per story)
5. Expand common abbreviations (KYC/AML, e-sign, etc.) for clarity

STRUCTURE THE FRD WITH:
1. **Project Overview & Scope**
2. **Stakeholders & User Personas**  
3. **EPIC to User Story Mapping**
4. **Functional Requirements (User Stories)**
5. **Non-Functional Requirements**
6. **Integration Requirements**
7. **Validation Rules Summary**

ENSURE EACH USER STORY:
- Maps clearly to source EPIC (only from objectives and scope, NOT budget/excluded items)
- Uses domain-specific terminology with expanded abbreviations 
- Includes measurable acceptance criteria
- Has detailed validation rules
- Addresses real business scenarios within defined scope
- Excludes budget details, payment processing, and out-of-scope functionality

Make every User Story actionable, testable, and valuable. Generate professional HTML with clear formatting.
"""

    html = _call_openai_chat(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.4,  # Lower temperature for more consistent, professional output
        max_tokens=4000,  # Increased for more detailed content
    )

    if html and "<" in html and "User Story:" in html:
        return html

    # Enhanced fallback for intelligent User Stories-based FRD
    return _generate_enhanced_user_stories_fallback(project, brd_text, version)


def _generate_enhanced_user_stories_fallback(project: str, brd_text: str, version: int) -> str:
    """Generate enhanced fallback FRD with intelligent User Stories and detailed acceptance criteria."""
    
    # Detect domain and extract EPICs from BRD
    domain = detect_domain(brd_text)
    epics = _extract_epics_from_text(brd_text)
    
    # If no EPICs found, create domain-specific ones
    if not epics:
        epics = _get_domain_default_epics(domain)
    
    # Domain-specific user personas
    personas = _get_domain_personas(domain)
    
    frd_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #1a365d; border-bottom: 3px solid #3182ce; padding-bottom: 10px;">
            Functional Requirements Document (FRD)
        </h1>
        
        <div style="background: #f7fafc; padding: 15px; border-left: 4px solid #3182ce; margin: 20px 0;">
            <h2>Project: {project}</h2>
            <p><strong>Version:</strong> {version} | <strong>Domain:</strong> {domain.title()} | <strong>Methodology:</strong> User Stories</p>
        </div>

        <h2 style="color: #2d3748; margin-top: 30px;">1. Stakeholders & User Personas</h2>
        <div style="background: #edf2f7; padding: 15px; border-radius: 5px;">
            {_generate_personas_html(personas)}
        </div>

        <h2 style="color: #2d3748; margin-top: 30px;">2. EPIC to User Story Mapping</h2>
        <div style="background: #e6fffa; padding: 15px; border-radius: 5px;">
            {_generate_epic_mapping_html(epics)}
        </div>

        <h2 style="color: #2d3748; margin-top: 30px;">3. Functional Requirements (User Stories)</h2>
        {_generate_detailed_user_stories_html(epics, personas, domain)}

        <h2 style="color: #2d3748; margin-top: 30px;">4. Non-Functional Requirements</h2>
        {_generate_nfr_html(domain)}

        <h2 style="color: #2d3748; margin-top: 30px;">5. Validation Rules Summary</h2>
        {_generate_validation_summary_html(domain)}
    </div>
    """
    
    return frd_html


def _extract_epics_from_text(text: str) -> List[Dict[str, str]]:
    """Extract EPICs from BRD text with intelligent parsing."""
    epics = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Look for EPIC patterns
        if 'EPIC-' in line.upper():
            # Extract EPIC number and description
            if ':' in line:
                epic_part, desc = line.split(':', 1)
                epic_num = epic_part.strip()
                epics.append({
                    'id': epic_num,
                    'description': desc.strip(),
                    'title': desc.split()[0:3] if desc.strip() else ['Business', 'Capability']
                })
    
    return epics


def _get_domain_default_epics(domain: str) -> List[Dict[str, str]]:
    """Get default EPICs based on detected domain."""
    domain_epics = {
        'crm': [
            {'id': 'EPIC-01', 'title': 'Lead Management', 'description': 'capture, qualify, and convert leads to opportunities'},
            {'id': 'EPIC-02', 'title': 'Opportunity Management', 'description': 'track sales pipeline and forecast revenue'},
            {'id': 'EPIC-03', 'title': 'Contact Management', 'description': 'maintain customer and prospect information'},
            {'id': 'EPIC-04', 'title': 'Activity Tracking', 'description': 'log and track sales activities and communications'},
            {'id': 'EPIC-05', 'title': 'Reporting & Analytics', 'description': 'generate sales reports and performance analytics'},
        ],
        'ecommerce': [
            {'id': 'EPIC-01', 'title': 'Product Catalog', 'description': 'manage product information and inventory'},
            {'id': 'EPIC-02', 'title': 'Shopping Cart', 'description': 'add products to cart and manage selections'},
            {'id': 'EPIC-03', 'title': 'Checkout Process', 'description': 'complete purchase with payment and shipping'},
            {'id': 'EPIC-04', 'title': 'User Accounts', 'description': 'customer registration and profile management'},
            {'id': 'EPIC-05', 'title': 'Order Management', 'description': 'process and track customer orders'},
        ],
        'healthcare': [
            {'id': 'EPIC-01', 'title': 'Patient Management', 'description': 'register and maintain patient records'},
            {'id': 'EPIC-02', 'title': 'Appointment Scheduling', 'description': 'book and manage patient appointments'},
            {'id': 'EPIC-03', 'title': 'Medical Records', 'description': 'store and access patient medical history'},
            {'id': 'EPIC-04', 'title': 'Billing & Insurance', 'description': 'manage patient billing and insurance claims'},
            {'id': 'EPIC-05', 'title': 'Reporting & Compliance', 'description': 'generate reports and ensure compliance'},
        ]
    }
    
    return domain_epics.get(domain.lower(), domain_epics['crm'])


def _get_domain_personas(domain: str) -> List[Dict[str, str]]:
    """Get user personas based on domain."""
    domain_personas = {
        'crm': [
            {'role': 'Sales Representative', 'description': 'Manages leads and opportunities'},
            {'role': 'Sales Manager', 'description': 'Oversees sales team and forecasts'},
            {'role': 'Marketing Manager', 'description': 'Creates campaigns and tracks leads'},
            {'role': 'Customer Service Agent', 'description': 'Handles customer inquiries and issues'},
        ],
        'ecommerce': [
            {'role': 'Customer', 'description': 'Browses and purchases products'},
            {'role': 'Store Administrator', 'description': 'Manages product catalog and orders'},
            {'role': 'Customer Service Rep', 'description': 'Assists customers with orders and returns'},
            {'role': 'Marketing Manager', 'description': 'Creates promotions and campaigns'},
        ],
        'healthcare': [
            {'role': 'Patient', 'description': 'Receives medical care and services'},
            {'role': 'Healthcare Provider', 'description': 'Provides medical care and treatment'},
            {'role': 'Administrative Staff', 'description': 'Manages appointments and billing'},
            {'role': 'System Administrator', 'description': 'Maintains system and user access'},
        ]
    }
    
    return domain_personas.get(domain.lower(), domain_personas['crm'])


def _generate_personas_html(personas: List[Dict[str, str]]) -> str:
    """Generate HTML for user personas."""
    html = "<ul>"
    for persona in personas:
        html += f"<li><strong>{persona['role']}:</strong> {persona['description']}</li>"
    html += "</ul>"
    return html


def _generate_epic_mapping_html(epics: List[Dict[str, str]]) -> str:
    """Generate HTML for EPIC mapping."""
    html = "<ul>"
    for epic in epics:
        title = ' '.join(epic.get('title', ['Business', 'Capability'])[:3]) if isinstance(epic.get('title'), list) else epic.get('title', 'Business Capability')
        html += f"<li><strong>{epic['id']} {title}:</strong> {epic['description']}</li>"
    html += "</ul>"
    return html


def _generate_detailed_user_stories_html(epics: List[Dict[str, str]], personas: List[Dict[str, str]], domain: str) -> str:
    """Generate detailed User Stories with specific acceptance criteria and validations."""
    html = ""
    fr_counter = 1
    
    for epic in epics:
        # Generate 2-3 user stories per EPIC
        epic_stories = _create_epic_user_stories(epic, personas, domain, fr_counter)
        html += epic_stories
        fr_counter += len(epic_stories.count('FR-'))
    
    return html


def _create_epic_user_stories(epic: Dict[str, str], personas: List[Dict[str, str]], domain: str, start_counter: int) -> str:
    """Create detailed user stories for a specific EPIC."""
    epic_id = epic['id']
    epic_desc = epic['description']
    title = ' '.join(epic.get('title', ['Business', 'Capability'])[:3]) if isinstance(epic.get('title'), list) else epic.get('title', 'Business Capability')
    
    # Domain and EPIC-specific story templates
    story_templates = _get_story_templates_for_epic(epic_id, epic_desc, domain)
    
    html = f"""
    <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin: 15px 0; background: #fafafa;">
        <h3 style="color: #2b6cb0; margin-top: 0;">{epic_id} - {title}</h3>
    """
    
    for i, template in enumerate(story_templates[:3]):  # Max 3 stories per EPIC
        fr_num = f"FR-{start_counter + i:03d}"
        persona = template['persona']
        capability = template['capability']
        value = template['value']
        acceptance_criteria = template['acceptance_criteria']
        validations = template['validations']
        
        html += f"""
        <div style="border-left: 4px solid #3182ce; padding-left: 15px; margin: 20px 0;">
            <h4 style="color: #2d3748;">{fr_num} {template['title']} ({epic_id} Reference)</h4>
            
            <p><strong>User Story:</strong> As a {persona}, I need {capability} so that {value}.</p>
            
            <div style="margin: 15px 0;">
                <strong>Acceptance Criteria:</strong>
                <ol>
                    {_format_criteria_list(acceptance_criteria)}
                </ol>
            </div>
            
            <div style="margin: 15px 0;">
                <strong>Validation:</strong>
                <ol>
                    {_format_criteria_list(validations)}
                </ol>
            </div>
        </div>
        """
    
    html += "</div>"
    return html


def _get_story_templates_for_epic(epic_id: str, epic_desc: str, domain: str) -> List[Dict[str, Any]]:
    """Get domain-specific user story templates for an EPIC."""
    
    # CRM domain templates
    if domain.lower() == 'crm':
        if 'lead' in epic_desc.lower():
            return [
                {
                    'title': 'Lead Capture',
                    'persona': 'Marketing Manager',
                    'capability': 'to capture leads from multiple sources (web forms, trade shows, referrals)',
                    'value': 'I can build a qualified pipeline for the sales team',
                    'acceptance_criteria': [
                        'System captures lead information within 2 seconds of form submission',
                        'Duplicate leads are automatically detected and merged based on email address',
                        'Lead source is automatically tracked and recorded',
                        'Lead scoring is applied based on predefined criteria',
                        'Notification is sent to assigned sales rep within 5 minutes'
                    ],
                    'validations': [
                        'Email address must be valid format (name@domain.com)',
                        'Phone number must be 10-15 digits with country code validation',
                        'Company name is required for B2B leads',
                        'Lead source must be from predefined list (Website, Trade Show, Referral, etc.)',
                        'System prevents duplicate entries within 24-hour window'
                    ]
                },
                {
                    'title': 'Lead Qualification',
                    'persona': 'Sales Representative',
                    'capability': 'to qualify leads using BANT criteria (Budget, Authority, Need, Timeline)',
                    'value': 'I can focus my efforts on high-value prospects',
                    'acceptance_criteria': [
                        'BANT qualification form is available with required fields',
                        'Lead status automatically updates based on qualification score',
                        'System suggests next best action based on qualification results',
                        'Manager receives notification for high-value qualified leads',
                        'Lead conversion probability is calculated and displayed'
                    ],
                    'validations': [
                        'Budget range must be selected from predefined options',
                        'Authority level must be specified (Decision Maker, Influencer, User)',
                        'Timeline must be within 12 months for qualified status',
                        'Need assessment score must be minimum 6/10 for qualification',
                        'All BANT fields are required before marking as qualified'
                    ]
                }
            ]
        elif 'opportunity' in epic_desc.lower():
            return [
                {
                    'title': 'Opportunity Creation',
                    'persona': 'Sales Representative',
                    'capability': 'to convert qualified leads into sales opportunities',
                    'value': 'I can track potential revenue and manage the sales process',
                    'acceptance_criteria': [
                        'Opportunity is created with minimum required fields populated',
                        'Opportunity value is automatically calculated based on products/services',
                        'Sales stage is set to initial stage with defined activities',
                        'Probability percentage is assigned based on stage and criteria',
                        'Expected close date is calculated based on average sales cycle'
                    ],
                    'validations': [
                        'Opportunity value must be greater than $0 and less than $10,000,000',
                        'Close date must be within 18 months from creation',
                        'Sales stage must be selected from predefined pipeline stages',
                        'Primary contact must be associated with the opportunity',
                        'Product/service selection is required for value calculation'
                    ]
                }
            ]
        elif 'activity' in epic_desc.lower():
            return [
                {
                    'title': 'Activity Logging',
                    'persona': 'Sales Representative',
                    'capability': 'to log calls, meetings, and emails with prospects and customers',
                    'value': 'I can maintain a complete communication history and follow up effectively',
                    'acceptance_criteria': [
                        'Activity is logged with timestamp and duration automatically captured',
                        'Activity is linked to appropriate contact, lead, or opportunity',
                        'Follow-up tasks are automatically created based on activity outcome',
                        'Manager can view team activity reports in real-time',
                        'Integration with email/calendar systems for automatic logging'
                    ],
                    'validations': [
                        'Activity type must be selected (Call, Email, Meeting, Task)',
                        'Duration must be between 1 minute and 8 hours',
                        'Associated record (Lead/Contact/Opportunity) is required',
                        'Activity notes must be minimum 10 characters for completed activities',
                        'Follow-up date cannot be more than 30 days in the future'
                    ]
                }
            ]
    
    # E-commerce domain templates
    elif domain.lower() == 'ecommerce':
        if 'catalog' in epic_desc.lower() or 'product' in epic_desc.lower():
            return [
                {
                    'title': 'Product Search',
                    'persona': 'Customer',
                    'capability': 'to search for products using keywords, filters, and categories',
                    'value': 'I can quickly find the products I want to purchase',
                    'acceptance_criteria': [
                        'Search results are returned within 2 seconds of query submission',
                        'Results are sorted by relevance with option to sort by price, rating, popularity',
                        'Filters include price range, brand, category, ratings, and availability',
                        'Search suggestions appear after typing 3 characters',
                        'No results page provides alternative suggestions and popular products'
                    ],
                    'validations': [
                        'Search query must be minimum 2 characters and maximum 100 characters',
                        'Special characters are sanitized to prevent injection attacks',
                        'Price range filters must have minimum less than maximum value',
                        'Category filters must be from predefined product categories',
                        'Search terms are logged for analytics (non-PII data only)'
                    ]
                }
            ]
        elif 'cart' in epic_desc.lower():
            return [
                {
                    'title': 'Add to Cart',
                    'persona': 'Customer',
                    'capability': 'to add products to my shopping cart with quantity and options',
                    'value': 'I can collect items I want to purchase before checkout',
                    'acceptance_criteria': [
                        'Product is added to cart within 1 second of clicking Add to Cart',
                        'Cart icon updates with item count and total value',
                        'Product options (size, color, etc.) are captured correctly',
                        'Inventory check prevents adding out-of-stock items',
                        'Cart persists across browser sessions for logged-in users'
                    ],
                    'validations': [
                        'Quantity must be between 1 and maximum stock available',
                        'Product options must be selected before adding to cart',
                        'User must be within cart size limit (50 items maximum)',
                        'Product must be active and available for purchase',
                        'Price is validated against current product pricing'
                    ]
                }
            ]
    
    # Healthcare domain templates  
    elif domain.lower() == 'healthcare':
        if 'patient' in epic_desc.lower():
            return [
                {
                    'title': 'Patient Registration',
                    'persona': 'Administrative Staff',
                    'capability': 'to register new patients with complete demographic and insurance information',
                    'value': 'I can ensure accurate patient records and billing processes',
                    'acceptance_criteria': [
                        'Patient registration form captures all required demographic information',
                        'Insurance verification is performed in real-time when possible',
                        'Duplicate patient check is performed using name, DOB, and SSN',
                        'Patient ID is automatically generated and assigned',
                        'HIPAA consent forms are presented and acknowledgment captured'
                    ],
                    'validations': [
                        'Date of birth must be valid date and patient must be born before today',
                        'Social Security Number must be 9 digits and pass validation algorithm',
                        'Insurance policy number format must match insurer requirements',
                        'Emergency contact phone number must be valid 10-digit US number',
                        'All required fields must be completed before registration is saved'
                    ]
                }
            ]
    
    # Default fallback templates
    return [
        {
            'title': 'Basic Functionality',
            'persona': 'User',
            'capability': f'to perform {epic_desc}',
            'value': 'I can complete my business tasks efficiently',
            'acceptance_criteria': [
                'Feature functions as specified with appropriate validation',
                'User interface is intuitive and responsive',
                'Data integrity is maintained throughout the process',
                'Proper error handling and user feedback is provided',
                'Performance meets established SLA requirements'
            ],
            'validations': [
                'Input validation ensures data quality and security',
                'Business rule enforcement maintains data consistency',
                'Security checks prevent unauthorized access',
                'Error handling provides clear user guidance',
                'Audit trail captures user actions for compliance'
            ]
        }
    ]


def _format_criteria_list(criteria: List[str]) -> str:
    """Format criteria as HTML list items."""
    return ''.join([f"<li>{criterion}</li>" for criterion in criteria])


def _generate_nfr_html(domain: str) -> str:
    """Generate Non-Functional Requirements based on domain."""
    nfrs = {
        'performance': 'System response time < 2 seconds for 95% of transactions',
        'security': 'Role-based access control with data encryption at rest and in transit',
        'availability': '99.9% uptime during business hours with planned maintenance windows',
        'scalability': 'Support up to 10,000 concurrent users with horizontal scaling capability',
        'usability': 'Intuitive interface requiring minimal training for end users'
    }
    
    html = "<div style='background: #f0fff4; padding: 15px; border-radius: 5px;'><ul>"
    for category, requirement in nfrs.items():
        html += f"<li><strong>{category.title()}:</strong> {requirement}</li>"
    html += "</ul></div>"
    return html


def _generate_validation_summary_html(domain: str) -> str:
    """Generate validation rules summary."""
    html = """
    <div style='background: #fffbf0; padding: 15px; border-radius: 5px;'>
        <h4>Input Validation Standards</h4>
        <ul>
            <li><strong>Email Validation:</strong> Must match pattern name@domain.com with TLD validation</li>
            <li><strong>Phone Validation:</strong> 10-15 digits with country code, formatted display</li>
            <li><strong>Date Validation:</strong> Valid date format, business rule constraints (future/past)</li>
            <li><strong>Numeric Validation:</strong> Range validation, decimal precision, currency formatting</li>
            <li><strong>Text Validation:</strong> Length limits, special character handling, XSS prevention</li>
        </ul>
        
        <h4>Business Rule Validation</h4>
        <ul>
            <li><strong>Data Integrity:</strong> Foreign key validation, referential integrity</li>
            <li><strong>Business Logic:</strong> Domain-specific rules and constraints</li>
            <li><strong>Workflow Validation:</strong> State transition rules and prerequisites</li>
            <li><strong>Security Validation:</strong> Permission checks, data access controls</li>
        </ul>
    </div>
    """
    return html
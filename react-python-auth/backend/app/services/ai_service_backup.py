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
  <h2 style="text-align:center;margin-top:2px;">{project} — BRD Version-{version}</h2>
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
    req_text = _merge_requirements(inputs)
    val_text = _safe(inputs.get("validations") or inputs.get("validation") or "")

    system = (
        "You are a senior Business Analyst. Produce an HTML snippet only. Include Executive Summary, "
        "Project Scope, Business Objectives, Budget Details, Business Requirements (numbered 'The system shall'), "
        "Assumptions, Constraints, Validations & Acceptance Criteria, Appendices."
    )
    user_prompt = (
        f"Project: {project}\nVersion: {version}\n\n"
        "Inputs (merged):\n"
        f"{req_text}\n\nValidations:\n{val_text}\n\n"
        "If inputs are brief, expand into sensible BA-style detailed items. Output only HTML."
    )

    html = _call_openai_chat(
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user_prompt}],
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.6,
        max_tokens=1500,
    )

    if html:
        if "<" not in html or "Business Requirements" not in html:
            logger.warning("AI returned unexpected format, using fallback.")
            return _local_fallback(project, inputs, version)
        return html

    return _local_fallback(project, inputs, version)


def _extract_section(text: str, heading: str) -> str:
    pattern = rf"(?im)^\s*{re.escape(heading)}\s*(?:\n|:)\s*(.*?)(?=\n[A-Z][\w &/()\-\.:]{{2,}}(?:\n|:)|\Z)"
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else ""


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
        req_text = item.strip()
        if req_text.startswith("The system shall"):
            req_text = req_text[16:].strip()
        
        # Extract a meaningful title
        title_words = req_text.split()[:4]
        title = " ".join(title_words).rstrip(".,;:")
        if len(title) < 10:
            title = req_text[:30] + "..." if len(req_text) > 30 else req_text
            
        description = f"The system shall {req_text.rstrip('.')}"
        if not description.endswith('.'):
            description += '.'
            
        fr_items_html += f"""
        <div style="margin-bottom: 16px; border-left: 3px solid #3b82f6; padding-left: 12px;">
            <h4 style="margin: 0 0 8px 0; color: #1f2937;">{fr_code} {title.title()}</h4>
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
    <h2 style="color: #6b7280; margin: 0; font-size: 20px; font-weight: normal;">{project} — Version {version}</h2>
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
    """
    Generate a comprehensive FRD from BRD using AI agents.
    This function is domain-agnostic and works for Healthcare, Banking, E-commerce, etc.
    """
    # Enhanced system prompt for better FRD generation
    system_prompt = """You are a senior Business Analyst and Systems Architect with expertise in converting Business Requirements Documents (BRDs) to detailed Functional Requirements Documents (FRDs). 

Your task is to analyze the provided BRD and generate a comprehensive, structured FRD that follows industry standards. The FRD should be domain-agnostic and applicable across various industries (Healthcare, Banking, E-commerce, etc.).

Generate ONLY the HTML content for the FRD with the following structure:
1. Scope and context (in-scope vs out-of-scope)
2. Stakeholders and primary channels
3. Assumptions and constraints  
4. Non-functional requirements (NFRs) - Security, Performance, Usability
5. Data model highlights and key entities
6. Interfaces and integrations
7. Detailed functional requirements (FR-001, FR-002, etc.) with:
   - Description
   - Roles involved
   - Acceptance criteria
   - Traceability back to BRD objectives
8. Field-level validations
9. Workflow scenarios (high-level use cases)
10. Acceptance criteria summary
11. Requirements traceability matrix

For each functional requirement, follow this format:
- FR-XXX [Title]
- Description: Clear explanation of the functionality
- Roles: Who uses this feature  
- Acceptance: Specific, testable criteria
- Traceability: Link back to BRD objectives

Make the FRD comprehensive but practical, with specific examples relevant to the domain identified in the BRD."""

    user_prompt = f"""Convert this BRD into a detailed FRD:

Project: {project}
Version: {version}

BRD Content:
{brd_text}

Requirements:
- Extract all business requirements and convert them to functional requirements
- Identify the domain/industry from the BRD content
- Create domain-appropriate stakeholders, data models, and integrations
- Ensure all functional requirements are numbered (FR-001, FR-002, etc.)
- Include specific acceptance criteria for each requirement
- Generate comprehensive NFRs appropriate for the identified domain
- Create realistic workflow scenarios
- Ensure traceability between FRD items and BRD objectives

Output ONLY the HTML content - no explanations or code blocks."""

    # Try AI generation first
    html_ai = _call_openai_chat(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        max_tokens=4000,  # Increased for more comprehensive output
    )
    
    # Validate AI output
    if html_ai and "<" in html_ai and "FR-" in html_ai and len(html_ai) > 1000:
        return html_ai

    # Enhanced fallback for when AI is not available or returns poor output
    logger.warning("AI generation failed or returned insufficient content, using enhanced fallback.")
    return _generate_enhanced_fallback_frd(project, brd_text, version)
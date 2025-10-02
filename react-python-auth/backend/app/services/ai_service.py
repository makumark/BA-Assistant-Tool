from typing import Dict, Any, List, Optional
import os
import re
import logging

logger = logging.getLogger(__name__)

try:
    import openai
except Exception:
    openai = None

# Import Agentic RAG Service
try:
    from .agentic_rag_service import agentic_rag_service, DocumentType
    AGENTIC_RAG_AVAILABLE = True
    logger.info("🤖 Agentic RAG Service loaded successfully")
except ImportError as e:
    AGENTIC_RAG_AVAILABLE = False
    logger.warning(f"⚠️ Agentic RAG Service not available: {e}")


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


def _detect_domain_from_inputs(inputs: Dict[str, Any]) -> str:
    """Detect business domain from project inputs for enhanced fallback."""
    domain_keywords = {
        "healthcare": ["patient", "medical", "clinical", "health", "hipaa", "ehr", "practice", "clinic", "hospital", "diagnosis"],
        "banking": ["account", "transaction", "payment", "banking", "financial", "loan", "credit", "debit", "branch", "atm"],
        "ecommerce": ["product", "cart", "checkout", "order", "inventory", "catalog", "shipping", "payment", "customer"],
        "marketing": ["campaign", "segmentation", "email", "sms", "analytics", "attribution", "omnichannel", "automation", "content", "engagement"],
        "education": ["student", "course", "learning", "education", "academic", "grade", "enrollment", "curriculum"],
        "insurance": ["policy", "claim", "premium", "coverage", "underwriting", "actuarial", "risk", "benefit", "quote", "bind", "policyholder", "agent", "broker", "reinsurance", "fnol", "settlement", "endorsement", "renewal", "cancellation", "reinstatement"],
        "mutualfund": ["mutual fund", "nav", "portfolio", "investment", "scheme", "units", "sip", "redemption", "dividend", "amc", "fund manager", "expense ratio"],
        "aif": ["alternative investment", "aif", "hedge fund", "private equity", "venture capital", "real estate fund", "commodity fund", "infrastructure fund", "angel fund", "fpi"],
        "finance": ["financial planning", "wealth management", "asset allocation", "risk management", "derivatives", "securities", "capital market", "treasury", "compliance", "audit"],
        "logistics": ["supply chain", "warehouse", "distribution", "freight", "shipping", "delivery", "tracking", "inventory management", "transportation", "courier", "logistics", "fulfillment"],
        "creditcard": ["credit card", "airline", "rewards", "miles", "points", "loyalty program", "co-brand", "frequent flyer", "cashback", "travel benefits", "airline partnership"],
        "payment": ["payment gateway", "digital wallet", "upi", "mobile payment", "payment processing", "merchant", "pos", "payment security", "fintech", "payment rails"]
    }
    
    # Combine all text from inputs
    all_text = ""
    for key, value in inputs.items():
        if isinstance(value, str):
            all_text += f" {value}"
        elif isinstance(value, list):
            all_text += f" {' '.join(str(v) for v in value)}"
    all_text = all_text.lower()
    
    # Count keyword matches
    max_matches = 0
    detected_domain = "general"
    
    for domain, keywords in domain_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in all_text)
        if matches > max_matches:
            max_matches = matches
            detected_domain = domain
    
    return detected_domain


def _generate_domain_specific_scope(domain: str, project: str) -> str:
    """Generate domain-specific project scope."""
    if domain == "marketing":
        return f"In scope: {project} for customer engagement through personalized campaigns, multi-channel communication, behavioral segmentation, and marketing analytics."
    elif domain == "healthcare":
        return f"In scope: {project} for patient management, clinical workflows, secure health information exchange, and compliance with healthcare regulations."
    elif domain == "banking":
        return f"In scope: {project} for secure banking operations, account management, payment processing, and regulatory compliance."
    elif domain == "ecommerce":
        return f"In scope: {project} for online retail operations, product catalog management, order processing, and customer experience optimization."
    elif domain == "education":
        return f"In scope: {project} for academic management, student enrollment, course delivery, and educational progress tracking."
    elif domain == "insurance":
        return f"In scope: {project} for policy management, claims processing, risk assessment, and customer service operations."
    elif domain == "mutualfund":
        return f"In scope: {project} for mutual fund operations, portfolio management, NAV calculations, investor services, and regulatory compliance."
    elif domain == "aif":
        return f"In scope: {project} for alternative investment fund management, investor onboarding, portfolio tracking, and regulatory reporting."
    elif domain == "finance":
        return f"In scope: {project} for financial operations, wealth management, risk assessment, and investment advisory services."
    elif domain == "logistics":
        return f"In scope: {project} for supply chain management, warehouse operations, distribution networks, and delivery tracking systems."
    elif domain == "creditcard":
        return f"In scope: {project} for credit card and airline partnership programs, rewards management, and co-branded loyalty services."
    elif domain == "payment":
        return f"In scope: {project} for payment processing, digital wallet services, merchant operations, and financial transaction management."
    else:
        return f"In scope: {project} for core business functionality, user management, and system integrations."


def _generate_domain_specific_objectives(domain: str) -> List[str]:
    """Generate domain-specific business objectives."""
    if domain == "marketing":
        return [
            "Increase customer engagement through personalized, data-driven campaigns",
            "Improve marketing ROI with advanced analytics and attribution modeling",
            "Automate repetitive marketing tasks to increase operational efficiency",
            "Enable seamless omnichannel customer experiences across all touchpoints"
        ]
    elif domain == "healthcare":
        return [
            "Improve patient care quality through better information access and coordination",
            "Reduce administrative burden on healthcare providers",
            "Ensure compliance with healthcare regulations and privacy requirements",
            "Enhance operational efficiency and reduce costs"
        ]
    elif domain == "banking":
        return [
            "Reduce manual customer support inquiries related to balances and statements",
            "Improve payment straight-through-processing and reduce failed transactions",
            "Enhance security and fraud detection capabilities",
            "Ensure regulatory compliance and audit readiness"
        ]
    elif domain == "ecommerce":
        return [
            "Increase online sales conversion rates and average order value",
            "Improve customer satisfaction through better user experience",
            "Reduce cart abandonment and optimize checkout process",
            "Enable scalable operations for business growth"
        ]
    elif domain == "education":
        return [
            "Improve student learning outcomes and academic engagement",
            "Streamline administrative processes for faculty and staff",
            "Enhance accessibility and flexibility of educational content",
            "Enable data-driven insights for educational improvement"
        ]
    elif domain == "insurance":
        return [
            "Accelerate claims processing and improve customer satisfaction",
            "Enhance risk assessment accuracy and pricing models",
            "Reduce operational costs and improve efficiency",
            "Ensure regulatory compliance and fraud prevention"
        ]
    elif domain == "mutualfund":
        return [
            "Provide transparent and efficient mutual fund investment services",
            "Optimize portfolio performance and risk-adjusted returns",
            "Streamline investor onboarding and KYC processes",
            "Ensure regulatory compliance and timely reporting"
        ]
    elif domain == "aif":
        return [
            "Deliver superior risk-adjusted returns for sophisticated investors",
            "Provide transparent reporting and performance analytics",
            "Ensure compliance with SEBI AIF regulations",
            "Optimize fund operations and investor relations"
        ]
    elif domain == "finance":
        return [
            "Enhance financial planning and wealth management capabilities",
            "Improve risk management and regulatory compliance",
            "Optimize investment strategies and portfolio performance",
            "Deliver comprehensive financial advisory services"
        ]
    elif domain == "logistics":
        return [
            "Optimize supply chain efficiency and reduce operational costs",
            "Improve delivery speed and tracking accuracy",
            "Enhance warehouse management and inventory optimization",
            "Ensure reliable and transparent logistics operations"
        ]
    elif domain == "creditcard":
        return [
            "Maximize customer engagement through rewards and loyalty programs",
            "Strengthen airline partnerships and co-branded offerings",
            "Enhance customer experience with travel benefits and services",
            "Drive card usage and customer retention through targeted incentives"
        ]
    elif domain == "payment":
        return [
            "Provide secure and seamless payment processing solutions",
            "Enable fast and reliable digital payment experiences",
            "Ensure compliance with payment security standards and regulations",
            "Support diverse payment methods and merchant requirements"
        ]
    else:
        return [
            "Deliver secure, reliable and user-friendly services",
            "Improve operational efficiency and reduce manual processes",
            "Enhance user experience and satisfaction",
            "Enable business scalability and growth"
        ]


def _generate_domain_specific_stakeholders(domain: str) -> str:
    """Generate domain-specific stakeholders."""
    if domain == "marketing":
        return "Marketing managers, Campaign managers, Content creators, Data analysts, Email specialists, Marketing operations team, IT/Integration team; primary channels: web, email, mobile, social media, SMS."
    elif domain == "healthcare":
        return "Patients, Front-desk staff, Clinicians, Billing staff, IT/Compliance, Payers; primary channels: web and desktop in clinic."
    elif domain == "banking":
        return "Account holders, Branch staff, Relationship managers, Operations team, Compliance officers, IT/Security; primary channels: web, mobile, ATM, branch."
    elif domain == "ecommerce":
        return "Customers, Store managers, Inventory managers, Customer service team, IT/Support, Management; primary channels: web, mobile, email, phone."
    elif domain == "education":
        return "Students, Teachers, Academic administrators, Parents/Guardians, IT/Support staff, Registrar office; primary channels: web, mobile, email, campus portal."
    elif domain == "insurance":
        return "Policyholders, Insurance agents, Claims adjusters, Underwriters, Actuaries, Customer service team, IT/Compliance; primary channels: web, mobile, phone, agent portal."
    elif domain == "mutualfund":
        return "Investors, Fund managers, Distributors, Relationship managers, Operations team, Compliance officers, Registrar agents; primary channels: web, mobile, distributor portal, customer service."
    elif domain == "aif":
        return "Qualified investors, Fund managers, Investment advisors, Operations team, Compliance officers, Custodians, Auditors; primary channels: investor portal, web, email, dedicated relationship management."
    elif domain == "finance":
        return "Clients, Financial advisors, Portfolio managers, Risk managers, Compliance officers, Operations team, IT/Support; primary channels: web, mobile, advisor portal, client meetings."
    elif domain == "logistics":
        return "Shippers, Carriers, Warehouse staff, Delivery personnel, Supply chain managers, Operations team, Customers; primary channels: web, mobile, tracking portal, warehouse systems."
    elif domain == "creditcard":
        return "Cardholders, Airline partners, Rewards managers, Customer service team, Marketing team, Loyalty program managers, Travel service providers; primary channels: web, mobile, airline portal, customer service."
    elif domain == "payment":
        return "Merchants, Customers, Payment processors, Bank partners, Compliance officers, Technical support, Financial institutions; primary channels: payment gateway, mobile apps, POS systems, web checkout."
    else:
        return "End users, Business users, Operations team, IT/Support, Management; primary channels: web and mobile applications."


def _local_fallback(project: str, inputs: Dict[str, Any], version: int) -> str:
    req_text = _merge_requirements(inputs)
    val_text = _safe(inputs.get("validations") or inputs.get("validation") or "")
    req_items = _split_items(req_text)
    val_items = _split_items(val_text)

    # Detect domain for intelligent content generation
    detected_domain = _detect_domain_from_inputs(inputs)
    print(f"🎯 Detected domain for fallback: {detected_domain}")

    exec_summary = _generate_exec_summary(project, req_text)
    scope = _safe(inputs.get("scope") or "")
    objectives = _derive_objectives(req_text)
    budget = _derive_budget(inputs)
    assumptions = _safe(inputs.get("assumptions") or "Core systems available; test environments mirror production.")
    constraints = _safe(inputs.get("constraints") or "")

    # Generate domain-specific scope and objectives if not provided or generic
    if not scope:
        scope = _generate_domain_specific_scope(detected_domain, project)
    
    # Use domain-specific objectives if none provided or if they're generic banking objectives
    if not objectives or len(objectives) == 0 or any("payment" in obj.lower() or "banking" in obj.lower() for obj in objectives):
        objectives = _generate_domain_specific_objectives(detected_domain)

    brd_list_html = ""
    if req_items:
        for it in req_items:
            sentence = _to_requirement_sentence(it)
            if sentence:
                brd_list_html += f"<li>{sentence}</li>\n"
    else:
        # Generate domain-specific default requirements
        if detected_domain == "marketing":
            brd_list_html = """<li>The system shall provide customer segmentation capabilities based on behavioral and demographic data.</li>
<li>The system shall support multi-channel campaign management across email, SMS, and push notifications.</li>
<li>The system shall enable real-time analytics and attribution reporting for campaign performance.</li>"""
        else:
            brd_list_html = "<li>The system shall implement secure customer authentication and account overview.</li>"

    # Generate domain-specific stakeholders
    stakeholders = _generate_domain_specific_stakeholders(detected_domain)

    val_list_html = ""
    # Check if validation input is meaningful content vs placeholder/test text
    has_meaningful_validations = (val_items and 
                                 not any(placeholder in val_text.lower() for placeholder in [
                                     "should show", "test", "placeholder", "generic", "specific validation", 
                                     "not generic", "example", "sample", "todo", "tbd"
                                 ]))
    
    if has_meaningful_validations:
        for it in val_items:
            txt = it.rstrip(".")
            if not re.match(r'(?i)(enforce|validate|require)', txt):
                txt = "Enforce " + txt
            val_list_html += f"<li>{txt.rstrip('.') }.</li>\n"
    else:
        # Generate domain-specific validation criteria (user input was empty or placeholder text)
        domain_validations = {
            "healthcare": [
                "Enforce mandatory patient demographic fields (name, DOB, SSN)",
                "Validate medical record privacy and HIPAA compliance",
                "Require physician authorization for prescription access",
                "Enforce audit trails for all patient data modifications"
            ],
            "banking": [
                "Enforce strong customer authentication and account verification",
                "Validate transaction limits and fraud detection rules",
                "Require regulatory compliance with banking standards",
                "Enforce real-time balance verification before transactions"
            ],
            "ecommerce": [
                "Enforce product inventory validation before order confirmation",
                "Validate shipping address and payment method accuracy",
                "Require secure checkout process with payment verification",
                "Enforce order tracking and delivery confirmation"
            ],
            "marketing": [
                "Enforce customer consent validation for communication preferences",
                "Validate email address format and deliverability",
                "Require campaign performance tracking and attribution",
                "Enforce A/B testing validation for campaign optimization"
            ],
            "education": [
                "Enforce student enrollment verification and prerequisite checks",
                "Validate course scheduling and instructor availability",
                "Require academic progress tracking and grade validation",
                "Enforce secure access to educational content and records"
            ],
            "insurance": [
                "Enforce policyholder identity verification and eligibility checks",
                "Validate claim documentation and coverage verification",
                "Require risk assessment and underwriting approval",
                "Enforce compliance with insurance regulatory standards"
            ],
            "mutualfund": [
                "Enforce investor KYC verification and risk assessment",
                "Validate NAV calculations and fund performance tracking",
                "Require SIP automation and investment mandate compliance",
                "Enforce regulatory reporting and SEBI compliance"
            ],
            "aif": [
                "Enforce qualified investor verification and accreditation",
                "Validate investment strategies and risk disclosure",
                "Require performance attribution and benchmark tracking",
                "Enforce SEBI AIF regulatory compliance and reporting"
            ],
            "finance": [
                "Enforce client financial assessment and risk profiling",
                "Validate investment recommendations and suitability",
                "Require portfolio rebalancing and performance monitoring",
                "Enforce regulatory compliance and fiduciary standards"
            ],
            "logistics": [
                "Enforce shipment tracking and delivery confirmation",
                "Validate carrier capacity and route optimization",
                "Require warehouse inventory accuracy and location tracking",
                "Enforce delivery time commitments and SLA compliance"
            ],
            "creditcard": [
                "Enforce credit limit verification and spending controls",
                "Validate airline miles earning and redemption accuracy",
                "Require fraud detection and transaction monitoring",
                "Enforce loyalty program rules and benefits tracking"
            ],
            "payment": [
                "Enforce payment security standards and PCI compliance",
                "Validate transaction processing and settlement accuracy",
                "Require multi-factor authentication for high-value transactions",
                "Enforce real-time fraud detection and prevention"
            ]
        }
        
        validations = domain_validations.get(detected_domain, [
            "Enforce strong authentication and integrity of audit logs",
            "Validate data accuracy and completeness",
            "Require proper error handling and user feedback",
            "Enforce security protocols and access controls"
        ])
        
        for validation in validations:
            val_list_html += f"<li>{validation}.</li>\n"

    html = f"""
<div style="font-family:Arial,Helvetica,sans-serif;color:#111827;padding:18px;">
  <h1 style="text-align:center;margin-bottom:6px;">Business Requirement Document (BRD)</h1>
  <h2 style="text-align:center;margin-top:2px;">{project} — BRD Version-{version}</h2>
  <hr/>
  <h3>Executive Summary</h3>
  <p>{exec_summary}</p>

  <h3>Project Scope</h3>
  <p>{scope}</p>

  <h3>Business Objectives</h3>
  <ul>
    {''.join(f'<li>{o}</li>' for o in objectives)}
  </ul>

  <h3>👥 Stakeholders</h3>
  <p>{stakeholders}</p>

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

  <hr/><p style="font-size:11px;color:#6b7280;">Generated by BA Assistant Tool (enhanced fallback)</p>
</div>
"""
    return html


def _use_openai_legacy() -> bool:
    # Check OpenAI version - if >= 1.0.0, use new client
    try:
        import openai
        version = getattr(openai, "__version__", "0.0.0")
        major_version = int(version.split(".")[0])
        return major_version < 1
    except:
        # If can't determine version, try new format first
        return False


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
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not (openai and api_key):
        print("❌ OpenAI/Perplexity not available or no API key")
        return None
    
    print(f"🔧 Using API key: {api_key[:15]}...{api_key[-10:]}")
    
    # Check if this is a Perplexity API key
    is_perplexity = api_key.startswith("pplx-")
    
    if is_perplexity:
        print("📞 Using Perplexity API")
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.perplexity.ai"
            )
            perplexity_model = model or "sonar-small"
            print(f"🔧 Calling Perplexity with model: {perplexity_model}")
            
            completion = client.chat.completions.create(
                model=perplexity_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            content = completion.choices[0].message.content
            return _strip_code_fences(content.strip()) if content else None
            
        except Exception as e:
            print(f"❌ Perplexity API exception: {e}")
            return None
    else:
        # Original OpenAI logic
        use_legacy = _use_openai_legacy()
        print(f"🔧 OpenAI version check: use_legacy={use_legacy}")
        
        try:
            if use_legacy:
                print("📞 Using legacy OpenAI API")
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
                print("📞 Using new OpenAI client")
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    print(f"🔧 Calling OpenAI with model: {model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")
                    resp = client.chat.completions.create(
                        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    content = resp.choices[0].message.content
                    return _strip_code_fences(content.strip()) if content else None
                except Exception as new_e:
                    print(f"❌ New OpenAI client exception: {new_e}")
                    return None
        except Exception as e:
            print(f"❌ OpenAI API exception: {e}")
            return None


def generate_brd_html(project: str, inputs: Dict[str, Any], version: int) -> str:
    """
    Generate BRD using domain-agnostic methodology or Agentic RAG if available.
    
    This function prioritizes the domain-agnostic BRD generator which follows
    a standardized structure with proper sections (Scope, Objectives, EPICs, KPIs, Risks)
    and traceability IDs (OBJ-#, EPIC-<area>-#, KPI-#, RISK-#).
    """
    logger.info(f"🚀 Starting BRD generation for project: {project}")
    
    # Check if domain-agnostic generation is requested or should be used by default
    # Use domain-agnostic generator as the primary method
    try:
        from .ai_service_domain_agnostic import generate_domain_agnostic_brd_html
        logger.info("📋 Using domain-agnostic BRD generator")
        return generate_domain_agnostic_brd_html(project, inputs, version)
    except Exception as e:
        logger.warning(f"⚠️ Domain-agnostic generator error: {e}, falling back to traditional method")
    
    # Try Agentic RAG as fallback if available
    if AGENTIC_RAG_AVAILABLE:
        try:
            logger.info("🤖 Using Agentic Adaptive RAG for BRD generation")
            result = agentic_rag_service.generate_document(
                project=project,
                inputs=inputs,
                doc_type=DocumentType.BRD,
                version=version
            )
            
            if result["success"]:
                logger.info(f"✅ Agentic RAG BRD generation successful")
                logger.info(f"📊 Domain detected: {result['metadata']['domain']}")
                logger.info(f"🎯 Quality score: {result['metadata']['quality_metrics']['overall_score']:.2f}")
                
                # Add metadata footer to content
                metadata_footer = _create_metadata_footer(result["metadata"])
                return result["content"] + metadata_footer
            else:
                logger.warning("❌ Agentic RAG generation failed, falling back to traditional method")
        except Exception as e:
            logger.error(f"❌ Agentic RAG error: {e}, falling back to traditional method")
    else:
        logger.info("📝 Using traditional AI/fallback method (Agentic RAG not available)")
    
    # Traditional method fallback
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

    print(f"🔍 AI response check - html exists: {bool(html)}")
    if html:
        print(f"🔍 HTML content preview: {html[:200]}...")
        has_html = "<" in html
        has_br = "Business Requirements" in html
        print(f"🔍 Contains HTML tags: {has_html}")
        print(f"🔍 Contains 'Business Requirements': {has_br}")
        
        if not has_html or not has_br:
            print("❌ AI returned unexpected format, using fallback.")
            return _local_fallback(project, inputs, version)
        print("✅ AI response format is valid, using AI content")
        return html

    print("❌ No AI response, using fallback")
    return _local_fallback(project, inputs, version)


def _create_metadata_footer(metadata: Dict[str, Any]) -> str:
    """Create metadata footer for Agentic RAG generated content"""
    quality_score = metadata.get("quality_metrics", {}).get("overall_score", 0.0)
    domain = metadata.get("domain", "general")
    generation_time = metadata.get("generation_time", 0.0)
    
    quality_color = "#10b981" if quality_score >= 0.8 else "#f59e0b" if quality_score >= 0.6 else "#ef4444"
    
    return f"""
    <div style="margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 10px; border: 1px solid #cbd5e1;">
        <h4 style="color: #1e40af; margin: 0 0 15px 0; font-size: 16px;">🤖 Agentic Adaptive RAG Generation Report</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
            <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #3b82f6;">
                <div style="font-size: 12px; color: #6b7280; font-weight: 500;">DOMAIN DETECTED</div>
                <div style="font-size: 14px; color: #1f2937; font-weight: 600;">{domain.title()}</div>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid {quality_color};">
                <div style="font-size: 12px; color: #6b7280; font-weight: 500;">QUALITY SCORE</div>
                <div style="font-size: 14px; color: #1f2937; font-weight: 600;">{quality_score:.1%}</div>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #10b981;">
                <div style="font-size: 12px; color: #6b7280; font-weight: 500;">GENERATION TIME</div>
                <div style="font-size: 14px; color: #1f2937; font-weight: 600;">{generation_time:.1f}s</div>
            </div>
            <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #8b5cf6;">
                <div style="font-size: 12px; color: #6b7280; font-weight: 500;">ENHANCEMENT LEVEL</div>
                <div style="font-size: 14px; color: #1f2937; font-weight: 600;">{metadata.get('generation_strategy', {}).get('enhancement', 'Standard')}</div>
            </div>
        </div>
        
        <div style="background: white; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <div style="font-size: 12px; color: #6b7280; font-weight: 500; margin-bottom: 8px;">QUALITY RECOMMENDATIONS</div>
            <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #374151;">
                {chr(10).join([f'<li style="margin-bottom: 4px;">{rec}</li>' for rec in metadata.get('quality_metrics', {}).get('recommendations', ['Document generated successfully'])])}
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid #e2e8f0;">
            <span style="font-size: 11px; color: #9ca3af;">
                Powered by Intelligent Agentic Adaptive RAG • 
                Knowledge-Enhanced Document Generation • 
                Generated at {metadata.get('generation_time', 0.0):.2f}s
            </span>
        </div>
    </div>
    """


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
        
        # Filter out non-functional items (budget, exclusions, assumptions)
        line_lower = line.lower()
        exclude_patterns = [
            "₹", "lakh", "budget", "estimated", "covering", "cost", "price", "$", "€", "£",
            "excluded", "out of scope", "not included", "won't include", "will not include",
            "assumption", "constraint", "phased", "mvp", "growth", "launch",
            "apis", "policies are approved", "domains", "headers", "warmed", "registered",
            "environments", "sso", "cicd", "governance", "retention", "defined"
        ]
        
        # Skip lines that contain exclusion patterns
        if any(pattern in line_lower for pattern in exclude_patterns):
            continue
            
        # Skip lines that are too short to be meaningful requirements
        if len(line.strip()) < 10:
            continue
            
        lines.append(line)
        
    if len(lines) == 1 and ("," in lines[0] or ";" in lines[0]):
        parts = re.split(r",|;", lines[0])
        filtered_parts = []
        for p in parts:
            p = p.strip()
            if p and len(p) > 10:
                # Additional filtering for comma-separated items
                p_lower = p.lower()
                if not any(pattern in p_lower for pattern in ["₹", "lakh", "budget", "excluded", "assumption"]):
                    filtered_parts.append(p)
        return filtered_parts
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
        "marketing": ["campaign", "segmentation", "email", "sms", "push", "analytics", "attribution", "lead", "audience", "omnichannel", "journey", "automation", "personalization", "content", "experiments", "a/b", "martech", "marketing"],
        "education": ["student", "course", "grade", "enrollment", "academic", "faculty", "curriculum", "learning"],
        "insurance": ["policy", "claim", "premium", "coverage", "underwriting", "actuarial", "risk assessment"],
        "crm": ["sales", "leads", "contacts", "opportunities", "pipeline", "customers", "prospects", "deals"]
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
    elif detected_domain == "marketing":
        stakeholders = "Marketing managers, Campaign managers, Content creators, Data analysts, Email specialists, Marketing operations team, IT/Integration team; primary channels: web, email, mobile, social media, SMS."
        data_model = "Core entities: Customer, Segment, Campaign, Journey, Message, Channel, Asset, Experiment, Attribution; key relationships: Customer–Segment (M‑M), Campaign–Message (1‑M), Customer–Journey (M‑M), Campaign–Experiment (1‑M)."
        interfaces = "CRM systems: Customer data and lead management; Email/SMS providers: SendGrid, Mailgun, Twilio; Analytics: Google Analytics, Adobe Analytics; Social platforms: Facebook, LinkedIn APIs; CDP: Customer data platform integration."
        nfrs = [
            "Performance: Email delivery < 5 minutes, segmentation queries < 10s, campaign launch < 2 minutes, analytics refresh < 30 seconds.",
            "Deliverability: Email inbox rate > 95%, SMS delivery rate > 98%, unsubscribe processing < 1 hour.",
            "Compliance: GDPR/CCPA consent management, CAN-SPAM compliance, data retention policies, suppression list management."
        ]
    elif detected_domain == "insurance":
        stakeholders = "Policyholders, Insurance agents, Underwriters, Claims adjusters, Actuaries, Compliance officers, Brokers, Reinsurers; primary channels: agent portals, customer self-service web/mobile, call centers."
        data_model = "Core entities: Policy, Policyholder, Agent, Claim, Premium, Coverage, Risk Assessment, Underwriting Decision, Payment; key relationships: Policyholder–Policy (1‑M), Policy–Claim (1‑M), Policy–Premium (1‑M), Agent–Policy (M‑M)."
        interfaces = "Rating engines: Actuarial calculation systems; Payment gateways: Credit card, bank transfer, ACH processing; Regulatory reporting: NAIC, state insurance department systems; Reinsurance platforms: Treaty management; Third-party data: Credit bureaus, MVR, CLUE reports."
        nfrs = [
            "Regulatory compliance: State insurance regulations, solvency requirements, data retention mandates, audit trail requirements.",
            "Performance: Quote generation < 30 seconds, policy issuance < 5 minutes, claims processing SLA compliance, premium calculation accuracy 99.99%.",
            "Security: PII protection, fraud detection, secure payment processing, role-based access to sensitive data."
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
        
        # Generate intelligent acceptance criteria and validation rules
        acceptance_criteria = _generate_intelligent_acceptance_criteria(detected_domain, req_text, brd_text)
        validation_rules = _generate_intelligent_validation_rules(detected_domain, req_text, brd_text)
            
        fr_items_html += f"""
        <div style="margin-bottom: 20px; border-left: 4px solid #3b82f6; padding-left: 15px; background: #f8fafc; padding: 15px; border-radius: 5px;">
            <h4 style="margin: 0 0 10px 0; color: #1f2937;">{fr_code} {title.title()}</h4>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Roles:</strong> Business users, Operations team, System administrators.</p>
            
            <div style="margin: 12px 0;">
                <h5 style="color: #2d3748; margin-bottom: 6px;">Acceptance Criteria:</h5>
                <ol style="color: #4a5568; line-height: 1.6; margin: 0; padding-left: 20px;">
                    {acceptance_criteria}
                </ol>
            </div>
            
            <div style="margin: 12px 0;">
                <h5 style="color: #2d3748; margin-bottom: 6px;">Validation Rules:</h5>
                <ol style="color: #4a5568; line-height: 1.6; margin: 0; padding-left: 20px;">
                    {validation_rules}
                </ol>
            </div>
            
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
        # Generate domain-specific field-level validations
        if detected_domain == "marketing":
            val_html = """
            <li><strong>V-001:</strong> Enforce customer consent validation for all communication preferences.</li>
            <li><strong>V-002:</strong> Validate email address format and deliverability standards.</li>
            <li><strong>V-003:</strong> Implement campaign performance tracking and attribution models.</li>
            <li><strong>V-004:</strong> Enforce A/B testing validation for statistical significance.</li>
            <li><strong>V-005:</strong> Validate lead scoring and segmentation accuracy.</li>
            <li><strong>V-006:</strong> Ensure GDPR compliance for customer data processing.</li>
            """
        elif detected_domain == "healthcare":
            val_html = """
            <li><strong>V-001:</strong> Enforce HIPAA compliance for patient data protection.</li>
            <li><strong>V-002:</strong> Validate medical record access permissions and audit trails.</li>
            <li><strong>V-003:</strong> Implement patient consent verification for all procedures.</li>
            <li><strong>V-004:</strong> Enforce clinical data validation and standardization.</li>
            """
        elif detected_domain == "banking":
            val_html = """
            <li><strong>V-001:</strong> Enforce strong customer authentication and verification.</li>
            <li><strong>V-002:</strong> Validate transaction limits and fraud detection rules.</li>
            <li><strong>V-003:</strong> Implement regulatory compliance checks and reporting.</li>
            <li><strong>V-004:</strong> Enforce real-time balance verification before transactions.</li>
            """
        else:
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
    Generate a comprehensive FRD from BRD using Agentic Adaptive RAG or fallback method.
    """
    logger.info(f"🚀 Starting FRD generation from BRD for project: {project}")
    
    # Try Agentic RAG first if available
    if AGENTIC_RAG_AVAILABLE:
        try:
            logger.info("🤖 Using Agentic Adaptive RAG for FRD generation")
            
            # Convert BRD text to inputs format for RAG processing
            frd_inputs = {
                "brd_content": brd_text,
                "project": project,
                "version": version,
                "document_type": "FRD",
                "source": "BRD_conversion"
            }
            
            result = agentic_rag_service.generate_document(
                project=project,
                inputs=frd_inputs,
                doc_type=DocumentType.FRD,
                version=version
            )
            
            if result["success"]:
                logger.info(f"✅ Agentic RAG FRD generation successful")
                logger.info(f"📊 Domain detected: {result['metadata']['domain']}")
                logger.info(f"🎯 Quality score: {result['metadata']['quality_metrics']['overall_score']:.2f}")
                
                # Add metadata footer to content
                metadata_footer = _create_metadata_footer(result["metadata"])
                return result["content"] + metadata_footer
            else:
                logger.warning("❌ Agentic RAG FRD generation failed, falling back to traditional method")
        except Exception as e:
            logger.error(f"❌ Agentic RAG FRD error: {e}, falling back to traditional method")
    else:
        logger.info("📝 Using traditional AI/fallback method for FRD (Agentic RAG not available)")
    
    # Traditional method fallback
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


def _generate_intelligent_acceptance_criteria(domain: str, requirement: str, context: str) -> str:
    """Generate intelligent, domain-specific acceptance criteria."""
    
    req_lower = requirement.lower()
    context_lower = context.lower()
    
    # Marketing automation specific criteria
    if domain == "marketing":
        if any(keyword in req_lower for keyword in ["segmentation", "audience", "lists"]):
            return """
            <li>Audience segments must update in real-time based on customer behavior and traits</li>
            <li>Segmentation criteria must support demographic, behavioral, and transaction-based filters</li>
            <li>List building must complete within 5 minutes for segments up to 1 million users</li>
            <li>Segment overlap analysis must show percentage overlaps between different audiences</li>
            <li>Dynamic segments must automatically update as customer data changes</li>
            """
        elif any(keyword in req_lower for keyword in ["campaign", "journey", "automation"]):
            return """
            <li>Campaign setup must support drag-and-drop visual builder with intuitive interface</li>
            <li>Journey triggers must activate within 2 minutes of qualifying customer action</li>
            <li>Branch logic must support complex conditional rules (AND/OR operators)</li>
            <li>Time delays must support minutes, hours, days, and specific date/time scheduling</li>
            <li>Campaign performance metrics must update in real-time during execution</li>
            """
        elif any(keyword in req_lower for keyword in ["email", "sms", "push", "channels"]):
            return """
            <li>Email deliverability must maintain >95% inbox placement rate</li>
            <li>SMS delivery must complete within 30 seconds globally</li>
            <li>Push notifications must support both iOS and Android with rich media</li>
            <li>Message personalization must support dynamic content insertion</li>
            <li>Channel preferences must be respected per customer consent settings</li>
            """
        elif any(keyword in req_lower for keyword in ["content", "asset", "template"]):
            return """
            <li>Asset library must support images, videos, documents with version control</li>
            <li>Template editor must provide WYSIWYG interface with mobile preview</li>
            <li>Approval workflow must support multi-stage review process</li>
            <li>Content localization must support multiple languages and regions</li>
            <li>Brand compliance checks must validate logo, color, and font usage</li>
            """
        elif any(keyword in req_lower for keyword in ["experiments", "a/b", "test"]):
            return """
            <li>A/B tests must support statistical significance calculation at 95% confidence</li>
            <li>Test variations must be randomly distributed across target audience</li>
            <li>Holdout groups must be configurable from 5% to 50% of total audience</li>
            <li>Lift measurement must show performance improvement vs control group</li>
            <li>Test results must be available within 24 hours of campaign completion</li>
            """
        elif any(keyword in req_lower for keyword in ["analytics", "attribution", "funnel"]):
            return """
            <li>Attribution reporting must track customer journey across all touchpoints</li>
            <li>Funnel analysis must show conversion rates at each stage</li>
            <li>Cohort retention must track customer behavior over time periods</li>
            <li>Data exports must support CSV, Excel, and API integration with BI tools</li>
            <li>Real-time dashboards must update campaign metrics every 15 minutes</li>
            """
        elif any(keyword in req_lower for keyword in ["lead", "prospect", "capture", "qualify"]):
            return """
            <li>Lead capture forms collect all required information</li>
            <li>Lead qualification criteria are applied consistently</li>
            <li>Lead assignment follows defined business rules</li>
            <li>Lead source tracking attributes inquiries to correct channels</li>
            <li>Lead scoring calculations update based on customer interactions</li>
            """
        elif any(keyword in req_lower for keyword in ["opportunity", "pipeline", "forecast", "stage"]):
            return """
            <li>Opportunity stages reflect actual sales process workflow</li>
            <li>Pipeline forecasts include probability weighting calculations</li>
            <li>Stage progression requires completion of mandatory fields</li>
            <li>Win/loss analysis captures reasons for opportunity outcomes</li>
            <li>Revenue forecasting aligns with sales team quotas and targets</li>
            """
        elif any(keyword in req_lower for keyword in ["contact", "account", "customer", "dedupe"]):
            return """
            <li>Contact information maintains data quality and completeness</li>
            <li>Account relationships preserve hierarchical structures</li>
            <li>Customer data synchronization maintains referential integrity</li>
            <li>Data privacy controls comply with GDPR and consent management</li>
            <li>Contact merge operations preserve all historical interaction data</li>
            """
        elif any(keyword in req_lower for keyword in ["activity", "task", "calendar", "meeting"]):
            return """
            <li>Activity logging tracks all customer touchpoints and interactions</li>
            <li>Task management includes assignment, due dates, and priority levels</li>
            <li>Calendar integration prevents scheduling conflicts for sales reps</li>
            <li>Meeting notes and outcomes are captured and linked to opportunities</li>
            <li>SLA compliance tracking ensures timely response to customer inquiries</li>
            """
    
    # E-commerce specific criteria
    elif domain == "ecommerce":
        if any(keyword in req_lower for keyword in ["checkout", "payment", "order"]):
            return """
            <li>Payment processing must complete within 5-10 seconds for optimal user experience</li>
            <li>Credit card and debit card numbers must be exactly 16 digits with valid Luhn algorithm verification</li>
            <li>CVV must be exactly 3 digits for Visa/MasterCard or 4 digits for American Express</li>
            <li>System must display total amount including taxes, shipping, and applicable discounts</li>
            <li>Transaction confirmation page must display within 3 seconds of successful payment</li>
            <li>Payment gateway timeouts must be handled gracefully with retry options</li>
            """
        elif any(keyword in req_lower for keyword in ["product", "catalog", "search"]):
            return """
            <li>Product search results must load within 2 seconds with pagination for >50 results</li>
            <li>Search filters must include price range, category, brand, ratings, and availability</li>
            <li>Product images must be high-resolution with zoom functionality</li>
            <li>Stock levels must be displayed accurately and updated in real-time</li>
            <li>Product reviews and ratings must be displayed with verification status</li>
            """
        elif any(keyword in req_lower for keyword in ["cart", "shopping"]):
            return """
            <li>Cart must update in real-time as items are added, removed, or quantities modified</li>
            <li>Cart persistence for logged-in users across browser sessions</li>
            <li>Inventory validation must prevent ordering out-of-stock items</li>
            <li>Price calculations must include all taxes, discounts, and shipping costs</li>
            <li>Guest checkout option must be available without mandatory registration</li>
            """
    
    # Healthcare specific criteria
    elif domain == "healthcare":
        if any(keyword in req_lower for keyword in ["patient", "registration", "medical record"]):
            return """
            <li>Patient registration must validate all mandatory fields (name, DOB, contact, insurance)</li>
            <li>Real-time insurance eligibility verification must complete within 30 seconds</li>
            <li>HIPAA compliance with encrypted data storage and access logging</li>
            <li>Duplicate patient detection to prevent multiple records for same individual</li>
            <li>Emergency contact information must be captured and validated</li>
            """
        elif any(keyword in req_lower for keyword in ["appointment", "scheduling"]):
            return """
            <li>Real-time provider availability with 15-minute time slot granularity</li>
            <li>Automated appointment confirmations via SMS and email within 2 minutes</li>
            <li>Reminder notifications 24 hours and 2 hours before appointments</li>
            <li>Rescheduling/cancellation allowed up to 2 hours before appointment</li>
            <li>Integration with provider calendars to prevent double-booking</li>
            """
        elif any(keyword in req_lower for keyword in ["medical", "clinical", "diagnosis"]):
            return """
            <li>Medical records access requires proper authentication and authorization</li>
            <li>Complete audit trail for all access and modifications to medical data</li>
            <li>ICD-10 and CPT code compliance for diagnoses and procedures</li>
            <li>Critical alerts and flags prominently displayed for patient safety</li>
            <li>Integration with lab systems for real-time results updates</li>
            """
    
    # Banking specific criteria
    elif domain == "banking":
        if any(keyword in req_lower for keyword in ["authentication", "login", "security"]):
            return """
            <li>Multi-factor authentication completion within 60 seconds</li>
            <li>Account lockout after 3 failed attempts with 30-minute auto-unlock</li>
            <li>Session timeout after 15 minutes of inactivity</li>
            <li>Biometric authentication support on compatible mobile devices</li>
            <li>Suspicious activity detection with immediate alerts</li>
            """
        elif any(keyword in req_lower for keyword in ["transaction", "transfer", "payment"]):
            return """
            <li>Real-time balance updates reflecting all pending and completed transactions</li>
            <li>Transaction history with filters for date range, amount, and type</li>
            <li>Transfer amount validation against available balance and limits</li>
            <li>Beneficiary account verification before processing transfers</li>
            <li>Transaction disputes can be initiated directly from transaction details</li>
            """
        elif any(keyword in req_lower for keyword in ["account", "balance", "statement"]):
            return """
            <li>Account balance display with real-time updates</li>
            <li>Statement generation within 30 seconds for up to 12 months</li>
            <li>Currency formatting with appropriate decimal precision</li>
            <li>Account activity summary with categorized transactions</li>
            <li>Download statements in PDF format with digital signatures</li>
            """
    
    # Insurance specific criteria
    elif domain == "insurance":
        if any(keyword in req_lower for keyword in ["quote", "bind", "proposal", "policy"]):
            return """
            <li>Quote generation must complete within 30 seconds with accurate rating calculations</li>
            <li>KYC verification must validate identity documents and addresses</li>
            <li>Payment processing must support multiple methods (card, bank transfer, check)</li>
            <li>Policy issuance must generate PDF documents with digital signatures</li>
            <li>Proposal forms must auto-save to prevent data loss</li>
            """
        elif any(keyword in req_lower for keyword in ["claims", "fnol", "settlement"]):
            return """
            <li>FNOL (First Notice of Loss) must capture all mandatory claim details</li>
            <li>Claim triage must assign claims to appropriate adjusters based on complexity</li>
            <li>Reserve calculations must follow actuarial guidelines and be auditable</li>
            <li>Investigation workflows must track all evidence and documentation</li>
            <li>Settlement approvals must follow authority limits and approval hierarchy</li>
            """
        elif any(keyword in req_lower for keyword in ["billing", "premium", "payment", "collection"]):
            return """
            <li>Premium invoices must calculate accurate amounts including taxes and fees</li>
            <li>Payment reminders must be sent at 30, 60, and 90-day intervals</li>
            <li>Dunning processes must follow regulatory guidelines for grace periods</li>
            <li>Autopay enrollment must securely store payment method information</li>
            <li>Refund processing must calculate pro-rated amounts accurately</li>
            """
        elif any(keyword in req_lower for keyword in ["underwriting", "risk", "assessment"]):
            return """
            <li>Underwriting rules must evaluate risk factors consistently across applications</li>
            <li>Risk scoring must use approved actuarial models and data sources</li>
            <li>Document collection must verify authenticity and completeness</li>
            <li>Approval workflows must enforce authority limits and escalation rules</li>
            <li>Decline reasons must be documented clearly for regulatory compliance</li>
            """
        elif any(keyword in req_lower for keyword in ["agent", "portal", "commission", "distribution"]):
            return """
            <li>Agent portals must display real-time commission tracking and statements</li>
            <li>Lead tracking must capture source attribution and conversion metrics</li>
            <li>Commission calculations must be accurate and auditable by agents</li>
            <li>Dashboard analytics must provide performance insights and trends</li>
            <li>Document access must be role-based with appropriate security controls</li>
            """
        elif any(keyword in req_lower for keyword in ["compliance", "regulatory", "audit", "report"]):
            return """
            <li>Audit logs must capture all system actions with user identification</li>
            <li>Regulatory reports must be generated accurately and submitted on time</li>
            <li>Bordereaux must reconcile with policy and claims data monthly</li>
            <li>Management information must provide real-time business insights</li>
            <li>Data retention must comply with state insurance department requirements</li>
            """
    
    # Default criteria for unknown domains or generic requirements
    return """
            <li>System response time must be within 3 seconds under normal load</li>
            <li>All user inputs validated with clear error messages for invalid data</li>
            <li>User interface provides intuitive navigation with consistent design</li>
            <li>Data changes are persisted immediately with backup and recovery</li>
            <li>Audit logs maintained for all user actions and system events</li>
            """


def _generate_intelligent_validation_rules(domain: str, requirement: str, context: str) -> str:
    """Generate intelligent, domain-specific validation rules based on user story content."""
    
    req_lower = requirement.lower()
    context_lower = context.lower()
    
    # Combine requirement and context for better analysis
    combined_text = f"{req_lower} {context_lower}"
    
    # Healthcare specific validations
    if domain == "healthcare":
        if any(keyword in combined_text for keyword in ["patient", "profile", "registration"]):
            return """
            <li>Patient name: required field, 2-100 characters, letters and spaces only</li>
            <li>Date of birth: valid date, patient must be living (not future date)</li>
            <li>Insurance information: policy number format validation per carrier</li>
            <li>Contact information: valid phone number and email address formats</li>
            <li>Emergency contact: required, different from patient contact</li>
            """
        elif any(keyword in combined_text for keyword in ["appointment", "scheduling", "schedule"]):
            return """
            <li>Appointment time: within provider availability slots</li>
            <li>Patient conflicts: no overlapping appointments for same patient</li>
            <li>Provider conflicts: no double-booking of provider time slots</li>
            <li>Advance booking: minimum 1 hour, maximum 6 months ahead</li>
            <li>Cancellation window: at least 24 hours before appointment</li>
            """
        elif any(keyword in combined_text for keyword in ["medical", "history", "records", "ehr"]):
            return """
            <li>Medical record access: verify user permissions (doctor/nurse/authorized staff)</li>
            <li>Record updates: require digital signature and timestamp</li>
            <li>History entries: chronological order with clear date/time stamps</li>
            <li>Clinical data: structured format for diagnoses, medications, allergies</li>
            <li>Audit trail: all changes logged with user ID and reason</li>
            """
        elif any(keyword in combined_text for keyword in ["billing", "invoice", "insurance", "claim"]):
            return """
            <li>Insurance eligibility: verify coverage before service delivery</li>
            <li>CPT codes: valid current codes for procedures performed</li>
            <li>Billing amounts: match service provided and insurance allowables</li>
            <li>Claim submission: within insurance filing deadlines</li>
            <li>Patient responsibility: calculated correctly after insurance processing</li>
            """
        elif any(keyword in combined_text for keyword in ["prescription", "medication", "drug"]):
            return """
            <li>Drug interactions: check against patient's current medications</li>
            <li>Dosage calculations: verify against patient weight, age, condition</li>
            <li>Prescriber authorization: verify DEA license and scope of practice</li>
            <li>Pharmacy routing: valid pharmacy selection and contact information</li>
            <li>Allergy checking: cross-reference against patient allergy list</li>
            """
        elif any(keyword in combined_text for keyword in ["consent", "authorization", "hipaa"]):
            return """
            <li>Patient consent: explicit agreement required before treatment</li>
            <li>Authorization forms: signed and dated by patient or legal guardian</li>
            <li>HIPAA compliance: privacy disclosures and acknowledgments complete</li>
            <li>Document retention: stored securely per regulatory requirements</li>
            <li>Access logging: track who accessed patient information when</li>
            """
    
    # Marketing automation specific validations
    elif domain == "marketing":
        if any(keyword in req_lower for keyword in ["segmentation", "audience", "lists"]):
            return """
            <li>Audience size: minimum 100 users, maximum 10 million per segment</li>
            <li>Segmentation criteria: must include at least one demographic or behavioral filter</li>
            <li>List names: 3-50 characters, alphanumeric and spaces only</li>
            <li>Segment refresh frequency: configurable from real-time to daily</li>
            <li>Data retention: segments must respect privacy compliance requirements</li>
            """
        elif any(keyword in req_lower for keyword in ["campaign", "journey", "automation"]):
            return """
            <li>Campaign names: 5-100 characters, must be unique within workspace</li>
            <li>Journey steps: minimum 2, maximum 50 steps per automation</li>
            <li>Trigger conditions: must have valid comparison operators and values</li>
            <li>Time delays: minimum 1 minute, maximum 365 days</li>
            <li>Send time validation: must respect recipient time zones and quiet hours</li>
            """
        elif any(keyword in req_lower for keyword in ["email", "sms", "push", "channels"]):
            return """
            <li>Email addresses: RFC 5322 compliant format validation</li>
            <li>Phone numbers: E.164 international format for SMS delivery</li>
            <li>Subject lines: 1-78 characters for optimal inbox display</li>
            <li>Message content: must include unsubscribe link and sender identification</li>
            <li>Frequency caps: configurable daily/weekly limits per customer</li>
            """
        elif any(keyword in combined_text for keyword in ["lead", "prospect", "qualify", "capture"]):
            return """
            <li>Lead capture forms collect all required contact information</li>
            <li>Lead qualification rules applied before assignment to sales reps</li>
            <li>Lead scoring algorithms validated for accuracy and consistency</li>
            <li>Duplicate lead detection prevents multiple entries for same contact</li>
            <li>Lead source attribution tracked for all inbound inquiries</li>
            """
        elif any(keyword in combined_text for keyword in ["opportunity", "pipeline", "forecast", "stage"]):
            return """
            <li>Opportunity stage progression follows defined sales process workflow</li>
            <li>Pipeline forecast calculations include probability weighting by stage</li>
            <li>Opportunity value must be positive numeric value with currency validation</li>
            <li>Stage transition requires mandatory field completion before advancement</li>
            <li>Win/loss reason selection required for closed opportunities</li>
            """
        elif any(keyword in combined_text for keyword in ["contact", "account", "customer", "dedupe"]):
            return """
            <li>Contact deduplication logic prevents duplicate customer records</li>
            <li>Account hierarchy validation maintains parent-child relationships</li>
            <li>Contact information must include at least one communication method</li>
            <li>Data synchronization maintains referential integrity across systems</li>
            <li>Contact merge operations preserve all historical interaction data</li>
            """
        elif any(keyword in combined_text for keyword in ["activity", "task", "calendar", "meeting"]):
            return """
            <li>Activity logging tracks all customer touchpoints and interactions</li>
            <li>Task assignment requires valid user and due date specification</li>
            <li>Calendar integration prevents double-booking of sales representatives</li>
            <li>Meeting scheduling respects participant time zone preferences</li>
            <li>SLA timer validation ensures response time compliance requirements</li>
            """
        elif any(keyword in combined_text for keyword in ["analytics", "report", "dashboard", "kpi"]):
            return """
            <li>Campaign performance tracking validates attribution models and ROI calculations</li>
            <li>Dashboard data refresh maintains real-time accuracy within defined intervals</li>
            <li>Report generation includes data validation and completeness checks</li>
            <li>KPI calculations follow standardized business rule definitions</li>
            <li>Analytics tracking complies with privacy regulations and consent requirements</li>
            """
        elif any(keyword in combined_text for keyword in ["lead", "prospect", "qualify", "capture"]):
            return """
            <li>Lead capture forms collect all required contact information</li>
            <li>Lead qualification rules applied before assignment to sales reps</li>
            <li>Lead scoring algorithms validated for accuracy and consistency</li>
            <li>Duplicate lead detection prevents multiple entries for same contact</li>
            <li>Lead source attribution tracked for all inbound inquiries</li>
            """
        elif any(keyword in combined_text for keyword in ["opportunity", "pipeline", "forecast", "stage"]):
            return """
            <li>Opportunity stage progression follows defined sales process workflow</li>
            <li>Pipeline forecast calculations include probability weighting by stage</li>
            <li>Opportunity value must be positive numeric value with currency validation</li>
            <li>Stage transition requires mandatory field completion before advancement</li>
            <li>Win/loss reason selection required for closed opportunities</li>
            """
        elif any(keyword in combined_text for keyword in ["contact", "account", "customer", "dedupe"]):
            return """
            <li>Contact deduplication logic prevents duplicate customer records</li>
            <li>Account hierarchy validation maintains parent-child relationships</li>
            <li>Contact information must include at least one communication method</li>
            <li>Data synchronization maintains referential integrity across systems</li>
            <li>Contact merge operations preserve all historical interaction data</li>
            """
        elif any(keyword in combined_text for keyword in ["activity", "task", "calendar", "meeting"]):
            return """
            <li>Activity logging tracks all customer touchpoints and interactions</li>
            <li>Task assignment requires valid user and due date specification</li>
            <li>Calendar integration prevents double-booking of sales representatives</li>
            <li>Meeting scheduling respects participant time zone preferences</li>
            <li>SLA timer validation ensures response time compliance requirements</li>
            """
        elif any(keyword in combined_text for keyword in ["analytics", "report", "dashboard", "kpi"]):
            return """
            <li>Campaign performance tracking validates attribution models and ROI calculations</li>
            <li>Dashboard data refresh maintains real-time accuracy within defined intervals</li>
            <li>Report generation includes data validation and completeness checks</li>
            <li>KPI calculations follow standardized business rule definitions</li>
            <li>Analytics tracking complies with privacy regulations and consent requirements</li>
            """
        elif any(keyword in req_lower for keyword in ["content", "asset", "template"]):
            return """
            <li>Asset file size: images max 5MB, videos max 100MB</li>
            <li>Template names: 3-50 characters, unique within template library</li>
            <li>Image formats: JPEG, PNG, GIF, WebP only</li>
            <li>HTML validation: must be valid HTML5 with inline CSS support</li>
            <li>Link validation: all URLs must be accessible and not blacklisted</li>
            """
        elif any(keyword in req_lower for keyword in ["experiments", "a/b", "test"]):
            return """
            <li>Test variations: minimum 2, maximum 10 variations per experiment</li>
            <li>Sample size: minimum 1000 users for statistical significance</li>
            <li>Test duration: minimum 24 hours, maximum 30 days</li>
            <li>Confidence level: must be 90%, 95%, or 99%</li>
            <li>Success metrics: must have at least one primary conversion goal</li>
            """
        elif any(keyword in req_lower for keyword in ["analytics", "attribution", "funnel"]):
            return """
            <li>Date ranges: maximum 2 years of historical data per query</li>
            <li>Attribution windows: 1-90 days post-click, 1-30 days post-view</li>
            <li>Export limits: maximum 1 million rows per CSV export</li>
            <li>Funnel steps: minimum 2, maximum 20 steps per funnel</li>
            <li>Cohort periods: daily, weekly, or monthly groupings only</li>
            """
    
    # E-commerce specific validations
    elif domain == "ecommerce":
        if any(keyword in req_lower for keyword in ["checkout", "payment", "order"]):
            return """
            <li>Credit card numbers: exactly 16 digits with Luhn algorithm validation</li>
            <li>CVV: exactly 3 digits (Visa/MC) or 4 digits (Amex)</li>
            <li>Expiry date: MM/YY format, not in the past</li>
            <li>Billing address must match payment method address</li>
            <li>Transaction amount: positive value, within daily limits</li>
            <li>Order total must not exceed maximum order value restrictions</li>
            """
        elif any(keyword in req_lower for keyword in ["product", "catalog", "search"]):
            return """
            <li>Search queries: 2-100 characters with XSS protection</li>
            <li>Price range: valid min/max values with min ≤ max constraint</li>
            <li>Product ratings: 1-5 stars with half-star precision</li>
            <li>Category selections from predefined taxonomy only</li>
            <li>Product SKUs must exist in current catalog</li>
            """
        elif any(keyword in req_lower for keyword in ["cart", "inventory"]):
            return """
            <li>Item quantities: positive integers not exceeding inventory</li>
            <li>Product availability validation before cart addition</li>
            <li>Promotional codes: valid, active, applicable to cart contents</li>
            <li>Shipping address: complete with valid postal codes</li>
            <li>Cart total calculations including all taxes and fees</li>
            """
    
    # Healthcare specific validations
    elif domain == "healthcare":
        if any(keyword in req_lower for keyword in ["patient", "registration"]):
            return """
            <li>Patient name: alphabetic characters, spaces, hyphens, apostrophes only</li>
            <li>Date of birth: MM/DD/YYYY format, age 0-150 years</li>
            <li>SSN: 9 digits in XXX-XX-XXXX format (optional)</li>
            <li>Insurance policy: carrier-specific format requirements</li>
            <li>Emergency contact: valid 10-digit US phone number</li>
            <li>Medical allergies: from approved allergy database</li>
            """
        elif any(keyword in req_lower for keyword in ["appointment", "scheduling"]):
            return """
            <li>Appointment dates: future dates within 6 months</li>
            <li>Time slots: align with provider availability and clinic hours</li>
            <li>No conflicting appointments for same patient</li>
            <li>Appointment type must match provider specialization</li>
            <li>Cancellation: minimum 2 hours advance notice required</li>
            """
        elif any(keyword in req_lower for keyword in ["medical", "diagnosis", "treatment"]):
            return """
            <li>Provider credentials: valid license verification required</li>
            <li>ICD-10 codes: from current approved code sets only</li>
            <li>Medication names: FDA-approved drug database validation</li>
            <li>Vital signs: medically reasonable ranges (BP 50-300/30-200)</li>
            <li>Patient consent verification before sensitive data access</li>
            """
    
    # Banking specific validations
    elif domain == "banking":
        if any(keyword in req_lower for keyword in ["authentication", "login"]):
            return """
            <li>Username: 6-20 characters, alphanumeric and underscores only</li>
            <li>Password: 8-50 characters with upper, lower, number, special character</li>
            <li>Account numbers: bank-specific format (10-12 digits typically)</li>
            <li>2FA codes: 6 digits, expire within 5 minutes</li>
            <li>Security questions: minimum 3 character answers</li>
            """
        elif any(keyword in req_lower for keyword in ["transaction", "transfer"]):
            return """
            <li>Transaction amounts: positive numbers, max 2 decimal places</li>
            <li>Account numbers: valid and belong to authenticated user</li>
            <li>Transfer amounts: not exceed available balance + overdraft</li>
            <li>Beneficiary details: verified before processing</li>
            <li>Transaction limits: daily, monthly, per-transaction maximums</li>
            """
        elif any(keyword in req_lower for keyword in ["account", "balance"]):
            return """
            <li>Date ranges: maximum 2 years for single history request</li>
            <li>Account access: proper authorization and ownership verification</li>
            <li>Statement periods: valid month/year combinations</li>
            <li>Currency codes: ISO 4217 standard format</li>
            <li>Balance inquiries: rate limited to prevent abuse</li>
            """
    
    # Insurance specific validations
    elif domain == "insurance":
        if any(keyword in req_lower for keyword in ["quote", "bind", "policy"]):
            return """
            <li>Policy numbers: unique 10-15 alphanumeric identifiers</li>
            <li>Premium amounts: positive numbers with 2 decimal places precision</li>
            <li>Coverage limits: within regulatory and company guidelines</li>
            <li>Effective dates: future dates only, align with payment schedule</li>
            <li>Applicant age: within underwriting age ranges for product type</li>
            """
        elif any(keyword in req_lower for keyword in ["claims", "fnol", "settlement"]):
            return """
            <li>Claim numbers: unique system-generated identifiers</li>
            <li>Loss dates: within policy effective period, not future dates</li>
            <li>Claim amounts: positive values within policy coverage limits</li>
            <li>Adjuster assignments: based on claim type and dollar threshold</li>
            <li>Settlement amounts: require approval per authority matrix</li>
            """
        elif any(keyword in req_lower for keyword in ["billing", "premium", "payment"]):
            return """
            <li>Payment amounts: match invoice totals exactly</li>
            <li>Due dates: calculated per policy billing frequency</li>
            <li>Bank account details: valid routing and account numbers</li>
            <li>Payment methods: credit/debit cards must pass validation</li>
            <li>Refund calculations: pro-rated based on policy terms</li>
            """
        elif any(keyword in req_lower for keyword in ["underwriting", "risk"]):
            return """
            <li>Risk scores: numerical values within approved ranges</li>
            <li>Application data: all required fields completed accurately</li>
            <li>Supporting documents: uploaded in accepted formats (PDF, JPEG)</li>
            <li>Approval decisions: documented with clear rationale</li>
            <li>Rate factors: applied consistently per approved rating rules</li>
            """
        elif any(keyword in req_lower for keyword in ["agent", "commission"]):
            return """
            <li>Agent licenses: current and valid in applicable states</li>
            <li>Commission rates: within approved percentage ranges</li>
            <li>Producer codes: unique identifiers in company system</li>
            <li>Appointment status: active for product lines being sold</li>
            <li>E&O coverage: verified current before policy binding</li>
            """
    
    # Default validations
    return """
            <li>Required fields: all mandatory fields completed before submission</li>
            <li>Data formats: conform to specified patterns (email, phone, dates)</li>
            <li>User permissions: verified before restricted functionality access</li>
            <li>Input lengths: within defined min/max character limits</li>
            <li>XSS protection: all user inputs sanitized and validated</li>
            """


def prioritize_frd_requirements(project: str, frd_html: str, version: int) -> dict:
    """
    AI-powered requirement prioritization using BABOK MoSCoW methodology.
    
    Args:
        project: Project name for domain detection
        frd_html: Complete FRD HTML content with user stories
        version: Version number
        
    Returns:
        dict: Prioritized requirements with MoSCoW categories and justifications
    """
    
    # Extract user stories from FRD
    user_stories = _extract_user_stories_from_frd(frd_html)
    
    # Detect domain for intelligent prioritization
    domain = _detect_domain_from_text(f"{project} {frd_html}")
    
    # Apply AI-powered prioritization
    prioritized_requirements = _apply_moscow_prioritization(user_stories, domain, project)
    
    # Generate dependency analysis
    dependencies = _analyze_requirement_dependencies(prioritized_requirements, domain)
    
    # Create prioritization report
    prioritization_report = _generate_prioritization_report(
        project, prioritized_requirements, dependencies, domain, version
    )
    
    return {
        "project": project,
        "domain": domain,
        "version": version,
        "total_requirements": len(user_stories),
        "moscow_distribution": _calculate_moscow_distribution(prioritized_requirements),
        "prioritized_requirements": prioritized_requirements,
        "dependencies": dependencies,
        "report_html": prioritization_report
    }


def _extract_user_stories_from_frd(frd_html: str) -> list:
    """Extract user stories from FRD HTML content."""
    user_stories = []
    
    # Look for user story patterns in the FRD
    import re
    
    # Pattern 1: Look for "As a [role], I want [goal], so that [benefit]" format
    story_pattern = r'As a ([^,]+), I want ([^,]+?)(?:, so that ([^<\n\r]+?))?(?:\s*</p>|$)'
    stories = re.findall(story_pattern, frd_html, re.IGNORECASE)
    
    for i, (role, goal, benefit) in enumerate(stories):
        user_stories.append({
            "id": f"US-{i+1:03d}",
            "role": role.strip(),
            "goal": goal.strip(),
            "benefit": benefit.strip() if benefit else "",
            "original_text": f"As a {role.strip()}, I want {goal.strip()}" + (f", so that {benefit.strip()}" if benefit else ""),
            "epic": _extract_epic_from_context(frd_html, goal),
            "complexity": _estimate_story_complexity(goal)
        })
    
    # Pattern 2: Extract FR titles and descriptions for better user story conversion
    fr_pattern = r'<h4>([^<]+)</h4>[^<]*<p><strong>Description:</strong>([^<]+)</p>[^<]*<p>As a ([^,]+), I want ([^,]+)(?:, so that ([^\.]+))?</p>'
    fr_matches = re.findall(fr_pattern, frd_html, re.IGNORECASE | re.DOTALL)
    
    for fr_title, description, role, goal, benefit in fr_matches:
        # Only add if not already captured in Pattern 1
        if not any(story["goal"].lower().strip() == goal.lower().strip() for story in user_stories):
            user_stories.append({
                "id": f"US-{len(user_stories)+1:03d}",
                "role": role.strip(),
                "goal": goal.strip(),
                "benefit": benefit.strip() if benefit else "accomplish business objectives efficiently",
                "original_text": f"As a {role.strip()}, I want {goal.strip()}" + (f", so that {benefit.strip()}" if benefit else ""),
                "epic": _extract_epic_from_context(frd_html, goal),
                "complexity": _estimate_story_complexity(goal),
                "functional_requirement": fr_title.strip(),
                "description": description.strip()
            })
    
    # If still no user stories found, create them from EPIC content
    if not user_stories:
        user_stories = _generate_user_stories_from_epics(frd_html)
    
    return user_stories


def _extract_epic_from_context(frd_html: str, content: str) -> str:
    """Extract EPIC information from FRD context."""
    import re
    
    # Look for EPIC patterns
    epic_pattern = r'EPIC-(\d+)[^:]*:([^<\n]+)'
    epics = re.findall(epic_pattern, frd_html, re.IGNORECASE)
    
    # Find the most relevant EPIC for this content
    content_lower = content.lower()
    
    for epic_num, epic_name in epics:
        if any(word in content_lower for word in epic_name.lower().split() if len(word) > 3):
            return f"EPIC-{epic_num}: {epic_name.strip()}"
    
    return "EPIC-01: Core Business Requirements"


def _estimate_story_complexity(goal: str) -> str:
    """Estimate complexity of user story based on content analysis."""
    goal_lower = goal.lower()
    
    # High complexity indicators
    high_complexity_keywords = [
        "integrate", "algorithm", "ai", "machine learning", "complex", "workflow", 
        "encryption", "security", "payment", "billing", "reporting", "analytics"
    ]
    
    # Medium complexity indicators  
    medium_complexity_keywords = [
        "manage", "process", "generate", "validate", "calculate", "schedule",
        "notification", "email", "search", "filter", "dashboard"
    ]
    
    # Low complexity indicators
    low_complexity_keywords = [
        "view", "display", "list", "show", "read", "access", "login", "logout",
        "profile", "basic", "simple"
    ]
    
    if any(keyword in goal_lower for keyword in high_complexity_keywords):
        return "High"
    elif any(keyword in goal_lower for keyword in medium_complexity_keywords):
        return "Medium"
    elif any(keyword in goal_lower for keyword in low_complexity_keywords):
        return "Low"
    else:
        return "Medium"  # Default


def _detect_domain_from_text(text: str) -> str:
    """Detect business domain from text content."""
    text_lower = text.lower()
    
    domain_keywords = {
        "ecommerce": ["product", "cart", "checkout", "order", "inventory", "catalog", "shipping", "customer", "purchase", "payment"],
        "healthcare": ["patient", "medical", "health", "hospital", "clinical", "physician", "diagnosis", "treatment", "hipaa", "ehr"],
        "banking": ["account", "transaction", "payment", "banking", "financial", "credit", "debit", "loan", "interest"],
        "insurance": ["policy", "claim", "premium", "coverage", "underwriting", "actuarial", "risk", "benefit", "quote", "bind"],
        "marketing": ["campaign", "segmentation", "email", "sms", "analytics", "lead", "audience", "automation"],
        "education": ["student", "course", "grade", "enrollment", "academic", "faculty", "curriculum", "learning"],
        "logistics": ["supply chain", "warehouse", "distribution", "freight", "shipping", "delivery", "tracking"]
    }
    
    max_matches = 0
    detected_domain = "general"
    
    for domain, keywords in domain_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        if matches > max_matches:
            max_matches = matches
            detected_domain = domain
    
    return detected_domain


def _apply_moscow_prioritization(user_stories: list, domain: str, project: str) -> list:
    """Apply MoSCoW prioritization using domain-specific intelligence."""
    
    prioritized_stories = []
    
    for story in user_stories:
        # Calculate priority based on multiple factors
        priority_score = _calculate_priority_score(story, domain, user_stories)
        moscow_category = _determine_moscow_category(priority_score, story, domain)
        justification = _generate_priority_justification(story, moscow_category, domain)
        
        prioritized_story = {
            **story,
            "priority_score": priority_score,
            "moscow_category": moscow_category,
            "justification": justification,
            "business_value": _assess_business_value(story, domain),
            "technical_risk": _assess_technical_risk(story),
            "dependencies": _identify_story_dependencies(story, user_stories, domain)
        }
        
        prioritized_stories.append(prioritized_story)
    
    # Sort by priority score (highest first)
    prioritized_stories.sort(key=lambda x: x["priority_score"], reverse=True)
    
    # Assign final priority ranks
    for i, story in enumerate(prioritized_stories):
        story["priority_rank"] = i + 1
    
    return prioritized_stories


def _calculate_priority_score(story: dict, domain: str, all_stories: list) -> int:
    """Calculate comprehensive priority score for a user story."""
    score = 0
    goal_lower = story["goal"].lower()
    role_lower = story["role"].lower()
    
    # Domain-specific priority patterns
    if domain == "ecommerce":
        # E-commerce prioritization logic - authentication gets highest priority
        if any(keyword in goal_lower for keyword in ["login", "authenticate", "register", "account creation", "sign in", "sign up", "user registration"]):
            score += 100  # Foundation - Must Have
        elif any(keyword in goal_lower for keyword in ["search", "browse", "catalog", "product", "find"]):
            score += 90   # Core functionality - Must Have
        elif any(keyword in goal_lower for keyword in ["cart", "add to cart", "shopping", "basket"]):
            score += 85   # Shopping flow - Must Have
        elif any(keyword in goal_lower for keyword in ["checkout", "payment", "pay", "order", "purchase"]):
            score += 80   # Revenue generation - Must Have
        elif any(keyword in goal_lower for keyword in ["profile", "manage", "account settings"]):
            score += 70   # User management - Should Have
        elif any(keyword in goal_lower for keyword in ["wishlist", "favorites", "save", "bookmark"]):
            score += 60   # User experience - Should Have
        elif any(keyword in goal_lower for keyword in ["review", "rating", "comment", "feedback"]):
            score += 50   # Social features - Could Have
        elif any(keyword in goal_lower for keyword in ["recommend", "suggest", "analytics", "ai"]):
            score += 40   # Advanced features - Could Have
    
    elif domain == "healthcare":
        # Healthcare prioritization logic
        if any(keyword in goal_lower for keyword in ["login", "authenticate", "access", "security"]):
            score += 100  # Security foundation - Must Have
        elif any(keyword in goal_lower for keyword in ["patient", "registration", "admit"]):
            score += 95   # Patient management - Must Have
        elif any(keyword in goal_lower for keyword in ["medical", "history", "record", "chart"]):
            score += 90   # Core medical data - Must Have
        elif any(keyword in goal_lower for keyword in ["appointment", "schedule", "booking"]):
            score += 85   # Scheduling - Must Have
        elif any(keyword in goal_lower for keyword in ["prescription", "medication", "drug"]):
            score += 80   # Medication management - Must Have
        elif any(keyword in goal_lower for keyword in ["billing", "insurance", "claim"]):
            score += 75   # Financial operations - Should Have
        elif any(keyword in goal_lower for keyword in ["report", "analytics", "dashboard"]):
            score += 65   # Reporting - Should Have
        elif any(keyword in goal_lower for keyword in ["notification", "alert", "reminder"]):
            score += 55   # User experience - Should Have
    
    elif domain == "banking":
        # Banking prioritization logic
        if any(keyword in goal_lower for keyword in ["login", "authenticate", "security", "access"]):
            score += 100  # Security foundation - Must Have
        elif any(keyword in goal_lower for keyword in ["account", "balance", "view"]):
            score += 95   # Core banking - Must Have
        elif any(keyword in goal_lower for keyword in ["transaction", "transfer", "payment"]):
            score += 90   # Core operations - Must Have
        elif any(keyword in goal_lower for keyword in ["statement", "history", "record"]):
            score += 80   # Account information - Should Have
        elif any(keyword in goal_lower for keyword in ["notification", "alert", "sms"]):
            score += 70   # Communication - Should Have
        elif any(keyword in goal_lower for keyword in ["investment", "portfolio", "advisory"]):
            score += 60   # Advanced services - Could Have
    
    # Role-based adjustments
    if any(role in role_lower for role in ["admin", "administrator", "system"]):
        score += 10  # Admin features get slight boost
    elif any(role in role_lower for role in ["customer", "user", "client"]):
        score += 20  # Customer-facing features get higher priority
    
    # Complexity adjustments
    if story["complexity"] == "Low":
        score += 15  # Easy wins get priority boost
    elif story["complexity"] == "High":
        score -= 10  # Complex features get slight penalty
    
    # Dependency boost - features that others depend on get higher priority
    dependency_count = sum(1 for other_story in all_stories 
                          if any(keyword in other_story["goal"].lower() 
                                for keyword in goal_lower.split() if len(keyword) > 3))
    score += dependency_count * 5
    
    return max(score, 10)  # Minimum score of 10


def _determine_moscow_category(priority_score: int, story: dict, domain: str) -> str:
    """Determine MoSCoW category based on priority score and domain rules."""
    
    # Adjust thresholds based on domain
    if domain in ["healthcare", "banking"]:
        # More strict requirements for critical domains
        must_threshold = 80
        should_threshold = 60
        could_threshold = 40
    else:
        # Standard thresholds for other domains
        must_threshold = 75
        should_threshold = 55
        could_threshold = 35
    
    if priority_score >= must_threshold:
        return "Must Have"
    elif priority_score >= should_threshold:
        return "Should Have"
    elif priority_score >= could_threshold:
        return "Could Have"
    else:
        return "Won't Have (this time)"


def _generate_priority_justification(story: dict, moscow_category: str, domain: str) -> str:
    """Generate justification for the assigned priority."""
    goal_lower = story["goal"].lower()
    
    # Domain-specific justifications
    justifications = {
        "Must Have": {
            "ecommerce": {
                "login": "Foundation requirement - users must authenticate before any personalized features",
                "search": "Core business functionality - users need to find products to make purchases",
                "cart": "Essential for shopping experience - enables product collection and purchase intent",
                "checkout": "Revenue generation capability - directly impacts business success",
                "default": "Critical business requirement that directly enables core functionality"
            },
            "healthcare": {
                "login": "Security foundation - patient data protection requires secure access control",
                "patient": "Core business process - patient management is fundamental to healthcare operations",
                "medical": "Clinical requirement - medical data access is essential for patient care",
                "appointment": "Operational necessity - scheduling is fundamental to healthcare delivery",
                "default": "Essential healthcare requirement for patient safety and operational efficiency"
            },
            "default": "Critical requirement that directly enables core business functionality"
        },
        "Should Have": {
            "default": "Important feature that significantly enhances user experience and business value"
        },
        "Could Have": {
            "default": "Nice-to-have feature that provides additional value but not essential for core operations"
        },
        "Won't Have (this time)": {
            "default": "Future enhancement that can be deferred to later releases without impacting core functionality"
        }
    }
    
    category_justifications = justifications.get(moscow_category, {})
    domain_justifications = category_justifications.get(domain, {})
    
    # If domain_justifications is empty, get default for that category
    if not domain_justifications:
        default_justification = category_justifications.get("default", "Priority assigned based on business value assessment and domain requirements")
        if isinstance(default_justification, str):
            return default_justification
        domain_justifications = default_justification
    
    # Find the most specific justification
    if isinstance(domain_justifications, dict):
        for keyword, justification in domain_justifications.items():
            if keyword != "default" and keyword in goal_lower:
                return justification
        
        # Return default justification for the domain
        return domain_justifications.get("default", "Priority assigned based on business value assessment and domain requirements")
    else:
        return str(domain_justifications)


def _assess_business_value(story: dict, domain: str) -> str:
    """Assess business value of the user story."""
    goal_lower = story["goal"].lower()
    
    # High business value keywords by domain
    high_value_keywords = {
        "ecommerce": ["purchase", "buy", "checkout", "payment", "order", "revenue"],
        "healthcare": ["patient", "medical", "treatment", "diagnosis", "safety"],
        "banking": ["transaction", "payment", "account", "security", "compliance"],
        "insurance": ["claim", "policy", "premium", "coverage", "risk"],
        "default": ["revenue", "customer", "business", "critical", "core"]
    }
    
    keywords = high_value_keywords.get(domain, high_value_keywords["default"])
    
    if any(keyword in goal_lower for keyword in keywords):
        return "High"
    elif any(keyword in goal_lower for keyword in ["manage", "process", "improve", "enhance"]):
        return "Medium"
    else:
        return "Low"


def _assess_technical_risk(story: dict) -> str:
    """Assess technical implementation risk."""
    goal_lower = story["goal"].lower()
    
    high_risk_keywords = ["integrate", "algorithm", "ai", "machine learning", "complex", "encryption", "payment", "security"]
    medium_risk_keywords = ["calculate", "validate", "process", "generate", "workflow", "notification"]
    
    if any(keyword in goal_lower for keyword in high_risk_keywords):
        return "High"
    elif any(keyword in goal_lower for keyword in medium_risk_keywords):
        return "Medium"
    else:
        return "Low"


def _identify_story_dependencies(story: dict, all_stories: list, domain: str) -> list:
    """Identify dependencies between user stories."""
    dependencies = []
    goal_lower = story["goal"].lower()
    
    # Domain-specific dependency rules
    dependency_rules = {
        "ecommerce": {
            "search": ["login", "authentication"],
            "cart": ["search", "product"],
            "checkout": ["cart", "login"],
            "payment": ["checkout", "account"],
            "order": ["payment", "checkout"]
        },
        "healthcare": {
            "appointment": ["patient", "registration"],
            "medical": ["login", "patient"],
            "prescription": ["medical", "patient"],
            "billing": ["patient", "treatment"]
        },
        "banking": {
            "transaction": ["login", "account"],
            "transfer": ["account", "authentication"],
            "statement": ["account", "login"]
        }
    }
    
    rules = dependency_rules.get(domain, {})
    
    for action, prereqs in rules.items():
        if action in goal_lower:
            for prereq in prereqs:
                for other_story in all_stories:
                    if (other_story["id"] != story["id"] and 
                        prereq in other_story["goal"].lower()):
                        dependencies.append({
                            "depends_on": other_story["id"],
                            "dependency_type": "prerequisite",
                            "reason": f"Requires {prereq} functionality to be available"
                        })
    
    return dependencies


def _analyze_requirement_dependencies(prioritized_requirements: list, domain: str) -> dict:
    """Analyze dependencies across all requirements."""
    dependency_graph = {}
    critical_path = []
    
    for req in prioritized_requirements:
        req_id = req["id"]
        dependency_graph[req_id] = {
            "requirement": req,
            "dependencies": req["dependencies"],
            "dependents": []
        }
    
    # Build reverse dependencies (what depends on this requirement)
    for req_id, req_data in dependency_graph.items():
        for dep in req_data["dependencies"]:
            dep_id = dep["depends_on"]
            if dep_id in dependency_graph:
                dependency_graph[dep_id]["dependents"].append({
                    "dependent_id": req_id,
                    "dependency_type": dep["dependency_type"],
                    "reason": dep["reason"]
                })
    
    # Identify critical path (requirements with most dependents)
    critical_requirements = sorted(
        dependency_graph.keys(),
        key=lambda x: len(dependency_graph[x]["dependents"]),
        reverse=True
    )[:5]  # Top 5 most critical
    
    return {
        "dependency_graph": dependency_graph,
        "critical_path": critical_requirements,
        "total_dependencies": sum(len(req["dependencies"]) for req in prioritized_requirements),
        "isolated_requirements": [req_id for req_id, data in dependency_graph.items() 
                                 if not data["dependencies"] and not data["dependents"]]
    }


def _calculate_moscow_distribution(prioritized_requirements: list) -> dict:
    """Calculate distribution of requirements across MoSCoW categories."""
    distribution = {"Must Have": 0, "Should Have": 0, "Could Have": 0, "Won't Have (this time)": 0}
    
    for req in prioritized_requirements:
        category = req["moscow_category"]
        distribution[category] += 1
    
    total = len(prioritized_requirements)
    
    return {
        "counts": distribution,
        "percentages": {category: round((count / total) * 100, 1) if total > 0 else 0 
                      for category, count in distribution.items()},
        "total_requirements": total
    }


def _generate_user_stories_from_epics(frd_html: str) -> list:
    """Generate user stories from EPIC content when none are found."""
    import re
    
    user_stories = []
    
    # Extract EPIC requirements
    epic_pattern = r'Requirements:[^•]*•([^•]+(?:•[^•]+)*)'
    epic_matches = re.findall(epic_pattern, frd_html, re.DOTALL)
    
    for i, epic_content in enumerate(epic_matches):
        # Split by bullet points
        requirements = [req.strip() for req in epic_content.split('•') if req.strip()]
        
        for j, req in enumerate(requirements):
            if len(req) > 10:  # Filter out very short requirements
                user_stories.append({
                    "id": f"US-{len(user_stories)+1:03d}",
                    "role": "User",
                    "goal": f"have {req.lower()}",
                    "benefit": "accomplish business objectives efficiently",
                    "original_text": req.strip(),
                    "epic": f"EPIC-{i+1:02d}",
                    "complexity": _estimate_story_complexity(req)
                })
    
    return user_stories[:20]  # Limit to 20 stories for manageable output


def _generate_prioritization_report(project: str, prioritized_requirements: list, 
                                  dependencies: dict, domain: str, version: int) -> str:
    """Generate comprehensive prioritization report in HTML format."""
    
    moscow_dist = _calculate_moscow_distribution(prioritized_requirements)
    
    html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #111827; padding: 24px; max-width: 1200px; line-height: 1.6;">
      <header style="text-align: center; margin-bottom: 32px; border-bottom: 2px solid #e5e7eb; padding-bottom: 16px;">
        <h1 style="color: #1f2937; margin-bottom: 8px; font-size: 28px;">Requirement Prioritization Report</h1>
        <h2 style="color: #6b7280; margin: 0; font-size: 20px; font-weight: normal;">{project} — Version {version}</h2>
        <p style="color: #9ca3af; margin: 8px 0 0 0; font-style: italic;">Domain: {domain.title()} | MoSCoW Methodology</p>
      </header>

      <section style="margin-bottom: 24px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📊 Executive Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 16px 0;">
          <div style="background: #f8fafc; padding: 16px; border-radius: 8px; border-left: 4px solid #10b981;">
            <h4 style="margin: 0 0 8px 0; color: #065f46;">Total Requirements</h4>
            <p style="margin: 0; font-size: 24px; font-weight: bold; color: #065f46;">{moscow_dist['total_requirements']}</p>
          </div>
          <div style="background: #fef3f2; padding: 16px; border-radius: 8px; border-left: 4px solid #dc2626;">
            <h4 style="margin: 0 0 8px 0; color: #7f1d1d;">Must Have</h4>
            <p style="margin: 0; font-size: 24px; font-weight: bold; color: #7f1d1d;">{moscow_dist['counts']['Must Have']} ({moscow_dist['percentages']['Must Have']}%)</p>
          </div>
          <div style="background: #fff7ed; padding: 16px; border-radius: 8px; border-left: 4px solid #ea580c;">
            <h4 style="margin: 0 0 8px 0; color: #9a3412;">Should Have</h4>
            <p style="margin: 0; font-size: 24px; font-weight: bold; color: #9a3412;">{moscow_dist['counts']['Should Have']} ({moscow_dist['percentages']['Should Have']}%)</p>
          </div>
          <div style="background: #f0f9ff; padding: 16px; border-radius: 8px; border-left: 4px solid #0284c7;">
            <h4 style="margin: 0 0 8px 0; color: #0c4a6e;">Could Have</h4>
            <p style="margin: 0; font-size: 24px; font-weight: bold; color: #0c4a6e;">{moscow_dist['counts']['Could Have']} ({moscow_dist['percentages']['Could Have']}%)</p>
          </div>
        </div>
      </section>

      <section style="margin-bottom: 24px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🎯 Prioritized Requirements</h3>
    """
    
    # Group requirements by MoSCoW category
    moscow_categories = ["Must Have", "Should Have", "Could Have", "Won't Have (this time)"]
    category_colors = {
        "Must Have": "#dc2626",
        "Should Have": "#ea580c", 
        "Could Have": "#0284c7",
        "Won't Have (this time)": "#6b7280"
    }
    
    for category in moscow_categories:
        category_reqs = [req for req in prioritized_requirements if req["moscow_category"] == category]
        if not category_reqs:
            continue
            
        color = category_colors[category]
        html += f"""
        <div style="margin-bottom: 24px;">
          <h4 style="color: {color}; margin-bottom: 16px; font-size: 18px;">🎯 {category} ({len(category_reqs)} requirements)</h4>
        """
        
        for req in category_reqs:
            dependencies_text = ""
            if req["dependencies"]:
                deps = [f"• {dep['depends_on']}: {dep['reason']}" for dep in req["dependencies"]]
                dependencies_text = f"""
                <div style="margin-top: 12px;">
                  <strong>Dependencies:</strong>
                  <ul style="margin: 4px 0 0 20px; padding: 0;">
                    {''.join(f'<li style="margin: 2px 0;">{dep}</li>' for dep in deps)}
                  </ul>
                </div>
                """
            
            html += f"""
            <div style="margin-bottom: 16px; border-left: 4px solid {color}; padding: 16px; background: #f8fafc; border-radius: 5px;">
              <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 8px;">
                <h5 style="margin: 0; color: #1f2937;">#{req['priority_rank']} {req['id']}: {req['role']} Story</h5>
                <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: auto;">
                  Score: {req['priority_score']}
                </span>
              </div>
              <p style="margin: 8px 0; font-weight: 500;">"{req['original_text']}"</p>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 12px 0; font-size: 14px;">
                <div><strong>Business Value:</strong> {req['business_value']}</div>
                <div><strong>Complexity:</strong> {req['complexity']}</div>
                <div><strong>Technical Risk:</strong> {req['technical_risk']}</div>
                <div><strong>EPIC:</strong> {req.get('epic', 'N/A')}</div>
              </div>
              <div style="background: #e5e7eb; padding: 8px; border-radius: 4px; margin-top: 8px;">
                <strong>Justification:</strong> {req['justification']}
              </div>
              {dependencies_text}
            </div>
            """
        
        html += "</div>"
    
    # Add dependency analysis
    html += f"""
      </section>

      <section style="margin-bottom: 24px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">🔗 Dependency Analysis</h3>
        <div style="background: #f8fafc; padding: 16px; border-radius: 8px; margin: 16px 0;">
          <p><strong>Total Dependencies:</strong> {dependencies['total_dependencies']}</p>
          <p><strong>Critical Path Requirements:</strong> {', '.join(dependencies['critical_path'][:3])}{"..." if len(dependencies['critical_path']) > 3 else ""}</p>
          <p><strong>Isolated Requirements:</strong> {len(dependencies['isolated_requirements'])} requirements with no dependencies</p>
        </div>
      </section>

      <section style="margin-bottom: 24px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #3b82f6; padding-bottom: 4px;">📋 Implementation Recommendations</h3>
        <div style="background: #f0f9ff; border-left: 4px solid #0284c7; padding: 16px; margin: 16px 0;">
          <h4 style="margin: 0 0 12px 0; color: #0c4a6e;">Phase 1: Foundation (Must Have)</h4>
          <p>Implement all "Must Have" requirements first, focusing on authentication, core business processes, and fundamental user journeys.</p>
        </div>
        <div style="background: #fff7ed; border-left: 4px solid #ea580c; padding: 16px; margin: 16px 0;">
          <h4 style="margin: 0 0 12px 0; color: #9a3412;">Phase 2: Enhancement (Should Have)</h4>
          <p>Add "Should Have" features that significantly improve user experience and operational efficiency.</p>
        </div>
        <div style="background: #f0fdf4; border-left: 4px solid #16a34a; padding: 16px; margin: 16px 0;">
          <h4 style="margin: 0 0 12px 0; color: #166534;">Phase 3: Optimization (Could Have)</h4>
          <p>Implement "Could Have" features based on user feedback and business priorities from earlier phases.</p>
        </div>
      </section>

      <footer style="border-top: 1px solid #e5e7eb; padding-top: 16px; margin-top: 32px; text-align: center; color: #6b7280; font-size: 14px;">
        <p>Generated by BA Assistant Tool | MoSCoW Prioritization | BABOK Methodology</p>
        <p>Report Generated: {_get_current_timestamp()}</p>
      </footer>
    </div>
    """
    
    return html


def _get_current_timestamp() -> str:
    """Get current timestamp for report generation."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
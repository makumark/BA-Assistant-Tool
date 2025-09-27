import React, { useState, useEffect } from "react";
import WireframeGenerator from "./components/WireframeGenerator.jsx";

export default function App() {
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [msg, setMsg] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [totalProjects, setTotalProjects] = useState(0);
  const [completedProjects, setCompletedProjects] = useState(0);

  const [isCreatingProject, setIsCreatingProject] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [savedProjectName, setSavedProjectName] = useState("");
  const [selectedModule, setSelectedModule] = useState("BRD Generation");
  const [documentGenerator, setDocumentGenerator] = useState("");

  const MODULES = [
    "BRD Generation",
    "FRD Generation",
    "SRS Generation",
    "Impact Analysis",
    "Requirement Priortization",
    "Wireframe Generator",
    "Prototype Generator",
  ];

  const DOC_OPTIONS = [
    "BRD Creation",
    "FRD Creation",
    "SRS Creation",
    "Impact Analysis",
    "Requirement Priortization",
    "Wire Frame Generator",
    "Prototype Generator",
  ];

  const STORAGE_KEY = "ba_projects_v1";
  const [projects, setProjects] = useState(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  });

  const [brdInputs, setBrdInputs] = useState({
    scope: "",
    objectives: "",
    budget: "",
    briefRequirements: "",
    assumptions: "",
    constraints: "",
    validations: "",
  });

  const [frdInputs, setFrdInputs] = useState({
    brdText: "",
  });

  const [brdPreviewHtml, setBrdPreviewHtml] = useState("");
  const [brdPreviewVersion, setBrdPreviewVersion] = useState(null);
  const [brdPreviewVisible, setBrdPreviewVisible] = useState(false);

  const [frdPreviewHtml, setFrdPreviewHtml] = useState("");
  const [frdPreviewVersion, setFrdPreviewVersion] = useState(null);
  const [frdPreviewVisible, setFrdPreviewVisible] = useState(false);
  const [frdLoading, setFrdLoading] = useState(false);

  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSearchProject, setSelectedSearchProject] = useState("");

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));
    const total = Object.keys(projects).length;
    const approvedCount = Object.values(projects).reduce((acc, p) => {
      return acc + (p.documents ? p.documents.filter((d) => d.approved).length : 0);
    }, 0);
    setTotalProjects(total);
    setCompletedProjects(approvedCount);
  }, [projects]);

  const updateBrdInput = (k, v) => setBrdInputs((s) => ({ ...s, [k]: v }));
  const updateFrdInput = (k, v) => setFrdInputs((s) => ({ ...s, [k]: v }));

  const closeBrdPreview = () => {
    setBrdPreviewVisible(false);
    setBrdPreviewHtml("");
    setBrdPreviewVersion(null);
  };

  const closeFrdPreview = () => {
    setFrdPreviewVisible(false);
    setFrdPreviewHtml("");
    setFrdPreviewVersion(null);
  };

  const downloadAsWord = (htmlContent, filename) => {
    try {
      const preface = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${filename}</title></head><body>`;
      const blob = new Blob([preface + htmlContent + "</body></html>"], {
        type: "application/msword",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename.endsWith(".doc") ? filename : filename + ".doc";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setMsg("Failed to download document.");
      setTimeout(() => setMsg(""), 2000);
    }
  };

  const detectBusinessDomain = (inputs, project) => {
    // Combine all relevant text for intelligent domain analysis
    const allContent = [
      project || "",
      inputs.briefRequirements || "",
      inputs.requirements || "",
      inputs.scope || "",
      inputs.objectives || "",
      inputs.assumptions || "",
      inputs.constraints || ""
    ].join(" ").toLowerCase();

    console.log("🤖 AI Domain Analysis for content:", allContent.substring(0, 200) + "...");

    // Financial/Banking Domain Detection
    const financialKeywords = ['bank', 'banking', 'finance', 'financial', 'account', 'transaction', 'payment', 'credit', 'debit', 'loan', 'invoice', 'billing', 'accounting', 'journal', 'ledger', 'reconciliation', 'audit', 'compliance', 'regulatory', 'gl', 'p&l', 'balance sheet', 'cash flow', 'revenue', 'expense', 'asset', 'liability', 'equity'];
    const financialScore = financialKeywords.filter(keyword => allContent.includes(keyword)).length;

    // Marketing Domain Detection  
    const marketingKeywords = ['marketing', 'campaign', 'email', 'customer', 'lead', 'prospect', 'automation', 'crm', 'sales', 'communication', 'newsletter', 'promotion', 'advertising', 'brand', 'social media', 'engagement', 'conversion', 'funnel', 'roi', 'analytics', 'tracking', 'segment', 'target audience', 'personalization'];
    const marketingScore = marketingKeywords.filter(keyword => allContent.includes(keyword)).length;

    // Healthcare Domain Detection
    const healthcareKeywords = ['health', 'healthcare', 'patient', 'medical', 'hospital', 'clinic', 'doctor', 'nurse', 'treatment', 'diagnosis', 'medication', 'prescription', 'hipaa', 'ehr', 'emr', 'appointment', 'billing', 'insurance', 'claim'];
    const healthcareScore = healthcareKeywords.filter(keyword => allContent.includes(keyword)).length;

    // E-commerce Domain Detection
    const ecommerceKeywords = ['ecommerce', 'e-commerce', 'online store', 'shopping', 'cart', 'checkout', 'product', 'inventory', 'order', 'shipping', 'payment gateway', 'catalog', 'customer', 'purchase', 'retail', 'marketplace'];
    const ecommerceScore = ecommerceKeywords.filter(keyword => allContent.includes(keyword)).length;

    console.log("🔍 Domain Scores:", { financial: financialScore, marketing: marketingScore, healthcare: healthcareScore, ecommerce: ecommerceScore });

    // Return the domain with highest score (minimum 2 keywords to avoid false positives)
    const scores = [
      { domain: 'marketing', score: marketingScore },
      { domain: 'financial', score: financialScore },
      { domain: 'healthcare', score: healthcareScore },
      { domain: 'ecommerce', score: ecommerceScore }
    ];

    const topDomain = scores.reduce((max, current) => current.score > max.score ? current : max);
    
    if (topDomain.score >= 2) {
      console.log("✅ AI DETECTED DOMAIN:", topDomain.domain.toUpperCase());
      return topDomain.domain;
    }

    console.log("❓ Domain unclear, using generic validation");
    return 'generic';
  };

  const getValidationCriteria = (inputs, project) => {
    console.log("🔍 getValidationCriteria called with:", { inputs, project });
    
    // Always use AI domain detection, ignore user validation for now to test the intelligence
    const detectedDomain = detectBusinessDomain(inputs, project);
    
    // Generate domain-specific validation based on AI detection
    switch (detectedDomain) {
      case 'marketing':
        return `• Enforce customer consent validation for communication preferences<br/>
• Validate email address format and deliverability standards<br/>
• Implement campaign performance tracking and attribution models<br/>
• Enforce A/B testing validation for campaign optimization<br/>
• Validate lead scoring and segmentation accuracy<br/>
• Ensure GDPR compliance for customer data processing`;

      case 'financial':
        return `• Enforce multi-level approval workflows for financial transactions<br/>
• Validate accounting equation balance (Assets = Liabilities + Equity)<br/>
• Implement audit trail requirements for all financial entries<br/>
• Enforce regulatory compliance checks (SOX, GAAP)<br/>
• Validate currency conversion and rounding rules<br/>
• Implement segregation of duties for financial operations`;

      case 'healthcare':
        return `• Enforce HIPAA compliance for patient data protection<br/>
• Validate medical record integrity and audit trails<br/>
• Implement patient consent validation for treatments<br/>
• Enforce prescription and medication safety checks<br/>
• Validate provider credentials and licensing<br/>
• Implement emergency access protocols for patient data`;

      case 'ecommerce':
        return `• Validate inventory levels before order confirmation<br/>
• Enforce payment gateway security and PCI compliance<br/>
• Implement order fulfillment and shipping validation<br/>
• Validate product pricing and discount calculations<br/>
• Enforce customer authentication and fraud detection<br/>
• Implement return and refund policy validation`;

      default:
        return `• Validate data integrity and consistency across all modules<br/>
• Implement user authentication and authorization controls<br/>
• Enforce business rule validation and exception handling<br/>
• Validate system performance and scalability requirements<br/>
• Implement audit logging for all critical operations<br/>
• Enforce data backup and disaster recovery procedures`;
    }
    
    if (projectLower.includes("healthcare") || projectLower.includes("patient") || projectLower.includes("medical")) {
      return `• Enforce mandatory patient demographic fields (name, DOB, SSN)<br/>
• Validate medical record privacy and HIPAA compliance<br/>
• Require physician authorization for prescription access<br/>
• Enforce audit trails for all patient data modifications`;
    }
    
    if (projectLower.includes("banking") || projectLower.includes("financial") || projectLower.includes("payment")) {
      return `• Enforce strong customer authentication and account verification<br/>
• Validate transaction limits and fraud detection rules<br/>
• Require regulatory compliance with banking standards<br/>
• Enforce real-time balance verification before transactions`;
    }
    
    if (projectLower.includes("ecommerce") || projectLower.includes("shopping") || projectLower.includes("order")) {
      return `• Enforce product inventory validation before order confirmation<br/>
• Validate shipping address and payment method accuracy<br/>
• Require secure checkout process with payment verification<br/>
• Enforce order tracking and delivery confirmation`;
    }
    
    // Default professional validation criteria
    return `• Enforce data accuracy and completeness validation<br/>
• Validate user access controls and authentication<br/>
• Require audit trails for all system modifications<br/>
• Enforce security protocols and compliance standards`;
  };

  const generateBrdHtml = ({ project, inputs, version, domain = null }) => {
    const idxItems = [
      "Executive Summary",
      "Project Scope",
      "Business Objectives",
      "Budget Details",
      "Business Requirements",
      "Assumptions",
      "Constraints",
      "Validations & Acceptance Criteria",
      "Appendices",
    ];
    const html = `
      <div style="font-family:Calibri, Arial, Helvetica, sans-serif;color:#111827;line-height:1.45;padding:18px;">
        <h1 style="text-align:center;margin-bottom:6px;">Business Requirement Document (BRD)</h1>
        <h2 style="text-align:center;margin-top:2px;">${project} — BRD Version-${version}</h2>
        <hr/>
        <h3>Document Index</h3>
        <ol>
          ${idxItems.map((i) => `<li>${i}</li>`).join("")}
        </ol>

        <h2>1. Executive Summary</h2>
        <p>This document captures the business requirements for the project <strong>${project}</strong>. It follows standard BA practice aligned to BABOK and provides the scope, objectives, requirements, budget and validations required for delivering the solution.</p>

        <h2>2. Project Scope</h2>
        <p>${(inputs.scope || "").replace(/\n/g, "<br/>")}</p>

        <h2>3. Business Objectives</h2>
        <p>${(inputs.objectives || "").replace(/\n/g, "<br/>")}</p>

        <h2>4. Budget Details</h2>
        <p>${(inputs.budget || "").replace(/\n/g, "<br/>")}</p>

        <h2>5. Business Requirements (EPIC Format)</h2>
        ${formatRequirementsAsEpics(inputs.briefRequirements || "", project, domain)}

        <h2>6. Assumptions</h2>
        <p>${(inputs.assumptions || "").replace(/\n/g, "<br/>")}</p>

        <h2>7. Constraints</h2>
        <p>${(inputs.constraints || "").replace(/\n/g, "<br/>")}</p>

        <h2>8. Validations & Acceptance Criteria</h2>
        <p>🤖 AI DOMAIN DETECTION ACTIVE - ${getValidationCriteria(inputs, project)}</p>

        <h2>9. Appendices</h2>
        <p>Appendix A: Glossary<br/>Appendix B: References</p>

        <hr/>
        <p style="font-size:11px;color:#6b7280;">Generated by BA Assistant Tool</p>
      </div>
    `;
    return html;
  };

  // STANDALONE FRD GENERATION - Convert BRD to FRD with EPIC formatting
  const generateFrdFromBrd = (brdText, project, version) => {
    // Extract business domain from BRD text
    const domain = detectDomainFromBrdText(brdText);
    
    // Parse requirements from BRD to create EPICs and User Stories
    const requirements = extractRequirementsFromBrd(brdText);
    const epics = convertRequirementsToEpics(requirements, domain);
    const userStories = convertEpicsToUserStories(epics, domain);
    
    const html = `
      <div style="font-family:Calibri, Arial, Helvetica, sans-serif;color:#111827;line-height:1.45;padding:18px;">
        <h1 style="text-align:center;margin-bottom:6px;">Functional Requirement Document (FRD)</h1>
        <h2 style="text-align:center;margin-top:2px;">${project} — FRD Version-${version}</h2>
        <div style="background:#f3f4f6;padding:8px;border-radius:4px;margin:12px 0;">
          <strong>🤖 AI DOMAIN INTELLIGENCE: ${domain.toUpperCase()} DOMAIN DETECTED</strong>
        </div>
        <hr/>
        
        <h3>Document Index</h3>
        <ol>
          <li>Executive Summary</li>
          <li>EPIC Breakdown</li>
          <li>User Stories</li>
          <li>Functional Requirements</li>
          <li>Acceptance Criteria</li>
          <li>Technical Specifications</li>
        </ol>

        <h2>1. Executive Summary</h2>
        <p>This Functional Requirements Document (FRD) translates the business requirements into detailed functional specifications for <strong>${project}</strong>. 
        The requirements are organized into EPICs and User Stories following Agile methodology with ${domain}-specific domain expertise.</p>

        <h2>2. EPIC Breakdown</h2>
        ${epics.map(epic => `
          <div style="border:1px solid #d1d5db;margin:10px 0;padding:12px;border-radius:6px;">
            <h3 style="color:#1f2937;margin-top:0;">${epic.id}: ${epic.title}</h3>
            <p><strong>Description:</strong> ${epic.description}</p>
            <p><strong>Business Value:</strong> ${epic.businessValue}</p>
            <p><strong>Acceptance Criteria:</strong></p>
            <ul>
              ${epic.acceptanceCriteria.map(criteria => `<li>${criteria}</li>`).join('')}
            </ul>
          </div>
        `).join('')}

        <h2>3. User Stories</h2>
        ${userStories.map(story => `
          <div style="border:1px solid #e5e7eb;margin:8px 0;padding:10px;border-radius:4px;background:#f9fafb;">
            <h4 style="color:#374151;margin-top:0;">${story.id}: ${story.title}</h4>
            <p><strong>As a</strong> ${story.asA}, <strong>I want</strong> ${story.iWant}, <strong>so that</strong> ${story.soThat}.</p>
            <p><strong>Acceptance Criteria:</strong></p>
            <ul>
              ${story.acceptanceCriteria.map(criteria => `<li>${criteria}</li>`).join('')}
            </ul>
            <div style="background:#fff3cd;padding:8px;border-radius:4px;margin:8px 0;border-left:4px solid #ffc107;">
              <p style="margin:0;"><strong>🔍 Validation Criteria:</strong></p>
              <ul style="margin:4px 0 0 0;">
                ${story.validationCriteria.map(validation => `<li>${validation}</li>`).join('')}
              </ul>
            </div>
            <p><strong>Priority:</strong> ${story.priority} | <strong>Story Points:</strong> ${story.storyPoints}</p>
          </div>
        `).join('')}

        <h2>4. Functional Requirements</h2>
        <p>The following functional requirements have been derived from the business requirements and organized by EPIC:</p>
        ${epics.map(epic => `
          <h3>${epic.id} Functional Requirements</h3>
          <ul>
            ${epic.functionalRequirements.map(req => `<li>${req}</li>`).join('')}
          </ul>
        `).join('')}

        <h2>5. Acceptance Criteria</h2>
        <p>Each EPIC and User Story includes specific acceptance criteria tailored for the ${domain} domain:</p>
        <ul>
          <li>All functional requirements must be validated against ${domain} industry standards</li>
          <li>User acceptance testing must cover all defined user stories</li>
          <li>Performance criteria must meet ${domain}-specific requirements</li>
          <li>Security and compliance requirements must be validated</li>
        </ul>

        <h2>6. Technical Specifications</h2>
        <p>Technical implementation details will be defined in separate Technical Requirements Document (TRD) based on these functional requirements.</p>

        <hr/>
        <p style="font-size:11px;color:#6b7280;">Generated by BA Assistant Tool with AI Domain Intelligence</p>
      </div>
    `;
    return html;
  };

  // Domain detection specifically for FRD generation from BRD text
  const detectDomainFromBrdText = (brdText) => {
    const text = brdText.toLowerCase();
    
    const domainKeywords = {
      telecom: ['telecom', 'telecommunication', 'sim', 'esim', 'mnp', 'ocs', 'billing', 'charging', 'kyc', 'activation', 'provisioning', 'hlr', 'hss', 'udm', 'pcf', 'trai', 'dot', 'carrier', 'subscriber', 'msisdn', 'imsi', 'network', 'tariff', 'plan', 'postpaid', 'prepaid', 'roaming', 'sms', 'data', 'voice', 'bss', 'oss', 'revenue assurance', 'dunning', 'mediation'],
      airline: ['flight', 'airline', 'aviation', 'passenger', 'booking', 'pnr', 'ticket', 'fare', 'seat', 'baggage', 'airport', 'gds', 'iata', 'aircraft', 'departure', 'arrival', 'ancillary', 'itinerary', 'check-in', 'boarding'],
      financial: ['investment', 'portfolio', 'trading', 'finance', 'banking', 'fund', 'asset', 'equity', 'debt', 'risk', 'compliance', 'audit', 'revenue', 'profit', 'budget', 'cost', 'accounting', 'transaction'],
      healthcare: ['patient', 'medical', 'clinical', 'diagnosis', 'treatment', 'healthcare', 'hospital', 'doctor', 'nurse', 'prescription', 'hipaa', 'medical record', 'clinical'],
      ecommerce: ['product', 'cart', 'checkout', 'payment', 'order', 'inventory', 'shipping', 'customer', 'ecommerce', 'online store', 'marketplace', 'catalog'],
      marketing: ['campaign', 'brand', 'customer', 'lead', 'conversion', 'engagement', 'social media', 'advertising', 'promotion', 'analytics', 'roi', 'ctr', 'cpc', 'segment']
    };
    
    let maxScore = 0;
    let detectedDomain = 'generic';
    
    Object.keys(domainKeywords).forEach(domain => {
      const score = domainKeywords[domain].filter(keyword => text.includes(keyword)).length;
      if (score > maxScore) {
        maxScore = score;
        detectedDomain = domain;
      }
    });
    
    console.log(`🎯 FRD Domain Detection: ${detectedDomain} (score: ${maxScore})`);
    return detectedDomain;
  };

  // Helper functions for FRD generation
  const extractRequirementsFromBrd = (brdText) => {
    // Extract requirements from BRD text with improved parsing
    const lines = brdText.split('\n').map(line => line.trim()).filter(line => line);
    const requirements = [];
    
    let currentEpicId = '';
    let currentEpicTitle = '';
    let inRequirementsSection = false;
    
    for (const line of lines) {
      // Detect EPIC sections
      if (line.match(/EPIC-\d+/)) {
        currentEpicId = line.match(/EPIC-\d+/)[0];
        currentEpicTitle = line.split(':')[1]?.trim() || 'Core System';
        inRequirementsSection = false;
        continue;
      }
      
      // Detect Requirements sections within EPICs
      if (line.toLowerCase().includes('requirements:') && currentEpicId) {
        inRequirementsSection = true;
        continue;
      }
      
      // Extract detailed requirements from bullet points within EPIC sections
      if (inRequirementsSection && (line.startsWith('•') || line.startsWith('-') || line.startsWith('*'))) {
        const cleanLine = line.replace(/^[•\-\*]\s*/, '').trim();
        if (cleanLine.length > 10) {
          requirements.push({
            text: cleanLine,
            epicId: currentEpicId,
            epicTitle: currentEpicTitle,
            priority: determinePriority(cleanLine),
            isDetailed: true
          });
        }
      }
    }
    
    console.log(`📋 Extracted ${requirements.length} requirements from BRD:`);
    requirements.forEach((req, i) => console.log(`  ${req.epicId}: ${req.text.substring(0, 80)}...`));
    
    return requirements;
  };

  const convertRequirementsToEpics = (requirements, domain) => {
    const epics = [];
    
    if (requirements.length === 0) {
      return getDefaultEpicsForDomain(domain);
    }
    
    // Group requirements by EPIC ID and analyze content to create meaningful EPICs
    const epicGroups = {};
    requirements.forEach(req => {
      const epicId = req.epicId || 'EPIC-01';
      if (!epicGroups[epicId]) {
        epicGroups[epicId] = [];
      }
      epicGroups[epicId].push(req);
    });
    
    // Create EPICs based on actual requirements content
    Object.keys(epicGroups).forEach(epicId => {
      const reqs = epicGroups[epicId];
      const epicTitle = generateMeaningfulEpicTitle(reqs, domain);
      const description = generateEpicDescription(reqs, epicTitle, domain);
      
      epics.push({
        id: epicId,
        title: epicTitle,
        description: description,
        businessValue: getDomainBusinessValue(epicTitle, domain),
        acceptanceCriteria: generateEpicAcceptanceCriteria(reqs, domain),
        functionalRequirements: reqs.map(req => req.text),
        priority: reqs.some(r => r.priority === 'High') ? 'High' : 'Medium'
      });
    });
    
    return epics;
  };
  
  // Generate meaningful EPIC titles based on actual requirements
  const generateMeaningfulEpicTitle = (requirements, domain) => {
    // Handle both old format (array of objects with .text) and new format (array of strings)
    const reqText = Array.isArray(requirements) 
      ? requirements.map(r => typeof r === 'string' ? r : r.text).join(' ').toLowerCase()
      : requirements.toLowerCase();
    
    // Telecom domain specific grouping
    if (domain === 'telecom') {
      if (reqText.includes('lead to order') || reqText.includes('catalog') || reqText.includes('offer') || reqText.includes('eligibility') || reqText.includes('credit check')) {
        return 'Product Catalog & Order Management';
      }
      if (reqText.includes('kyc') || reqText.includes('activation') || reqText.includes('sim') || reqText.includes('esim') || reqText.includes('mnp') || reqText.includes('provisioning')) {
        return 'Customer Onboarding & SIM Activation';
      }
      if (reqText.includes('charging') || reqText.includes('billing') || reqText.includes('rating') || reqText.includes('ocs') || reqText.includes('invoicing') || reqText.includes('dunning')) {
        return 'Charging & Billing Management';
      }
      if (reqText.includes('care') || reqText.includes('assurance') || reqText.includes('tickets') || reqText.includes('diagnostics') || reqText.includes('outages') || reqText.includes('knowledge base')) {
        return 'Customer Care & Service Assurance';
      }
      if (reqText.includes('payment') || reqText.includes('collection') || reqText.includes('cards') || reqText.includes('upi') || reqText.includes('autopay') || reqText.includes('refund')) {
        return 'Payment & Collection Management';
      }
      if (reqText.includes('partner') || reqText.includes('retailer') || reqText.includes('commission') || reqText.includes('inventory') || reqText.includes('sales reporting')) {
        return 'Partner & Channel Management';
      }
      if (reqText.includes('analytics') || reqText.includes('compliance') || reqText.includes('usage') || reqText.includes('churn') || reqText.includes('revenue') || reqText.includes('audit') || reqText.includes('regulatory')) {
        return 'Analytics & Regulatory Compliance';
      }
    }
    
    // Financial domain specific grouping
    if (domain === 'financial') {
      if (reqText.includes('intake') || reqText.includes('onboard') || reqText.includes('digital') || reqText.includes('form')) {
        return 'Investor Onboarding & Digital Intake';
      }
      if (reqText.includes('kyc') || reqText.includes('aml') || reqText.includes('screening') || reqText.includes('compliance')) {
        return 'Compliance & Risk Management';
      }
      if (reqText.includes('sign') || reqText.includes('document') || reqText.includes('stamp') || reqText.includes('version')) {
        return 'Document Management & E-Signature';
      }
      if (reqText.includes('payment') || reqText.includes('bank') || reqText.includes('funding') || reqText.includes('penny')) {
        return 'Payment & Fund Management';
      }
      if (reqText.includes('tracking') || reqText.includes('notification') || reqText.includes('communication') || reqText.includes('export')) {
        return 'Communication & Integration Management';
      }
    }
    
    // Airline domain specific grouping
    if (domain === 'airline') {
      if (reqText.includes('search') || reqText.includes('shopping') || reqText.includes('availability')) {
        return 'Flight Search & Shopping';
      }
      if (reqText.includes('booking') || reqText.includes('pnr') || reqText.includes('reservation')) {
        return 'Booking & Reservation Management';
      }
      if (reqText.includes('payment') || reqText.includes('ticket') || reqText.includes('billing')) {
        return 'Payment & Ticketing';
      }
    }
    
    // Generic grouping for other domains
    if (reqText.includes('user') || reqText.includes('account') || reqText.includes('auth')) {
      return 'User Management & Authentication';
    }
    if (reqText.includes('data') || reqText.includes('process') || reqText.includes('manage')) {
      return 'Data Processing & Management';
    }
    if (reqText.includes('report') || reqText.includes('analytic') || reqText.includes('track')) {
      return 'Reporting & Analytics';
    }
    
    return 'Core Business Functionality';
  };
  
  // Generate EPIC descriptions based on requirements
  const generateEpicDescription = (requirements, title, domain) => {
    const mainFunctions = requirements.slice(0, 3).map(r => r.text.toLowerCase()).join(', ');
    return `Implement ${title.toLowerCase()} including ${mainFunctions} with ${domain}-specific business logic and industry compliance`;
  };
  
  // Generate EPIC acceptance criteria based on actual requirements
  const generateEpicAcceptanceCriteria = (requirements, domain) => {
    const criteria = [];
    
    // Add requirement-specific criteria
    requirements.slice(0, 3).forEach(req => {
      const reqLower = req.text.toLowerCase();
      if (reqLower.includes('intake') || reqLower.includes('form')) {
        criteria.push('Digital forms are intuitive and guide users through the process');
      }
      if (reqLower.includes('validation') || reqLower.includes('verify')) {
        criteria.push('Real-time validation provides immediate feedback to users');
      }
      if (reqLower.includes('document') || reqLower.includes('upload')) {
        criteria.push('Document upload and management supports required file formats');
      }
      if (reqLower.includes('workflow') || reqLower.includes('approval')) {
        criteria.push('Approval workflows enforce business rules and compliance');
      }
    });
    
    // Add domain-specific criteria
    if (domain === 'financial') {
      criteria.push('All functionality complies with financial regulations (SEC, FINRA)');
      criteria.push('Audit trails are maintained for regulatory compliance');
    }
    
    criteria.push('Performance meets industry standards');
    criteria.push('Security and data protection requirements are satisfied');
    
    return criteria.slice(0, 4); // Limit to 4 criteria
  };

  // Domain-specific grouping logic
  const getDomainSpecificGrouping = (requirements, domain) => {
    const groups = {};
    
    if (domain === 'airline') {
      // Airline-specific grouping
      requirements.forEach(req => {
        const text = req.text.toLowerCase();
        let feature = 'Flight Operations';
        
        if (text.includes('search') || text.includes('availability') || text.includes('shopping')) {
          feature = 'Flight Search & Shopping';
        } else if (text.includes('booking') || text.includes('pnr') || text.includes('reservation')) {
          feature = 'Booking & Reservation Management';
        } else if (text.includes('payment') || text.includes('ticket') || text.includes('billing')) {
          feature = 'Payment & Ticketing';
        } else if (text.includes('seat') || text.includes('ancillary') || text.includes('baggage') || text.includes('meal')) {
          feature = 'Ancillary Services';
        } else if (text.includes('change') || text.includes('cancel') || text.includes('refund')) {
          feature = 'Post-Booking Services';
        } else if (text.includes('admin') || text.includes('ops') || text.includes('queue') || text.includes('report')) {
          feature = 'Operations & Administration';
        }
        
        if (!groups[feature]) groups[feature] = [];
        groups[feature].push(req);
      });
    } else {
      // Generic grouping for other domains
      requirements.forEach(req => {
        let feature = 'Core System';
        
        if (req.text.toLowerCase().includes('user') || req.text.toLowerCase().includes('auth')) {
          feature = 'User Management';
        } else if (req.text.toLowerCase().includes('data') || req.text.toLowerCase().includes('process')) {
          feature = 'Data Processing';
        } else if (req.text.toLowerCase().includes('report') || req.text.toLowerCase().includes('analytic')) {
          feature = 'Reporting';
        } else if (req.section && req.section !== '') {
          feature = req.section;
        }
        
        if (!groups[feature]) groups[feature] = [];
        groups[feature].push(req);
      });
    }
    
    return groups;
  };

  // Domain-specific business value
  const getDomainBusinessValue = (feature, domain) => {
    const domainValues = {
      airline: {
        'Flight Search & Shopping': 'Enables passengers to find and compare flights, increasing conversion rates and revenue',
        'Booking & Reservation Management': 'Streamlines reservation process, reducing abandonment and improving customer experience',
        'Payment & Ticketing': 'Ensures secure payment processing and instant ticket issuance, reducing fraud and improving cash flow',
        'Ancillary Services': 'Maximizes ancillary revenue through upselling services like seats, bags, and meals',
        'Post-Booking Services': 'Reduces call center load and improves customer satisfaction through self-service options',
        'Operations & Administration': 'Provides operational efficiency and business intelligence for airline staff'
      }
    };
    
    return domainValues[domain]?.[feature] || `Enables efficient ${feature.toLowerCase()} operations and improves ${domain} business processes`;
  };

  // Domain-specific acceptance criteria
  const getDomainAcceptanceCriteria = (feature, domain) => {
    const domainCriteria = {
      airline: {
        'Flight Search & Shopping': [
          'Flight search results are returned within 3 seconds',
          'All GDS/NDC sources are integrated and searchable',
          'Fare rules and restrictions are clearly displayed',
          'Search filters work correctly (price, timing, airline, stops)'
        ],
        'Booking & Reservation Management': [
          'PNR creation follows IATA standards',
          'Passenger data validation meets airline requirements',
          'Seat selection integrates with airline seat maps',
          'Booking confirmations are sent immediately'
        ],
        'Payment & Ticketing': [
          'Payment processing is PCI DSS compliant',
          'Ticket issuance follows IATA standards',
          'Fraud detection rules are implemented',
          'EMD generation for ancillaries is supported'
        ],
        'Ancillary Services': [
          'Seat map integration displays real-time availability',
          'Baggage rules are accurately calculated and displayed',
          'Meal preferences are captured and transmitted to airline',
          'Ancillary EMDs are generated automatically'
        ],
        'Post-Booking Services': [
          'Change and cancellation rules are enforced automatically',
          'Refund calculations follow airline fare rules',
          'Schedule change notifications are sent real-time',
          'Voucher and credit management is fully automated'
        ],
        'Operations & Administration': [
          'Queue management supports airline operational workflows',
          'Reporting provides real-time business intelligence',
          'IRROPS support enables disruption management',
          'Audit trails meet regulatory requirements'
        ]
      }
    };
    
    return domainCriteria[domain]?.[feature] || [
      `${feature} functionality is fully implemented and tested`,
      `All ${domain}-specific requirements are met`,
      'Performance meets industry standards',
      'Security and compliance requirements are satisfied'
    ];
  };

  // Default EPICs for specific domains when no requirements are extracted
  const getDefaultEpicsForDomain = (domain) => {
    const defaults = {
      airline: [
        {
          id: 'EPIC-01',
          title: 'Flight Search & Shopping',
          description: 'Comprehensive flight search and shopping experience with multi-source integration',
          businessValue: 'Enables passengers to find and compare flights, increasing conversion rates',
          acceptanceCriteria: [
            'Multi-city, round-trip, and one-way search capabilities',
            'Real-time fare and availability from GDS/NDC sources',
            'Advanced filtering and sorting options',
            'Branded fares and ancillary product display'
          ],
          functionalRequirements: ['Flight search functionality', 'Fare comparison and display', 'Filter and sort capabilities'],
          priority: 'High'
        }
      ]
    };
    
    return defaults[domain] || [
      {
        id: 'EPIC-01',
        title: 'Core System Requirements',
        description: 'Basic system functionality requirements',
        businessValue: 'Provides core system capabilities',
        acceptanceCriteria: ['System functionality implemented', 'Basic requirements met'],
        functionalRequirements: ['Core system functionality'],
        priority: 'Medium'
      }
    ];
  };

  const convertEpicsToUserStories = (epics, domain) => {
    const userStories = [];
    
    epics.forEach((epic, epicIndex) => {
      // Generate user stories based on actual requirements within each EPIC
      const stories = generateUserStoriesFromRequirements(epic, domain, epicIndex);
      userStories.push(...stories);
    });
    
    return userStories;
  };

  // Generate user stories based on actual EPIC requirements
  const generateUserStoriesFromRequirements = (epic, domain, epicIndex) => {
    const stories = [];
    const requirements = epic.functionalRequirements;
    
    // Group related requirements into logical user stories
    const storyGroups = groupRequirementsIntoStories(requirements, epic.title, domain);
    
    storyGroups.forEach((storyGroup, storyIndex) => {
      const storyId = `US-${String(epicIndex + 1).padStart(2, '0')}-${String(storyIndex + 1).padStart(2, '0')}`;
      const persona = getAppropriatePersona(storyGroup.requirements, domain);
      const storyTitle = generateStoryTitle(storyGroup, epic.title);
      const storyWant = generateStoryWant(storyGroup.requirements);
      const storySoThat = generateStorySoThat(storyGroup.requirements, domain);
      
      stories.push({
        id: storyId,
        title: storyTitle,
        asA: persona,
        iWant: storyWant,
        soThat: storySoThat,
        acceptanceCriteria: generateStoryAcceptanceCriteria(storyGroup.requirements),
        validationCriteria: getStoryValidationCriteria(domain, epic.title, storyGroup.action, persona),
        priority: epic.priority,
        storyPoints: calculateStoryPoints(storyGroup.requirements),
        epicId: epic.id
      });
    });
    
    return stories;
  };

  // Group requirements into logical user stories
  const groupRequirementsIntoStories = (requirements, epicTitle, domain) => {
    const groups = [];
    
    // For financial domain, create specific story groups
    if (domain === 'financial') {
      if (epicTitle.includes('Onboarding') || epicTitle.includes('Intake')) {
        requirements.forEach(req => {
          const reqLower = req.toLowerCase();
          if (reqLower.includes('digital intake') || reqLower.includes('form')) {
            groups.push({
              action: 'Complete Digital Intake',
              requirements: [req],
              focus: 'intake'
            });
          } else if (reqLower.includes('eligibility') || reqLower.includes('accreditation')) {
            groups.push({
              action: 'Verify Eligibility',
              requirements: [req],
              focus: 'verification'
            });
          } else if (reqLower.includes('document upload')) {
            groups.push({
              action: 'Upload Documents',
              requirements: [req],
              focus: 'documentation'
            });
          }
        });
      } else if (epicTitle.includes('Compliance')) {
        requirements.forEach(req => {
          const reqLower = req.toLowerCase();
          if (reqLower.includes('kyc') || reqLower.includes('aml')) {
            groups.push({
              action: 'Complete KYC/AML Screening',
              requirements: [req],
              focus: 'compliance'
            });
          } else if (reqLower.includes('screening') || reqLower.includes('risk scoring')) {
            groups.push({
              action: 'Perform Risk Assessment',
              requirements: [req],
              focus: 'risk'
            });
          }
        });
      }
    }
    
    // If no specific groups created, create generic ones
    if (groups.length === 0) {
      const mid = Math.ceil(requirements.length / 2);
      if (requirements.length > 1) {
        groups.push({
          action: 'Manage Primary Functions',
          requirements: requirements.slice(0, mid),
          focus: 'primary'
        });
        groups.push({
          action: 'Handle Secondary Operations',
          requirements: requirements.slice(mid),
          focus: 'secondary'
        });
      } else {
        groups.push({
          action: 'Execute Core Functionality',
          requirements: requirements,
          focus: 'core'
        });
      }
    }
    
    return groups;
  };

  // Get appropriate persona based on requirements
  // 🎭 Enhanced Persona Assignment with contextual intelligence  
  const getAppropriatePersona = (requirements, domain) => {
    const reqText = requirements.join(' ').toLowerCase();
    
    // Enhanced telecom personas with contextual intelligence
    if (domain === 'telecom') {
      if (reqText.includes('catalog') || reqText.includes('offer') || reqText.includes('order') || reqText.includes('eligibility')) {
        return 'Customer';
      }
      if (reqText.includes('kyc') || reqText.includes('activation') || reqText.includes('provisioning') || reqText.includes('sim')) {
        return 'Customer Service Representative';
      }
      if (reqText.includes('billing') || reqText.includes('charging') || reqText.includes('payment') || reqText.includes('collection')) {
        return 'Billing Specialist';
      }
      if (reqText.includes('care') || reqText.includes('ticket') || reqText.includes('diagnostic') || reqText.includes('trouble')) {
        return 'Technical Support Agent';
      }
      if (reqText.includes('partner') || reqText.includes('retailer') || reqText.includes('commission') || reqText.includes('sales')) {
        return 'Channel Partner';
      }
      if (reqText.includes('analytics') || reqText.includes('compliance') || reqText.includes('audit') || reqText.includes('regulatory')) {
        return 'Business Analyst';
      }
    }
    
    // Enhanced financial personas with contextual intelligence
    if (domain === 'financial') {
      if (reqText.includes('investor') || reqText.includes('individual') || reqText.includes('intake')) {
        return 'Investor';
      }
      if (reqText.includes('reviewer') || reqText.includes('approval') || reqText.includes('compliance')) {
        return 'Compliance Officer';
      }
      if (reqText.includes('admin') || reqText.includes('manage') || reqText.includes('workflow')) {
        return 'Fund Administrator';
      }
      if (reqText.includes('portfolio') || reqText.includes('investment') || reqText.includes('allocation')) {
        return 'Portfolio Manager';
      }
      if (reqText.includes('trading') || reqText.includes('execution') || reqText.includes('settlement')) {
        return 'Trading Specialist';
      }
      if (reqText.includes('risk') || reqText.includes('assessment') || reqText.includes('monitoring')) {
        return 'Risk Analyst';
      }
    }
    
    // Enhanced airline personas with contextual intelligence  
    if (domain === 'airline') {
      if (reqText.includes('passenger') || reqText.includes('booking') || reqText.includes('flight') || reqText.includes('travel')) {
        return 'Passenger';
      }
      if (reqText.includes('check-in') || reqText.includes('counter') || reqText.includes('boarding')) {
        return 'Check-in Agent';
      }
      if (reqText.includes('operations') || reqText.includes('schedule') || reqText.includes('disruption')) {
        return 'Operations Manager';
      }
      if (reqText.includes('crew') || reqText.includes('cabin') || reqText.includes('flight attendant')) {
        return 'Cabin Crew';
      }
      if (reqText.includes('baggage') || reqText.includes('handling') || reqText.includes('cargo')) {
        return 'Baggage Handler';
      }
      if (reqText.includes('maintenance') || reqText.includes('aircraft') || reqText.includes('safety')) {
        return 'Maintenance Engineer';
      }
    }
    
    // Enhanced healthcare personas with contextual intelligence
    if (domain === 'healthcare') {
      if (reqText.includes('patient') || reqText.includes('individual') || reqText.includes('appointment')) {
        return 'Patient';
      }
      if (reqText.includes('doctor') || reqText.includes('physician') || reqText.includes('diagnosis')) {
        return 'Physician';
      }
      if (reqText.includes('nurse') || reqText.includes('clinical') || reqText.includes('care')) {
        return 'Clinical Nurse';
      }
      if (reqText.includes('admin') || reqText.includes('receptionist') || reqText.includes('registration')) {
        return 'Medical Administrator';
      }
      if (reqText.includes('prescription') || reqText.includes('medication') || reqText.includes('pharmacy')) {
        return 'Pharmacist';
      }
      if (reqText.includes('insurance') || reqText.includes('claim') || reqText.includes('coverage')) {
        return 'Insurance Coordinator';
      }
    }
    
    // Enhanced ecommerce personas with contextual intelligence
    if (domain === 'ecommerce') {
      if (reqText.includes('customer') || reqText.includes('shopper') || reqText.includes('browse') || reqText.includes('purchase')) {
        return 'Customer';
      }
      if (reqText.includes('merchant') || reqText.includes('seller') || reqText.includes('vendor')) {
        return 'Merchant';
      }
      if (reqText.includes('admin') || reqText.includes('store') || reqText.includes('manager')) {
        return 'Store Manager';
      }
      if (reqText.includes('inventory') || reqText.includes('product') || reqText.includes('catalog')) {
        return 'Product Manager';
      }
      if (reqText.includes('order') || reqText.includes('fulfillment') || reqText.includes('shipping')) {
        return 'Fulfillment Specialist';
      }
      if (reqText.includes('support') || reqText.includes('service') || reqText.includes('help')) {
        return 'Customer Service Representative';
      }
    }
    
    // Enhanced marketing personas with contextual intelligence
    if (domain === 'marketing') {
      if (reqText.includes('marketer') || reqText.includes('manager') || reqText.includes('campaign')) {
        return 'Marketing Manager';
      }
      if (reqText.includes('analyst') || reqText.includes('data') || reqText.includes('analytics')) {
        return 'Marketing Analyst';
      }
      if (reqText.includes('customer') || reqText.includes('prospect') || reqText.includes('lead')) {
        return 'Prospective Customer';
      }
      if (reqText.includes('content') || reqText.includes('creative') || reqText.includes('copy')) {
        return 'Content Manager';
      }
      if (reqText.includes('email') || reqText.includes('automation') || reqText.includes('workflow')) {
        return 'Email Marketing Specialist';
      }
      if (reqText.includes('social') || reqText.includes('media') || reqText.includes('engagement')) {
        return 'Social Media Manager';
      }
    }
    
    // Enhanced default personas by domain with more variety
    const defaultPersonas = {
      telecom: ['Customer', 'Customer Service Representative', 'Technical Support Agent', 'Billing Specialist'],
      airline: ['Passenger', 'Check-in Agent', 'Operations Manager', 'Cabin Crew'],
      financial: ['Investor', 'Portfolio Manager', 'Compliance Officer', 'Trading Specialist'],
      healthcare: ['Patient', 'Physician', 'Clinical Nurse', 'Medical Administrator'],
      ecommerce: ['Customer', 'Store Manager', 'Product Manager', 'Fulfillment Specialist'],
      marketing: ['Marketing Manager', 'Marketing Analyst', 'Content Manager', 'Email Marketing Specialist']
    };
    
    return defaultPersonas[domain]?.[0] || 'User';
  };

  // Generate story title based on group
  const generateStoryTitle = (storyGroup, epicTitle) => {
    return `${epicTitle} - ${storyGroup.action}`;
  };

  // Generate "I want" statement from requirements
  const generateStoryWant = (requirements) => {
    const firstReq = requirements[0].toLowerCase();
    
    // Telecom-specific wants
    if (firstReq.includes('catalog') || firstReq.includes('offer')) {
      return 'browse product catalog and view available offers';
    }
    if (firstReq.includes('eligibility') || firstReq.includes('credit check')) {
      return 'check customer eligibility and perform credit verification';
    }
    if (firstReq.includes('kyc') || firstReq.includes('activation')) {
      return 'complete KYC verification and activate services';
    }
    if (firstReq.includes('sim') || firstReq.includes('esim') || firstReq.includes('provisioning')) {
      return 'provision and activate SIM/eSIM with seamless setup';
    }
    if (firstReq.includes('mnp') || firstReq.includes('portability')) {
      return 'process mobile number portability requests efficiently';
    }
    if (firstReq.includes('charging') || firstReq.includes('billing') || firstReq.includes('rating')) {
      return 'manage real-time charging and accurate billing processes';
    }
    if (firstReq.includes('care') || firstReq.includes('ticket') || firstReq.includes('diagnostic')) {
      return 'handle customer care requests and resolve technical issues';
    }
    if (firstReq.includes('payment') || firstReq.includes('collection')) {
      return 'process payments and manage collections efficiently';
    }
    if (firstReq.includes('partner') || firstReq.includes('retailer')) {
      return 'manage partner relationships and channel operations';
    }
    if (firstReq.includes('analytics') || firstReq.includes('reporting')) {
      return 'generate analytics and compliance reports';
    }
    
    // Financial-specific wants
    if (firstReq.includes('digital intake') || firstReq.includes('form')) {
      return 'complete digital intake forms with guided assistance';
    }
    if (firstReq.includes('document upload')) {
      return 'upload required documents with real-time validation';
    }
    if (firstReq.includes('kyc') || firstReq.includes('screening')) {
      return 'complete KYC/AML screening and compliance checks';
    }
    if (firstReq.includes('payment') || firstReq.includes('funding')) {
      return 'process payments and funding transactions securely';
    }
    if (firstReq.includes('sign') || firstReq.includes('stamp')) {
      return 'electronically sign documents and manage versions';
    }
    
    // Generic fallback
    return `implement ${firstReq.split('.')[0].replace(/^[•\-\*]\s*/, '')}`;
  };

  // Generate "so that" statement based on domain and requirements
  const generateStorySoThat = (requirements, domain) => {
    const reqText = requirements.join(' ').toLowerCase();
    
    if (domain === 'telecom') {
      if (reqText.includes('catalog') || reqText.includes('offer') || reqText.includes('order')) {
        return 'I can easily discover and subscribe to relevant services';
      }
      if (reqText.includes('kyc') || reqText.includes('activation') || reqText.includes('provisioning')) {
        return 'I can quickly onboard and start using telecom services';
      }
      if (reqText.includes('billing') || reqText.includes('charging') || reqText.includes('rating')) {
        return 'I can ensure accurate and transparent billing processes';
      }
      if (reqText.includes('care') || reqText.includes('ticket') || reqText.includes('support')) {
        return 'I can receive timely and effective customer support';
      }
      if (reqText.includes('payment') || reqText.includes('collection')) {
        return 'I can make payments conveniently and maintain service continuity';
      }
      if (reqText.includes('partner') || reqText.includes('channel') || reqText.includes('retailer')) {
        return 'I can effectively manage and grow channel partnerships';
      }
      if (reqText.includes('analytics') || reqText.includes('compliance') || reqText.includes('regulatory')) {
        return 'I can make data-driven decisions and ensure regulatory compliance';
      }
    }
    
    if (domain === 'financial') {
      if (reqText.includes('investor') || reqText.includes('onboard')) {
        return 'I can efficiently onboard and start investing';
      }
      if (reqText.includes('compliance') || reqText.includes('kyc')) {
        return 'I can ensure regulatory compliance and risk management';
      }
      if (reqText.includes('document') || reqText.includes('sign')) {
        return 'I can complete legal requirements securely';
      }
      if (reqText.includes('payment') || reqText.includes('fund')) {
        return 'I can process investments and manage funds';
      }
    }
    
    return 'I can accomplish my business objectives efficiently';
  };

  // Generate acceptance criteria from requirements
  // 🤖 AI-Enhanced Acceptance Criteria Generation with Domain Intelligence
  const generateStoryAcceptanceCriteria = (requirements) => {
    const criteria = [];
    
    requirements.forEach(req => {
      const reqLower = req.toLowerCase();
      
      // 📡 Telecom-Specific Acceptance Criteria
      if (reqLower.includes('catalog') || reqLower.includes('offer')) {
        criteria.push('Product catalog displays accurate pricing and feature information');
        criteria.push('Offer eligibility rules are properly validated');
      }
      if (reqLower.includes('kyc') || reqLower.includes('verification')) {
        criteria.push('KYC verification completes within regulatory timeframes');
        criteria.push('Identity validation meets telecom compliance standards');
      }
      if (reqLower.includes('sim') || reqLower.includes('esim') || reqLower.includes('activation')) {
        criteria.push('SIM/eSIM provisioning completes successfully');
        criteria.push('Service activation is verified and functional');
      }
      if (reqLower.includes('mnp') || reqLower.includes('portability')) {
        criteria.push('Number portability request is processed within TRAI timelines');
        criteria.push('Customer communication is sent at each MNP milestone');
      }
      if (reqLower.includes('billing') || reqLower.includes('charging') || reqLower.includes('rating')) {
        criteria.push('Real-time charging calculations are accurate');
        criteria.push('Billing data is generated and validated correctly');
      }
      if (reqLower.includes('payment') || reqLower.includes('collection')) {
        criteria.push('Payment processing supports multiple methods securely');
        criteria.push('Collection workflows handle failed payments appropriately');
      }
      if (reqLower.includes('care') || reqLower.includes('ticket') || reqLower.includes('support')) {
        criteria.push('Customer support tickets are created and tracked properly');
        criteria.push('Resolution workflows meet defined SLA requirements');
      }
      if (reqLower.includes('partner') || reqLower.includes('retailer') || reqLower.includes('commission')) {
        criteria.push('Partner transactions are recorded and commission calculated');
        criteria.push('Retailer portal provides accurate inventory and sales data');
      }
      if (reqLower.includes('analytics') || reqLower.includes('reporting') || reqLower.includes('compliance')) {
        criteria.push('Reports generate accurate data within specified timeframes');
        criteria.push('Regulatory compliance requirements are met and auditable');
      }
      
      // ✈️ Airline-Specific Acceptance Criteria
      if (reqLower.includes('flight') || reqLower.includes('booking') || reqLower.includes('reservation')) {
        criteria.push('Flight bookings are confirmed with valid PNR generation');
        criteria.push('Seat selection reflects real-time aircraft configuration');
      }
      if (reqLower.includes('check-in') || reqLower.includes('boarding')) {
        criteria.push('Check-in process completes within airline specified timeframes');
        criteria.push('Boarding passes are generated with valid barcode data');
      }
      if (reqLower.includes('baggage') || reqLower.includes('ancillary')) {
        criteria.push('Baggage policies are enforced according to airline rules');
        criteria.push('Ancillary services are priced and booked accurately');
      }
      if (reqLower.includes('schedule') || reqLower.includes('disruption') || reqLower.includes('delay')) {
        criteria.push('Schedule changes are communicated to passengers immediately');
        criteria.push('Disruption management follows IRROPS procedures');
      }
      if (reqLower.includes('fare') || reqLower.includes('pricing')) {
        criteria.push('Fare calculations include all taxes and fees correctly');
        criteria.push('Price validation ensures competitive and accurate pricing');
      }
      
      // 💰 Financial-Specific Acceptance Criteria
      if (reqLower.includes('portfolio') || reqLower.includes('investment')) {
        criteria.push('Portfolio allocations are calculated and displayed accurately');
        criteria.push('Investment transactions are processed within market hours');
      }
      if (reqLower.includes('risk') || reqLower.includes('assessment')) {
        criteria.push('Risk calculations follow established financial models');
        criteria.push('Risk tolerance assessment captures investor preferences');
      }
      if (reqLower.includes('form') || reqLower.includes('intake')) {
        criteria.push('Digital forms are completed with all required fields');
        criteria.push('Form validation prevents submission of incomplete data');
      }
      if (reqLower.includes('document') || reqLower.includes('upload')) {
        criteria.push('Documents are uploaded and verified successfully');
        criteria.push('Document storage complies with financial regulations');
      }
      if (reqLower.includes('screening') || reqLower.includes('check') || reqLower.includes('compliance')) {
        criteria.push('All compliance checks are completed successfully');
        criteria.push('Screening results are documented for audit purposes');
      }
      if (reqLower.includes('workflow') || reqLower.includes('approval')) {
        criteria.push('Approval workflows are followed correctly');
        criteria.push('Workflow status is visible to all stakeholders');
      }
      if (reqLower.includes('trading') || reqLower.includes('execution')) {
        criteria.push('Trade execution occurs at best available price');
        criteria.push('Trade confirmations are generated immediately');
      }
      
      // 🏥 Healthcare-Specific Acceptance Criteria
      if (reqLower.includes('patient') || reqLower.includes('medical record')) {
        criteria.push('Patient information is accurately captured and stored');
        criteria.push('Medical records are accessible to authorized providers only');
      }
      if (reqLower.includes('appointment') || reqLower.includes('scheduling')) {
        criteria.push('Appointments are scheduled without conflicts');
        criteria.push('Schedule changes are communicated to all parties');
      }
      if (reqLower.includes('prescription') || reqLower.includes('medication')) {
        criteria.push('Prescription validation checks for drug interactions');
        criteria.push('Medication dosage calculations are clinically accurate');
      }
      if (reqLower.includes('diagnosis') || reqLower.includes('clinical')) {
        criteria.push('Clinical data supports evidence-based decision making');
        criteria.push('Diagnostic codes follow ICD-10 standards');
      }
      if (reqLower.includes('insurance') || reqLower.includes('claim')) {
        criteria.push('Insurance verification occurs in real-time');
        criteria.push('Claims are submitted with complete required documentation');
      }
      if (reqLower.includes('consent') || reqLower.includes('privacy')) {
        criteria.push('Patient consent is documented and verifiable');
        criteria.push('Privacy controls comply with HIPAA requirements');
      }
      
      // 🛒 E-commerce-Specific Acceptance Criteria
      if (reqLower.includes('product') || reqLower.includes('catalog')) {
        criteria.push('Product information is accurate and up-to-date');
        criteria.push('Product search returns relevant results quickly');
      }
      if (reqLower.includes('cart') || reqLower.includes('checkout')) {
        criteria.push('Shopping cart maintains items across sessions');
        criteria.push('Checkout process is completed without errors');
      }
      if (reqLower.includes('inventory') || reqLower.includes('stock')) {
        criteria.push('Inventory levels are updated in real-time');
        criteria.push('Stock availability is accurately displayed');
      }
      if (reqLower.includes('order') || reqLower.includes('fulfillment')) {
        criteria.push('Orders are processed and confirmed immediately');
        criteria.push('Fulfillment status is tracked and communicated');
      }
      if (reqLower.includes('shipping') || reqLower.includes('delivery')) {
        criteria.push('Shipping calculations include all applicable fees');
        criteria.push('Delivery tracking information is accurate and current');
      }
      if (reqLower.includes('review') || reqLower.includes('rating')) {
        criteria.push('Customer reviews are moderated and published appropriately');
        criteria.push('Rating calculations reflect all customer feedback');
      }
      if (reqLower.includes('recommendation') || reqLower.includes('personalization')) {
        criteria.push('Product recommendations are relevant to customer preferences');
        criteria.push('Personalization respects customer privacy settings');
      }
      
      // 📈 Marketing-Specific Acceptance Criteria
      if (reqLower.includes('campaign') || reqLower.includes('promotion')) {
        criteria.push('Marketing campaigns are deployed according to schedule');
        criteria.push('Promotional offers are applied correctly at checkout');
      }
      if (reqLower.includes('segment') || reqLower.includes('audience')) {
        criteria.push('Customer segmentation criteria are applied accurately');
        criteria.push('Audience targeting respects opt-out preferences');
      }
      if (reqLower.includes('email') || reqLower.includes('notification')) {
        criteria.push('Email deliverability rates meet industry standards');
        criteria.push('Notification preferences are honored consistently');
      }
      if (reqLower.includes('analytics') || reqLower.includes('tracking')) {
        criteria.push('Analytics data is collected accurately and completely');
        criteria.push('Tracking implementation complies with privacy regulations');
      }
      if (reqLower.includes('lead') || reqLower.includes('conversion')) {
        criteria.push('Lead capture forms collect all required information');
        criteria.push('Conversion tracking attributes revenue to correct channels');
      }
      if (reqLower.includes('social') || reqLower.includes('engagement')) {
        criteria.push('Social media integration functions without errors');
        criteria.push('Engagement metrics are calculated and reported accurately');
      }
      if (reqLower.includes('ab test') || reqLower.includes('experiment')) {
        criteria.push('A/B tests are statistically valid and conclusive');
        criteria.push('Experimental results are documented and actionable');
      }
    });
    
    // 🎯 Smart Default Criteria Based on Requirement Complexity
    if (criteria.length === 0) {
      criteria.push('User can successfully complete the required functionality');
      criteria.push('System validates all inputs and provides feedback');
    }
    
    // 🚀 Universal Performance Criteria
    criteria.push('Performance meets acceptable standards');
    
    // 🧹 Remove duplicates and return most relevant criteria
    const uniqueCriteria = [...new Set(criteria)];
    return uniqueCriteria.slice(0, 4); // Limit to 4 criteria for readability
  };

  // Calculate story points based on complexity
  const calculateStoryPoints = (requirements) => {
    const complexity = requirements.join(' ').toLowerCase();
    
    if (complexity.includes('workflow') || complexity.includes('integration') || complexity.includes('screening')) {
      return 8; // Complex
    }
    if (complexity.includes('validation') || complexity.includes('approval') || complexity.includes('document')) {
      return 5; // Medium
    }
    return 3; // Simple
  };

  // Helper functions for story generation
  const groupRequirementsByFeature = (requirements) => {
    const groups = {};
    
    requirements.forEach(req => {
      let feature = 'Core System';
      
      if (req.text.toLowerCase().includes('user') || req.text.toLowerCase().includes('auth')) {
        feature = 'User Management';
      } else if (req.text.toLowerCase().includes('data') || req.text.toLowerCase().includes('process')) {
        feature = 'Data Processing';
      } else if (req.text.toLowerCase().includes('report') || req.text.toLowerCase().includes('analytic')) {
        feature = 'Reporting';
      } else if (req.section && req.section !== '') {
        feature = req.section;
      }
      
      if (!groups[feature]) groups[feature] = [];
      groups[feature].push(req);
    });
    
    return groups;
  };

  const determinePriority = (text) => {
    if (text.toLowerCase().includes('must') || text.toLowerCase().includes('critical')) return 'High';
    if (text.toLowerCase().includes('should') || text.toLowerCase().includes('important')) return 'Medium';
    return 'Low';
  };

  // 🤖 AI-Powered Contextual Validation Generation
  const generateAIContextualValidation = (domain, epicTitle, action, persona) => {
    const epicLower = epicTitle.toLowerCase();
    const actionLower = action.toLowerCase();
    const personaLower = persona.toLowerCase();
    const context = `${epicLower} ${actionLower} ${personaLower}`;
    
    console.log(`🎯 AI Context Analysis: domain=${domain}, context=${context}`);
    
    // 🎯 Enhanced Persona-Based Validation Logic
    // Analyze persona + action combination for contextual validation
    
    // Marketing/CRM Personas - Generate validation based on role and action
    if (personaLower.includes('marketing') || personaLower.includes('sales') || domain === 'marketing') {
      
      // Content Manager - Course/Content Management
      if (personaLower.includes('content') && (context.includes('course') || context.includes('content'))) {
        return [
          'Course content must be validated for accuracy and educational standards',
          'Content version control must track changes and approval workflow',
          'Learning objectives must be measurable and aligned with curriculum',
          'Content accessibility must comply with WCAG 2.1 guidelines',
          'Course prerequisites must be enforced before enrollment'
        ];
      }
      
      // Marketing Manager - Campaign and Strategy
      if (personaLower.includes('marketing manager') || (context.includes('classroom') || context.includes('campaign'))) {
        return [
          'Live session scheduling must prevent resource conflicts',
          'Attendance tracking must be accurate and real-time',
          'Interactive features (polls, Q&A) must support concurrent users',
          'Recording quality must meet minimum resolution and audio standards',
          'Breakout group assignments must be randomly distributed and balanced'
        ];
      }
      
      // Marketing Analyst - Analytics and Tracking
      if (personaLower.includes('analyst') || context.includes('analytics') || context.includes('tracking')) {
        return [
          'Learning progress tracking must capture detailed user interactions',
          'Recommendation algorithms must be based on learning patterns and preferences',
          'Certificate generation must validate course completion requirements',
          'Progress data must be exportable in standard reporting formats',
          'User onboarding flow must be optimized for conversion and retention'
        ];
      }
      
      // Generic Marketing Actions
      if (context.includes('lead') || context.includes('capture')) {
        return [
          'Lead capture forms must validate all required contact information fields',
          'Lead source attribution must be tracked accurately for campaign ROI',
          'Duplicate lead detection must prevent multiple entries for same contact',
          'Lead qualification scoring must be calculated consistently',
          'Lead routing to sales representatives must follow assignment rules'
        ];
      }
      
      if (context.includes('opportunity') || context.includes('pipeline')) {
        return [
          'Opportunity stage progression must follow defined sales workflow rules',
          'Pipeline value calculations must include probability weighting by stage',
          'Opportunity close date forecasting must be realistic and data-driven',
          'Win/loss reason tracking must be mandatory for closed opportunities',
          'Opportunity team assignments must maintain proper access controls'
        ];
      }
      
      if (context.includes('contact') || context.includes('customer')) {
        return [
          'Contact deduplication algorithms must prevent duplicate customer records',
          'Contact data synchronization must maintain referential integrity',
          'Customer communication preferences must be respected consistently',
          'Contact hierarchy relationships must be maintained accurately',
          'GDPR consent tracking must be documented for all customer interactions'
        ];
      }
    }
    
    // Healthcare Domain - Contextual Validation
    if (domain === 'healthcare') {
      if (context.includes('patient') || context.includes('registration')) {
        return [
          'Patient identity verification must prevent duplicate medical records',
          'Insurance eligibility must be validated in real-time before service',
          'Emergency contact information must be mandatory and accessible',
          'Medical history accuracy must be verified with patient confirmation',
          'HIPAA consent forms must be signed and dated before data collection'
        ];
      }
      if (context.includes('appointment') || context.includes('scheduling')) {
        return [
          'Appointment conflicts must be prevented through real-time availability checking',
          'Provider schedule changes must trigger automatic patient notifications',
          'Appointment reminders must respect patient communication preferences',
          'No-show tracking must be automated with configurable policies',
          'Emergency appointment slots must be reserved and accessible'
        ];
      }
      if (context.includes('medical') || context.includes('clinical')) {
        return [
          'Clinical data entry must follow standardized medical terminology',
          'Drug interaction checking must use current pharmaceutical databases',
          'Clinical decision support must provide evidence-based recommendations',
          'Medical coding must comply with ICD-10 and CPT standards',
          'Clinical alerts must be prioritized by severity and urgency'
        ];
      }
    }
    
    // E-commerce Domain - Contextual Validation
    if (domain === 'ecommerce') {
      if (context.includes('catalog') || context.includes('product')) {
        return [
          'Product information must be synchronized across all sales channels',
          'Inventory levels must be validated before allowing purchase',
          'Product images must be optimized for web and mobile viewing',
          'Price calculations must include all applicable taxes and fees',
          'Product recommendations must be personalized based on browsing history'
        ];
      }
      if (context.includes('cart') || context.includes('checkout')) {
        return [
          'Shopping cart persistence must maintain items for registered users',
          'Checkout process must support guest and registered user flows',
          'Payment validation must comply with PCI DSS security standards',
          'Shipping calculations must integrate with carrier APIs for accuracy',
          'Order confirmation must be sent immediately after successful payment'
        ];
      }
      if (context.includes('order') || context.includes('fulfillment')) {
        return [
          'Order status tracking must be updated in real-time throughout fulfillment',
          'Inventory allocation must be immediate upon order confirmation',
          'Shipping notifications must include tracking numbers and delivery estimates',
          'Order modifications must be allowed within defined time windows',
          'Return processing must follow automated workflow with status updates'
        ];
      }
    }
    
    // Banking/Financial Domain - Contextual Validation
    if (domain === 'banking' || domain === 'financial') {
      if (context.includes('transaction') || context.includes('payment')) {
        return [
          'Transaction authentication must use multi-factor verification',
          'Real-time fraud detection must analyze transaction patterns',
          'Currency conversion rates must be current and accurate',
          'Transaction limits must be enforced based on account type and history',
          'Settlement processing must comply with banking regulations'
        ];
      }
      if (context.includes('account') || context.includes('customer')) {
        return [
          'Account opening must include comprehensive KYC verification',
          'Credit scoring must use validated algorithms and current data',
          'Account statements must be generated accurately and on schedule',
          'Customer onboarding must be completed within regulatory timeframes',
          'Account closure must follow proper procedures and data retention'
        ];
      }
    }
    
    // 🎯 Enhanced Action-Based Validation for Unknown Domains
    // Generate contextual validation based on action and function
    
    if (actionLower.includes('manage') || actionLower.includes('primary')) {
      return [
        `${persona.split(' ')[0]} workflow must follow established business process standards`,
        'Data validation must ensure completeness and accuracy for all inputs',
        'User interface must provide clear navigation and intuitive controls',
        'Process automation must handle exceptions gracefully with proper error handling',
        'System performance must meet response time requirements for user satisfaction'
      ];
    }
    
    if (actionLower.includes('handle') || actionLower.includes('secondary')) {
      return [
        'Secondary operations must not interfere with primary business functions',
        'Background processing must be resilient to system interruptions',
        'Data consistency must be maintained across all related operations',
        'Error recovery must restore system state to known good condition',
        'Audit logging must capture all secondary operation activities'
      ];
    }
    
    if (context.includes('form') || context.includes('intake')) {
      return [
        'Form validation must provide real-time feedback for field-level errors',
        'Progressive disclosure must guide users through complex form processes',
        'Auto-save functionality must prevent data loss during form completion',
        'Accessibility features must support screen readers and keyboard navigation',
        'Form submission must include confirmation and next-step guidance'
      ];
    }
    
    console.log('⚠️ Using enhanced generic validation based on context');
    
    // Enhanced Fallback - Generate contextual validation from available context
    const baseActions = [
      'Input validation must ensure data integrity and business rule compliance',
      'User experience must be intuitive and support efficient task completion',
      'Error handling must provide clear guidance for problem resolution',
      'Security measures must protect sensitive information and prevent unauthorized access',
      'Performance optimization must deliver responsive user interactions'
    ];
    
    return baseActions;
    return []; // Return empty to trigger fallback
  };
  
  // 🤖 AI-Enhanced User Story Validation Criteria Generation
  const getStoryValidationCriteria = (domain, epicTitle, action, persona) => {
    console.log(`🤖 AI Validation Generator: domain=${domain}, epic=${epicTitle}, action=${action}, persona=${persona}`);
    
    // 🎯 AI-Generated Contextual Validation Criteria
    const contextualValidation = generateAIContextualValidation(domain, epicTitle, action, persona);
    if (contextualValidation.length > 0) {
      console.log(`✅ AI Generated ${contextualValidation.length} contextual validation criteria`);
      return contextualValidation;
    }
    
    // Fallback to enhanced domain-specific validation if AI generation unavailable
    const baseValidations = [
      'Input validation ensures data integrity and prevents malformed data entry',
      'Error handling provides clear, actionable feedback to users',
      'Security validation prevents unauthorized access and data breaches',
      'Performance validation ensures response times meet user expectations'
    ];

    const domainSpecificValidations = {
      telecom: [
        'Telecom regulatory compliance (TRAI/DoT) must be enforced for all operations',
        'Number portability (MNP) processing must complete within regulatory timeframes',
        'Real-time charging accuracy must be validated to prevent revenue leakage',
        'KYC validation must comply with telecom industry standards and DoT guidelines',
        'SIM/eSIM provisioning must follow secure activation protocols',
        'Billing accuracy must be verified with mediation and reconciliation processes',
        'Network integration APIs (HLR/HSS/OCS) must handle failover scenarios',
        'Tariff calculations must support complex rating rules and promotional offers',
        'Customer care SLA requirements must be monitored and enforced',
        'Partner commission calculations must be accurate and auditable',
        'Usage data collection must comply with privacy and data retention policies'
      ],
      airline: [
        'Flight data must comply with IATA standards and GDS protocols',
        'PNR creation and management must follow airline industry standards',
        'Payment processing must be PCI DSS compliant with 3DS authentication',
        'Ticket issuance must comply with IATA ticketing standards (ET/EMD)',
        'Fare calculations must include all taxes, fees, and carrier surcharges',
        'Schedule change handling must support IRROPS and disruption management',
        'Seat map integration must reflect real-time airline inventory',
        'Baggage policy validation must enforce airline-specific rules',
        'Ancillary service pricing must integrate with airline merchandising systems',
        'Airport code validation must use IATA/ICAO standards',
        'DCS integration must support real-time seat map and passenger data',
        'APIS data collection must comply with international travel requirements'
      ],
      financial: [
        'Financial calculations must be accurate to 4 decimal places',
        'Regulatory compliance (SEC, FINRA) requirements must be met',
        'Audit trails must be maintained for all financial transactions',
        'Risk assessment algorithms must be validated against historical data',
        'Real-time market data integration must have <2 second latency',
        'Portfolio valuation must be calculated using current market prices',
        'Transaction settlement must follow T+2 clearing standards',
        'Anti-money laundering (AML) checks must be performed on all transactions',
        'Credit risk assessments must use validated scoring models',
        'Margin calculations must include all applicable fees and haircuts',
        'Stress testing scenarios must be updated regularly with market conditions'
      ],
      marketing: [
        'Marketing campaign data must comply with GDPR and privacy regulations',
        'A/B testing results must be statistically significant (95% confidence)',
        'Customer segmentation algorithms must be validated for accuracy',
        'Email deliverability rates must maintain >95% success rate',
        'Analytics tracking must comply with cookie consent requirements',
        'Attribution modeling must account for multi-touch customer journeys',
        'Campaign ROI calculations must include all associated costs',
        'Lead scoring algorithms must be calibrated regularly for accuracy',
        'Social media API integrations must handle rate limiting gracefully',
        'Personalization engines must respect customer privacy preferences',
        'Marketing automation workflows must prevent message fatigue'
      ],
      healthcare: [
        'HIPAA compliance must be validated for all patient data handling',
        'Medical data accuracy must be verified against clinical standards',
        'Patient consent validation must be documented and traceable',
        'Clinical decision support must be evidence-based and validated',
        'Emergency access protocols must be tested and functional',
        'HL7 FHIR standards must be followed for healthcare data exchange',
        'Drug interaction checking must use current clinical databases',
        'Clinical coding must follow ICD-10 and CPT standards',
        'Patient matching algorithms must prevent duplicate records',
        'Clinical alerts must be prioritized based on severity levels',
        'Medical device integration must validate data accuracy and timing'
      ],
      ecommerce: [
        'Payment processing must comply with PCI DSS standards',
        'Inventory synchronization must be real-time across all channels',
        'Price calculations must include all applicable taxes and fees',
        'Shopping cart persistence must maintain data for 30 days',
        'Product recommendations must be validated for relevance and accuracy',
        'Search functionality must return results within 2 seconds',
        'Mobile checkout must support one-click purchasing options',
        'Fraud detection must analyze transaction patterns in real-time',
        'Product data must be synchronized across all sales channels',
        'Customer reviews must be moderated for authenticity',
        'Shipping calculations must integrate with carrier APIs for accuracy'
      ]
    };

    const actionSpecificValidations = {
      'Create and Manage': [
        'Data creation validation ensures all required fields are completed',
        'Duplicate detection prevents creation of redundant records',
        'Workflow approval processes must be tested and functional',
        'Data modification logging must capture who, what, when details'
      ],
      'View and Search': [
        'Search functionality must return relevant results within 2 seconds',
        'Filtering options must accurately narrow down result sets',
        'Pagination must handle large datasets efficiently',
        'Export functionality must maintain data formatting and integrity'
      ],
      'Update and Maintain': [
        'Version control must track all changes with rollback capability',
        'Concurrent editing must prevent data conflicts and loss',
        'Backup and recovery procedures must be tested regularly',
        'Change notifications must be sent to relevant stakeholders'
      ]
    };

    const personaSpecificValidations = {
      'Customer': [
        'User interface must be accessible and comply with WCAG 2.1 guidelines',
        'Mobile responsiveness must be tested across major device types',
        'Self-service capabilities must be intuitive and comprehensive'
      ],
      'Customer Service Representative': [
        'Agent tools must provide 360-degree customer view and interaction history',
        'Escalation workflows must be clearly defined and automated',
        'Knowledge base integration must provide contextual assistance'
      ],
      'Technical Support Agent': [
        'Diagnostic tools must provide real-time network and service status',
        'Trouble ticketing must integrate with network management systems',
        'Resolution tracking must measure first-call resolution rates'
      ],
      'Billing Specialist': [
        'Billing accuracy validation must prevent revenue leakage',
        'Dispute resolution workflows must be streamlined and auditable',
        'Payment processing must support multiple methods and currencies'
      ],
      'Channel Partner': [
        'Partner portal must provide real-time commission and sales tracking',
        'Inventory management must reflect accurate stock levels',
        'Training materials must be current and accessible'
      ],
      'Business Analyst': [
        'Analytics dashboards must provide drill-down capabilities',
        'Report generation must support scheduled and on-demand execution',
        'Data quality validation must ensure accuracy of insights'
      ],
      'Passenger': [
        'User interface must be intuitive for non-technical airline passengers',
        'Mobile responsiveness must support booking on all device types',
        'Accessibility must comply with disability access requirements (ADA)'
      ],
      'Travel Agent': [
        'Agent tools must support rapid multi-passenger bookings',
        'GDS integration must provide real-time fare and inventory access',
        'Commission tracking and reporting must be accurate and timely'
      ],
      'Airline Operations Staff': [
        'Operational tools must integrate with airline DCS and inventory systems',
        'IRROPS management must provide real-time disruption handling',
        'Queue management must support airline operational workflows'
      ],
      'Financial Analyst': [
        'Financial models must be validated against industry benchmarks',
        'Risk calculations must include stress testing scenarios'
      ],
      'Portfolio Manager': [
        'Portfolio rebalancing must consider transaction costs and tax implications',
        'Performance attribution must be calculated using industry standards'
      ],
      'Marketing Manager': [
        'Campaign ROI calculations must include all direct and indirect costs',
        'Brand compliance guidelines must be enforced across all content'
      ],
      'Healthcare Provider': [
        'Clinical protocols must be validated against current medical guidelines',
        'Patient safety alerts must be immediate and actionable'
      ]
    };

    // 🤖 AI-Enhanced Contextual Validation Generation
    // Combine validations based on context with intelligent selection
    let validations = [...baseValidations];
    
    // Add domain-specific validations (select most relevant based on epic context)
    if (domainSpecificValidations[domain]) {
      let domainValidations = domainSpecificValidations[domain];
      
      // 🎯 AI-style contextual filtering based on epic title and action for ALL domains
      if (domain === 'telecom') {
        if (epicTitle.toLowerCase().includes('billing') || epicTitle.toLowerCase().includes('charging')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('billing') || v.includes('charging') || v.includes('revenue') || v.includes('mediation')
          );
        } else if (epicTitle.toLowerCase().includes('onboarding') || epicTitle.toLowerCase().includes('activation')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('KYC') || v.includes('activation') || v.includes('provisioning') || v.includes('SIM')
          );
        } else if (epicTitle.toLowerCase().includes('care') || epicTitle.toLowerCase().includes('support')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('Customer care') || v.includes('SLA') || v.includes('resolution')
          );
        } else if (epicTitle.toLowerCase().includes('compliance') || epicTitle.toLowerCase().includes('analytics')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('regulatory') || v.includes('TRAI') || v.includes('privacy') || v.includes('audit')
          );
        }
      } else if (domain === 'airline') {
        if (epicTitle.toLowerCase().includes('booking') || epicTitle.toLowerCase().includes('reservation')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('PNR') || v.includes('booking') || v.includes('IATA') || v.includes('GDS')
          );
        } else if (epicTitle.toLowerCase().includes('payment') || epicTitle.toLowerCase().includes('fare')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('payment') || v.includes('PCI DSS') || v.includes('fare') || v.includes('pricing')
          );
        } else if (epicTitle.toLowerCase().includes('operation') || epicTitle.toLowerCase().includes('schedule')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('schedule') || v.includes('IRROPS') || v.includes('DCS') || v.includes('disruption')
          );
        } else if (epicTitle.toLowerCase().includes('service') || epicTitle.toLowerCase().includes('ancillary')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('ancillary') || v.includes('baggage') || v.includes('seat map') || v.includes('service')
          );
        }
      } else if (domain === 'financial') {
        if (epicTitle.toLowerCase().includes('portfolio') || epicTitle.toLowerCase().includes('investment')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('portfolio') || v.includes('market data') || v.includes('valuation') || v.includes('risk')
          );
        } else if (epicTitle.toLowerCase().includes('trading') || epicTitle.toLowerCase().includes('execution')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('settlement') || v.includes('transaction') || v.includes('margin') || v.includes('clearing')
          );
        } else if (epicTitle.toLowerCase().includes('compliance') || epicTitle.toLowerCase().includes('risk')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('compliance') || v.includes('audit') || v.includes('AML') || v.includes('regulatory')
          );
        } else if (epicTitle.toLowerCase().includes('calculation') || epicTitle.toLowerCase().includes('pricing')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('calculation') || v.includes('decimal places') || v.includes('accuracy') || v.includes('stress testing')
          );
        }
      } else if (domain === 'healthcare') {
        if (epicTitle.toLowerCase().includes('patient') || epicTitle.toLowerCase().includes('record')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('patient') || v.includes('HIPAA') || v.includes('consent') || v.includes('matching')
          );
        } else if (epicTitle.toLowerCase().includes('clinical') || epicTitle.toLowerCase().includes('medical')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('clinical') || v.includes('HL7') || v.includes('ICD-10') || v.includes('medical')
          );
        } else if (epicTitle.toLowerCase().includes('prescription') || epicTitle.toLowerCase().includes('drug')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('drug') || v.includes('interaction') || v.includes('medication') || v.includes('clinical')
          );
        } else if (epicTitle.toLowerCase().includes('emergency') || epicTitle.toLowerCase().includes('alert')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('emergency') || v.includes('alert') || v.includes('priority') || v.includes('clinical')
          );
        }
      } else if (domain === 'ecommerce') {
        if (epicTitle.toLowerCase().includes('product') || epicTitle.toLowerCase().includes('catalog')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('product') || v.includes('search') || v.includes('inventory') || v.includes('recommendation')
          );
        } else if (epicTitle.toLowerCase().includes('cart') || epicTitle.toLowerCase().includes('checkout')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('cart') || v.includes('checkout') || v.includes('payment') || v.includes('persistence')
          );
        } else if (epicTitle.toLowerCase().includes('order') || epicTitle.toLowerCase().includes('fulfillment')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('shipping') || v.includes('synchronization') || v.includes('fraud') || v.includes('carrier')
          );
        } else if (epicTitle.toLowerCase().includes('customer') || epicTitle.toLowerCase().includes('review')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('review') || v.includes('moderated') || v.includes('mobile') || v.includes('one-click')
          );
        }
      } else if (domain === 'marketing') {
        if (epicTitle.toLowerCase().includes('campaign') || epicTitle.toLowerCase().includes('promotion')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('campaign') || v.includes('ROI') || v.includes('GDPR') || v.includes('automation')
          );
        } else if (epicTitle.toLowerCase().includes('analytics') || epicTitle.toLowerCase().includes('tracking')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('analytics') || v.includes('tracking') || v.includes('attribution') || v.includes('cookie')
          );
        } else if (epicTitle.toLowerCase().includes('segment') || epicTitle.toLowerCase().includes('personalization')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('segmentation') || v.includes('personalization') || v.includes('privacy') || v.includes('lead scoring')
          );
        } else if (epicTitle.toLowerCase().includes('email') || epicTitle.toLowerCase().includes('social')) {
          domainValidations = domainValidations.filter(v => 
            v.includes('email') || v.includes('deliverability') || v.includes('social media') || v.includes('API')
          );
        }
      }
      
      validations = validations.concat(domainValidations.slice(0, 3));
    }
    
    // Add action-specific validations
    if (actionSpecificValidations[action]) {
      validations = validations.concat(actionSpecificValidations[action].slice(0, 2));
    }
    
    // Add persona-specific validations
    if (personaSpecificValidations[persona]) {
      validations = validations.concat(personaSpecificValidations[persona]);
    }
    
    // 🎯 AI-Enhanced Validation Prioritization
    // Remove duplicates and prioritize most relevant validations
    const uniqueValidations = [...new Set(validations)];
    
    // Return 5-7 most relevant validations with intelligent selection
    return uniqueValidations.slice(0, Math.min(7, uniqueValidations.length));
  };

  // Format requirements as EPICs for BRD
  const formatRequirementsAsEpics = (requirements, project, domain = null) => {
    if (!requirements || requirements.trim() === '') {
      return `<p><em>No specific requirements provided. Please add business requirements to see EPIC formatting.</em></p>`;
    }

    // Split requirements into lines and process each
    const lines = requirements.split('\n').map(line => line.trim()).filter(line => line);
    const epics = [];
    
    // Group related requirements into EPICs
    let currentEpic = [];
    let epicCount = 1;
    
    lines.forEach((line, index) => {
      // Start new EPIC every 2-3 requirements or when we detect a major section
      if (currentEpic.length >= 3 || 
          line.toLowerCase().includes('system') && currentEpic.length > 0 ||
          line.toLowerCase().includes('user') && currentEpic.length > 0) {
        
        if (currentEpic.length > 0) {
          epics.push({
            id: `EPIC-${String(epicCount).padStart(2, '0')}`,
            title: generateEpicTitle(currentEpic[0], domain),
            requirements: [...currentEpic]
          });
          epicCount++;
          currentEpic = [];
        }
      }
      
      currentEpic.push(line);
    });
    
    // Add the last epic if there are remaining requirements
    if (currentEpic.length > 0) {
      epics.push({
        id: `EPIC-${String(epicCount).padStart(2, '0')}`,
        title: generateEpicTitle(currentEpic[0], domain),
        requirements: [...currentEpic]
      });
    }
    
    // If no EPICs were created, create a default one
    if (epics.length === 0) {
      epics.push({
        id: 'EPIC-01',
        title: 'Core System Requirements',
        requirements: lines
      });
    }
    
    // Generate HTML for EPICs
    return epics.map(epic => `
      <div style="border:1px solid #d1d5db;margin:12px 0;padding:15px;border-radius:6px;background:#f8fafc;">
        <h3 style="color:#1f2937;margin-top:0;display:flex;align-items:center;">
          <span style="background:#3b82f6;color:white;padding:4px 8px;border-radius:4px;font-size:12px;margin-right:10px;">${epic.id}</span>
          ${epic.title}
        </h3>
        <div style="margin-top:10px;">
          <strong>Requirements:</strong>
          <ul style="margin-top:6px;">
            ${epic.requirements.map(req => `<li style="margin-bottom:4px;">${req}</li>`).join('')}
          </ul>
        </div>
        <div style="margin-top:10px;padding-top:8px;border-top:1px solid #e5e7eb;font-size:13px;color:#6b7280;">
          <strong>EPIC Status:</strong> Ready for FRD conversion | <strong>Priority:</strong> ${getEpicPriority(epic.requirements)}
        </div>
      </div>
    `).join('');
  };

  // Helper to generate EPIC titles
  // 🎯 Enhanced EPIC Title Generation with domain-specific intelligence
  const generateEpicTitle = (firstRequirement, domain = null) => {
    const req = firstRequirement.toLowerCase();
    
    // Domain-specific EPIC generation with contextual intelligence
    if (domain === 'telecom') {
      if (req.includes('subscriber') || req.includes('customer') || req.includes('onboard')) {
        return 'Customer Onboarding & Activation';
      }
      if (req.includes('billing') || req.includes('charging') || req.includes('payment')) {
        return 'Billing & Revenue Management';
      }
      if (req.includes('plan') || req.includes('service') || req.includes('catalog')) {
        return 'Service Catalog & Plan Management';
      }
      if (req.includes('care') || req.includes('support') || req.includes('ticket')) {
        return 'Customer Care & Support';
      }
      if (req.includes('compliance') || req.includes('regulatory') || req.includes('audit')) {
        return 'Regulatory Compliance & Analytics';
      }
    } else if (domain === 'airline') {
      if (req.includes('booking') || req.includes('reservation') || req.includes('search')) {
        return 'Flight Booking & Reservation';
      }
      if (req.includes('check') || req.includes('boarding') || req.includes('gate')) {
        return 'Check-in & Boarding Management';
      }
      if (req.includes('baggage') || req.includes('cargo') || req.includes('handling')) {
        return 'Baggage & Cargo Handling';
      }
      if (req.includes('schedule') || req.includes('operation') || req.includes('disruption')) {
        return 'Flight Operations & Schedule Management';
      }
      if (req.includes('loyalty') || req.includes('frequent') || req.includes('rewards')) {
        return 'Loyalty & Rewards Program';
      }
    } else if (domain === 'financial') {
      if (req.includes('portfolio') || req.includes('investment') || req.includes('allocation')) {
        return 'Portfolio & Investment Management';
      }
      if (req.includes('trading') || req.includes('execution') || req.includes('settlement')) {
        return 'Trading & Settlement Operations';
      }
      if (req.includes('risk') || req.includes('assessment') || req.includes('monitoring')) {
        return 'Risk Management & Assessment';
      }
      if (req.includes('compliance') || req.includes('regulatory') || req.includes('audit')) {
        return 'Regulatory Compliance & Reporting';
      }
      if (req.includes('client') || req.includes('onboard') || req.includes('kyc')) {
        return 'Client Onboarding & KYC';
      }
    } else if (domain === 'healthcare') {
      if (req.includes('patient') || req.includes('registration') || req.includes('intake')) {
        return 'Patient Registration & Management';
      }
      if (req.includes('appointment') || req.includes('schedule') || req.includes('booking')) {
        return 'Appointment Scheduling & Management';
      }
      if (req.includes('clinical') || req.includes('diagnosis') || req.includes('treatment')) {
        return 'Clinical Care & Treatment';
      }
      if (req.includes('prescription') || req.includes('medication') || req.includes('pharmacy')) {
        return 'Prescription & Medication Management';
      }
      if (req.includes('insurance') || req.includes('claim') || req.includes('billing')) {
        return 'Insurance & Billing Management';
      }
    } else if (domain === 'ecommerce') {
      if (req.includes('product') || req.includes('catalog') || req.includes('inventory')) {
        return 'Product Catalog & Inventory Management';
      }
      if (req.includes('cart') || req.includes('checkout') || req.includes('purchase')) {
        return 'Shopping Cart & Checkout Process';
      }
      if (req.includes('order') || req.includes('fulfillment') || req.includes('shipping')) {
        return 'Order Management & Fulfillment';
      }
      if (req.includes('customer') || req.includes('account') || req.includes('profile')) {
        return 'Customer Account & Profile Management';
      }
      if (req.includes('review') || req.includes('rating') || req.includes('feedback')) {
        return 'Reviews & Customer Feedback';
      }
    } else if (domain === 'marketing') {
      if (req.includes('campaign') || req.includes('promotion') || req.includes('advertisement')) {
        return 'Campaign & Promotion Management';
      }
      if (req.includes('lead') || req.includes('prospect') || req.includes('conversion')) {
        return 'Lead Generation & Conversion';
      }
      if (req.includes('segment') || req.includes('audience') || req.includes('targeting')) {
        return 'Audience Segmentation & Targeting';
      }
      if (req.includes('analytics') || req.includes('tracking') || req.includes('measurement')) {
        return 'Marketing Analytics & Performance Tracking';
      }
      if (req.includes('email') || req.includes('automation') || req.includes('workflow')) {
        return 'Email Marketing & Automation';
      }
    }
    
    // Generic EPIC generation (fallback)
    if (req.includes('user') || req.includes('auth') || req.includes('login')) {
      return 'User Management & Authentication';
    }
    if (req.includes('data') || req.includes('database') || req.includes('storage')) {
      return 'Data Management & Storage';
    }
    if (req.includes('report') || req.includes('analytic') || req.includes('dashboard')) {
      return 'Reporting & Analytics';
    }
    if (req.includes('payment') || req.includes('transaction') || req.includes('billing')) {
      return 'Payment & Transaction Processing';
    }
    if (req.includes('security') || req.includes('compliance') || req.includes('audit')) {
      return 'Security & Compliance';
    }
    if (req.includes('integration') || req.includes('api') || req.includes('external')) {
      return 'System Integration';
    }
    if (req.includes('performance') || req.includes('scalability') || req.includes('optimization')) {
      return 'Performance & Scalability';
    }
    
    return 'Core Business Requirements';
  };

  // Helper to determine EPIC priority
  const getEpicPriority = (requirements) => {
    const text = requirements.join(' ').toLowerCase();
    
    if (text.includes('critical') || text.includes('must') || text.includes('essential')) {
      return 'High';
    }
    if (text.includes('should') || text.includes('important') || text.includes('required')) {
      return 'Medium';
    }
    return 'Low';
  };

  const saveDocumentToProject = (project, docType, htmlContent, approved = false) => {
    setProjects((prev) => {
      const newPrev = { ...prev };
      const p = newPrev[project] || { name: project, documents: [] };
      const existingCount = p.documents.filter((d) => d.type === docType).length;
      const version = existingCount + 1;
      const doc = {
        id: `${docType.replace(/\s/g, "_")}_${Date.now()}`,
        type: docType,
        version,
        html: htmlContent,
        approved,
        createdAt: new Date().toISOString(),
      };
      p.documents = [...p.documents, doc];
      newPrev[project] = p;
      return newPrev;
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (user === "kmadhukumar25@gmail.com" && pass === "Madhu143") {
      setMsg("Login successful.");
      setIsLoggedIn(true);
    } else {
      setMsg("Invalid credentials.");
    }
  };

  const handleAddProject = () => {
    setProjectName("");
    setSavedProjectName("");
    setDocumentGenerator("");
    setSelectedModule(MODULES[0]);
    setIsCreatingProject(true);
    setSelectedSearchProject("");
    setSearchTerm("");
  };

  const handleSaveProject = () => {
    if (!projectName.trim()) {
      setMsg("Please enter a project name.");
      setTimeout(() => setMsg(""), 2500);
      return;
    }
    const name = projectName.trim();
    setSavedProjectName(name);
    setProjects((prev) => {
      if (prev[name]) return prev;
      return { ...prev, [name]: { name, documents: [] } };
    });
    setMsg("Project saved.");
    setTimeout(() => setMsg(""), 1500);
  };

  const handleCancelCreate = () => {
    setIsCreatingProject(false);
  };

  const handleCompleteProject = () => {
    setCompletedProjects((c) => Math.min(c + 1, totalProjects));
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setIsCreatingProject(false);
    setUser("");
    setPass("");
    setMsg("");
    setProjectName("");
    setSavedProjectName("");
    setDocumentGenerator("");
    setSelectedSearchProject("");
    setSearchTerm("");
  };

  // STANDALONE MODE: Use enhanced local template with AI domain detection only
  const handleBrdSubmit = async () => {
    if (!savedProjectName) {
      setMsg("Please save project name first.");
      setTimeout(() => setMsg(""), 2000);
      return;
    }
    const project = savedProjectName;
    const version =
      (projects[project]?.documents?.filter((d) => d.type === "BRD")?.length || 0) + 1;

    setMsg("Generating BRD with AI domain detection...");
    
    // FORCE STANDALONE MODE - Always use enhanced local template
    console.log("🚀 STANDALONE MODE: Using enhanced local template with AI domain detection");
    const html = generateBrdHtml({ project, inputs: brdInputs, version });
    
    saveDocumentToProject(project, "BRD", html, false);
    setBrdPreviewHtml(html);
    setBrdPreviewVersion(version);
    setBrdPreviewVisible(true);
    setMsg(`Enhanced BRD Version-${version} generated with AI domain detection.`);
    setTimeout(() => setMsg(""), 3000);
  };

  // New FRD generation function using AI agents
  // STANDALONE FRD GENERATION - No backend dependency
  const handleFrdSubmit = async () => {
    if (!savedProjectName) {
      setMsg("Please save project name first.");
      setTimeout(() => setMsg(""), 2000);
      return;
    }
    
    if (!frdInputs.brdText.trim()) {
      setMsg("Please provide BRD content for FRD generation.");
      setTimeout(() => setMsg(""), 2000);
      return;
    }

    const project = savedProjectName;
    const version =
      (projects[project]?.documents?.filter((d) => d.type === "FRD")?.length || 0) + 1;

    setFrdLoading(true);
    setMsg("🤖 Generating FRD with AI domain intelligence...");
    
    // STANDALONE MODE - Generate FRD locally
    console.log("🚀 FRD STANDALONE MODE: Converting BRD to FRD with domain intelligence");
    
    const html = generateFrdFromBrd(frdInputs.brdText.trim(), project, version);
    
    saveDocumentToProject(project, "FRD", html, false);
    setFrdPreviewHtml(html);
    setFrdPreviewVersion(version);
    setFrdPreviewVisible(true);
    setMsg(`Enhanced FRD Version-${version} generated successfully!`);
    setTimeout(() => setMsg(""), 3000);
    
    setFrdLoading(false);
  };

  const handleBrdApprove = (project) => {
    setProjects((prev) => {
      const copy = { ...prev };
      const p = copy[project];
      if (!p) return prev;
      const brds = p.documents.filter((d) => d.type === "BRD");
      if (!brds.length) return prev;
      const latest = brds.reduce((a, b) => (a.version > b.version ? a : b));
      latest.approved = true;
      return copy;
    });
    setMsg("BRD approved.");
    setTimeout(() => setMsg(""), 1500);
  };

  const handleFrdApprove = (project) => {
    setProjects((prev) => {
      const copy = { ...prev };
      const p = copy[project];
      if (!p) return prev;
      const frds = p.documents.filter((d) => d.type === "FRD");
      if (!frds.length) return prev;
      const latest = frds.reduce((a, b) => (a.version > b.version ? a : b));
      latest.approved = true;
      return copy;
    });
    setMsg("FRD approved.");
    setTimeout(() => setMsg(""), 1500);
  };

  const handleBrdClear = () => {
    setBrdInputs({
      scope: "",
      objectives: "",
      budget: "",
      briefRequirements: "",
      assumptions: "",
      constraints: "",
      validations: "",
    });
    setMsg("BRD input cleared.");
    setTimeout(() => setMsg(""), 1000);
  };

  const handleFrdClear = () => {
    setFrdInputs({
      brdText: "",
    });
    setFrdPreviewHtml("");
    setFrdPreviewVisible(false);
    setMsg("FRD input cleared.");
    setTimeout(() => setMsg(""), 1000);
  };

  const loadSampleHealthcareBRD = () => {
    const sampleBRD = `Executive Summary
Health Care BRD: Ability to create and manage patient profiles, schedule appointments with notifications, store and update patient medical history securely, and generate invoices with insurance claim support.

Project Scope
Included – Patient registration, appointment scheduling, electronic health records integration, billing module. Excluded – Telemedicine services, AI diagnostic tools, integration with third-party pharmacies.

Business Objectives
Reduce manual customer support inquiries related to balances and statements.
Improve payment straight-through-processing and reduce failed transactions.

Budget Details
Estimated project budget of $500K–$750K, covering development, testing, deployment, and first-year maintenance.

Business Requirements
The system shall ability to create.
The system shall manage patient profiles.
The system shall schedule appointments with notifications.
The system shall store.
The system shall update patient medical history securely.
The system shall generate invoices with insurance claim support.
The system shall included – Patient registration.
The system shall appointment scheduling.
The system shall electronic health records integration.
The system shall billing module. Excluded – Telemedicine services.
The system shall aI diagnostic tools.
The system shall integration with third-party pharmacies.
The system shall improve patient management efficiency.
The system shall streamline appointment scheduling.
The system shall provide centralized health records.
The system shall enhance billing accuracy.

Assumptions
Integration with existing hospital systems is feasible.
Staff training will be provided.
Compliance requirements are well-defined.

Validations
Patient data must be validated for completeness.
Appointment conflicts must be prevented.
Billing calculations must be accurate.
Security protocols must be enforced.`;

    setFormData({ 
      projectScope: "Included – Patient registration, appointment scheduling, electronic health records integration, billing module. Excluded – Telemedicine services, AI diagnostic tools, integration with third-party pharmacies.",
      businessObjectives: "Reduce manual customer support inquiries related to balances and statements. Improve payment straight-through-processing and reduce failed transactions.",
      budgetDetails: "Estimated project budget of $500K–$750K, covering development, testing, deployment, and first-year maintenance.",
      briefRequirements: sampleBRD,
      assumptions: "Integration with existing hospital systems is feasible. Staff training will be provided. Compliance requirements are well-defined.",
      validations: "Patient data must be validated for completeness. Appointment conflicts must be prevented. Billing calculations must be accurate. Security protocols must be enforced."
    });
    
    // Also update FRD inputs for FRD Creation page
    setFrdInputs({
      brdText: sampleBRD
    });
    
    setMsg("Sample Healthcare BRD loaded successfully!");
    setTimeout(() => setMsg(""), 2000);
  };

  const loadSampleEcommerceBRD = () => {
    const sampleBRD = `Project Scope (Included & Excluded): Included — product catalog and search, cart and checkout, payments, shipping/rates, order management, returns/refunds, promotions/coupons, customer accounts, admin CMS, and analytics; Excluded — marketplace multi‑vendor onboarding, in‑store POS integration, warehouse robotics, and cross‑border tax automation at launch.

Business Objectives: Increase online revenue and conversion rate, reduce cart abandonment, improve repeat purchase rate/CLV, shorten fulfillment lead time, and decrease payment failures and support tickets.

Budget Details: Estimated ₹80–₹140 lakh for design/build, platform licenses, integrations (payment, shipping, tax), testing, deployment, observability, and first‑year run/support; phased MVP then growth epics.

Brief Business Requirements (EPICs):

EPIC-01 Catalog & Discovery: browse, filter, search, SEO, rich PDP content.

EPIC-02 Cart & Checkout: guest/login checkout, address book, taxes, shipping options, order review.

EPIC-03 Payments: cards/UPI/wallets/BNPL, 3DS, retries, refunds.

EPIC-04 Orders & Fulfillment: order creation, split shipments, tracking, cancellations/returns.

EPIC-05 Promotions & Pricing: coupons, discounts, gift cards, price rules.

EPIC-06 Accounts & Loyalty: registration/SSO, profiles, wishlists, loyalty points.

EPIC-07 Admin & Content: product/inventory/pricing management, CMS, role‑based access, approvals.

EPIC-08 Analytics & Reporting: conversion funnel, sales/returns, campaign attribution.

Assumptions: Product, price, and inventory are available via API or scheduled feeds; payment/shipping accounts are provisioned; tax/returns/privacy policies are approved; non‑prod and prod environments with SSO/CDN exist; SLA for upstream systems meets storefront needs.

Validations: Required customer/address fields; email/phone formats; postal code and tax/VAT rules by region; inventory reservation at checkout; payment authorization and risk checks; coupon eligibility/stacking rules; shipment method/address compatibility; hard limits on order value/quantity to prevent abuse.`;

    setFormData({ 
      projectScope: "Included — product catalog and search, cart and checkout, payments, shipping/rates, order management, returns/refunds, promotions/coupons, customer accounts, admin CMS, and analytics; Excluded — marketplace multi‑vendor onboarding, in‑store POS integration, warehouse robotics, and cross‑border tax automation at launch.",
      businessObjectives: "Increase online revenue and conversion rate, reduce cart abandonment, improve repeat purchase rate/CLV, shorten fulfillment lead time, and decrease payment failures and support tickets.",
      budgetDetails: "Estimated ₹80–₹140 lakh for design/build, platform licenses, integrations (payment, shipping, tax), testing, deployment, observability, and first‑year run/support; phased MVP then growth epics.",
      briefRequirements: sampleBRD,
      assumptions: "Product, price, and inventory are available via API or scheduled feeds; payment/shipping accounts are provisioned; tax/returns/privacy policies are approved; non‑prod and prod environments with SSO/CDN exist; SLA for upstream systems meets storefront needs.",
      validations: "Required customer/address fields; email/phone formats; postal code and tax/VAT rules by region; inventory reservation at checkout; payment authorization and risk checks; coupon eligibility/stacking rules; shipment method/address compatibility; hard limits on order value/quantity to prevent abuse."
    });
    
    // Also update FRD inputs for FRD Creation page
    setFrdInputs({
      brdText: sampleBRD
    });
    
    setMsg("Sample E-commerce BRD with EPICs loaded successfully!");
    setTimeout(() => setMsg(""), 2000);
  };

  const handleDownloadDoc = (project, doc) => {
    const filename = `${project}_BRD_v${doc.version}.doc`;
    downloadAsWord(doc.html, filename);
  };

  const handleSearch = () => {
    if (!searchTerm.trim()) {
      setMsg("Enter project name to search.");
      setTimeout(() => setMsg(""), 1500);
      return;
    }
    const found = Object.keys(projects).find(
      (k) => k.toLowerCase() === searchTerm.trim().toLowerCase()
    );
    if (!found) {
      setMsg("Project not found.");
      setTimeout(() => setMsg(""), 1500);
      return;
    }
    
    // Initialize sample documents for demonstration if project exists but has no documents
    if (found && (!projects[found]?.documents || projects[found]?.documents.length === 0)) {
      initializeSampleDocuments(found);
    }
    
    setSelectedSearchProject(found);

    if (isCreatingProject) {
      setSavedProjectName(found);
      setProjectName(found);
      setDocumentGenerator("");
      setMsg(`Loaded project "${found}" into workspace.`);
      setTimeout(() => setMsg(""), 1400);
    }
  };

  // Function to initialize sample documents for demonstration
  const initializeSampleDocuments = (projectName) => {
    const sampleDocs = [
      {
        id: `BRD_${Date.now()}_1`,
        type: "BRD",
        version: 1,
        html: `<h1>Business Requirements Document V1 - ${projectName}</h1><p>Sample BRD content...</p>`,
        approved: true,
        createdAt: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
      },
      {
        id: `BRD_${Date.now()}_2`,
        type: "BRD", 
        version: 2,
        html: `<h1>Business Requirements Document V2 - ${projectName}</h1><p>Updated BRD content...</p>`,
        approved: true,
        createdAt: new Date(Date.now() - 43200000).toISOString(), // 12 hours ago
      },
      {
        id: `FRD_${Date.now()}_1`,
        type: "FRD",
        version: 1,
        html: `<h1>Functional Requirements Document V1 - ${projectName}</h1><p>Sample FRD content...</p>`,
        approved: true,
        createdAt: new Date(Date.now() - 21600000).toISOString(), // 6 hours ago
      },
      {
        id: `SRS_${Date.now()}_1`,
        type: "SRS",
        version: 1,
        html: `<h1>Software Requirements Specification V1 - ${projectName}</h1><p>Sample SRS content...</p>`,
        approved: false,
        createdAt: new Date(Date.now() - 10800000).toISOString(), // 3 hours ago
      },
      {
        id: `Impact_${Date.now()}_1`,
        type: "Impact Analysis",
        version: 1,
        html: `<h1>Impact Analysis V1 - ${projectName}</h1><p>Sample Impact Analysis content...</p>`,
        approved: true,
        createdAt: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
      },
      {
        id: `Wireframe_${Date.now()}_1`,
        type: "Wireframe",
        version: 1,
        html: `<h1>Wireframe V1 - ${projectName}</h1><p>Sample Wireframe content...</p>`,
        approved: true,
        createdAt: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
      }
    ];

    setProjects((prev) => ({
      ...prev,
      [projectName]: {
        name: projectName,
        documents: sampleDocs
      }
    }));
  };

  const pageStyle = {
    minHeight: "100vh",
    background: "#f4f6f8",
    padding: 28,
    fontFamily: "Inter, Roboto, Arial, sans-serif",
  };

  const cardStyle = {
    background: "#ffffff",
    padding: 24,
    borderRadius: 12,
    boxShadow: "0 8px 28px rgba(16,24,40,0.08)",
    color: "#111827",
  };

  const inputStyle = {
    display: "block",
    width: "100%",
    padding: "10px 12px",
    margin: "8px 0 16px",
    borderRadius: 8,
    border: "1px solid #e6e9ef",
    fontSize: 14,
    outline: "none",
  };

  const topButton = {
    background: "#0f172a",
    color: "#fff",
    border: "none",
    padding: "8px 14px",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: 600,
  };

  if (!isLoggedIn) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(180deg,#f5f7fa 0%,#eef2f6 100%)", padding: 24 }}>
        <div style={{ ...cardStyle, width: 420, padding: 32 }}>
          <h1 style={{ margin: 0, fontSize: 20 }}>BA Assistant Tool</h1>
          <p style={{ marginTop: 8, marginBottom: 20, color: "#6b7280", fontSize: 13 }}>Sign in to continue</p>

          <form onSubmit={handleSubmit} aria-label="login form">
            <label style={{ fontSize: 13, color: "#374151", fontWeight: 600 }}>
              Email
              <input style={inputStyle} value={user} onChange={(e) => setUser(e.target.value)} placeholder="name@company.com" type="email" required />
            </label>

            <label style={{ fontSize: 13, color: "#374151", fontWeight: 600 }}>
              Password
              <input type="password" style={inputStyle} value={pass} onChange={(e) => setPass(e.target.value)} placeholder="Enter your password" required />
            </label>

            <button type="submit" style={{ ...topButton, width: "100%" }}>Sign in</button>
          </form>

          {msg && <p style={{ marginTop: 16, color: msg.includes("successful") ? "#059669" : "#dc2626" }}>{msg}</p>}
        </div>
      </div>
    );
  }

  if (isCreatingProject) {
    return (
      <div style={{ minHeight: "100vh", background: "#f4f6f8", padding: 20, fontFamily: "Inter, Roboto, Arial, sans-serif" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", display: "flex", gap: 24 }}>
          <aside style={{ width: 280 }}>
            <div style={{ background: "#fff", borderRadius: 12, padding: 18, boxShadow: "0 6px 18px rgba(16,24,40,0.06)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <div style={{ fontWeight: 700 }}>Modules</div>
                <button onClick={() => setIsCreatingProject(false)} style={{ background: "transparent", border: "none", cursor: "pointer", color: "#6b7280" }}>Close</button>
              </div>

              <nav>
                {MODULES.map((m) => (
                  <div key={m} onClick={() => setSelectedModule(m)} style={{ padding: "10px 12px", borderRadius: 8, cursor: "pointer", marginBottom: 8, background: selectedModule === m ? "#0f172a" : "transparent", color: selectedModule === m ? "#fff" : "#111827", fontWeight: selectedModule === m ? 700 : 600 }}>
                    {m}
                  </div>
                ))}
              </nav>
            </div>
          </aside>

          <main style={{ flex: 1 }}>
            <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 6px 18px rgba(16,24,40,0.06)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <div>
                  <button onClick={() => setIsCreatingProject(false)} aria-label="Back to dashboard" style={{ background: "transparent", border: "none", cursor: "pointer", fontSize: 18 }}>←</button>
                </div>

                <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                  <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project Name" style={{ ...inputStyle, width: 260, margin: 0 }} />
                  <button onClick={handleSaveProject} style={{ ...topButton, padding: "8px 12px" }}>Save</button>

                  <input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Search Project" style={{ ...inputStyle, width: 200, margin: 0 }} />
                  <button onClick={handleSearch} style={{ ...topButton, padding: "8px 12px" }}>Search</button>

                  <button onClick={handleLogout} style={{ background: "transparent", border: "1px solid #e6e9ef", padding: "8px 12px", borderRadius: 8, cursor: "pointer" }}>Logout</button>
                </div>
              </div>

              <div>
                <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 600 }}>Project</div>
                <div style={{ marginTop: 6, fontSize: 18, fontWeight: 700, color: "#0f172a" }}>{savedProjectName || "No project saved yet"}</div>
              </div>

              <section style={{ marginTop: 12, color: "#374151" }}>
                <label style={{ display: "block", fontSize: 13, color: "#374151", marginBottom: 8 }}>Document Generator</label>
                <select value={documentGenerator} onChange={(e) => setDocumentGenerator(e.target.value)} style={{ ...inputStyle, padding: "10px 12px", width: 360 }}>
                  <option value="">Select document</option>
                  {DOC_OPTIONS.map((d) => <option key={d} value={d}>{d}</option>)}
                </select>

                {documentGenerator === "FRD Creation" && (
                  <div style={{ marginTop: 18 }}>
                    <div style={{ marginBottom: 16, padding: 16, background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 8 }}>
                      <h4 style={{ margin: "0 0 8px 0", color: "#374151" }}>🤖 AI-Powered FRD Generation</h4>
                      <p style={{ margin: 0, color: "#6b7280", fontSize: 14 }}>
                        Our AI agents analyze your Business Requirements Document (BRD) and automatically generate a comprehensive 
                        Functional Requirements Document (FRD) with domain-specific details, stakeholders, NFRs, and detailed functional requirements.
                      </p>
                    </div>

                    <div style={{ marginBottom: 8, fontWeight: 700 }}>FRD Generation - Input BRD</div>
                    <p style={{ color: "#6b7280", fontSize: 13, marginBottom: 12 }}>
                      Paste your complete Business Requirements Document below. The AI agent will automatically detect the domain 
                      (Healthcare, Banking, E-commerce, etc.) and generate appropriate FRD content.
                    </p>

                    <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
                      <button 
                        onClick={loadSampleHealthcareBRD} 
                        style={{ 
                          padding: "8px 12px", 
                          background: "#10b981", 
                          color: "white", 
                          border: "none", 
                          borderRadius: 6,
                          cursor: "pointer",
                          fontSize: 13
                        }}
                      >
                        Load Healthcare Sample
                      </button>
                      <button 
                        onClick={loadSampleEcommerceBRD} 
                        style={{ 
                          padding: "8px 12px", 
                          background: "#3b82f6", 
                          color: "white", 
                          border: "none", 
                          borderRadius: 6,
                          cursor: "pointer",
                          fontSize: 13
                        }}
                      >
                        Load E-commerce EPICs Sample
                      </button>
                      <button 
                        onClick={handleFrdClear} 
                        style={{ 
                          padding: "8px 12px", 
                          background: "#6b7280", 
                          color: "white", 
                          border: "none", 
                          borderRadius: 6,
                          cursor: "pointer",
                          fontSize: 13
                        }}
                      >
                        Clear Input
                      </button>
                    </div>

                    <label style={{ fontWeight: 600 }}>Business Requirements Document (BRD) Content</label>
                    <textarea 
                      value={frdInputs.brdText} 
                      onChange={(e) => updateFrdInput("brdText", e.target.value)} 
                      placeholder="Paste your complete BRD here including:
• Executive Summary
• Project Scope
• Business Objectives  
• Budget Details
• Business Requirements
• Assumptions
• Constraints
• Validations & Acceptance Criteria

The AI agent will analyze this content and generate a comprehensive FRD."
                      style={{ 
                        ...inputStyle, 
                        minHeight: 280,
                        fontFamily: "monospace",
                        fontSize: 13
                      }} 
                    />
                    <div style={{ fontSize: 12, color: "#6b7280", marginTop: 4, marginBottom: 16 }}>
                      Characters: {frdInputs.brdText.length} | AI works best with detailed, structured BRDs
                    </div>

                    <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
                      <button 
                        onClick={handleFrdSubmit} 
                        disabled={frdLoading}
                        style={{ 
                          ...topButton, 
                          background: frdLoading ? "#9ca3af" : "#3b82f6",
                          cursor: frdLoading ? "not-allowed" : "pointer"
                        }}
                      >
                        {frdLoading ? "🤖 AI Agent Processing..." : "🚀 Generate FRD"}
                      </button>
                      <button 
                        onClick={() => { 
                          if (savedProjectName) handleFrdApprove(savedProjectName); 
                          else setMsg("Save project first to approve."); 
                        }} 
                        style={{ 
                          background: "#047857", 
                          color: "#fff", 
                          border: "none", 
                          padding: "8px 14px", 
                          borderRadius: 8 
                        }}
                      >
                        APPROVE
                      </button>
                      <button 
                        onClick={handleFrdClear} 
                        style={{ 
                          background: "#ef4444", 
                          color: "#fff", 
                          border: "none", 
                          padding: "8px 14px", 
                          borderRadius: 8 
                        }}
                      >
                        CLEAR
                      </button>
                    </div>

                    {frdPreviewVisible && (
                      <div style={{ marginTop: 16, border: "1px solid #e6e9ef", borderRadius: 8, overflow: "hidden", background: "#fff" }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", borderBottom: "1px solid #eef2f6", background: "#f8fafc" }}>
                          <div style={{ fontWeight: 700 }}>🤖 AI-Generated FRD — Version {frdPreviewVersion}</div>
                          <div style={{ display: "flex", gap: 8 }}>
                            <button 
                              onClick={() => downloadAsWord(frdPreviewHtml, `${savedProjectName}_FRD_v${frdPreviewVersion}.doc`)} 
                              style={{ 
                                padding: "6px 10px", 
                                borderRadius: 6, 
                                background: "#fff", 
                                border: "1px solid #e6e9ef", 
                                cursor: "pointer" 
                              }}
                            >
                              Download
                            </button>
                            <button 
                              onClick={() => { 
                                if (savedProjectName) handleFrdApprove(savedProjectName); 
                                else setMsg("Save project first to approve."); 
                              }} 
                              style={{ 
                                padding: "6px 10px", 
                                borderRadius: 6, 
                                background: "#047857", 
                                color: "#fff", 
                                border: "none", 
                                cursor: "pointer" 
                              }}
                            >
                              Approve
                            </button>
                            <button 
                              onClick={closeFrdPreview} 
                              style={{ 
                                padding: "6px 10px", 
                                borderRadius: 6, 
                                background: "#ef4444", 
                                color: "#fff", 
                                border: "none", 
                                cursor: "pointer" 
                              }}
                            >
                              Close Preview
                            </button>
                          </div>
                        </div>
                        <div style={{ padding: 16, maxHeight: 500, overflow: "auto" }}>
                          <div dangerouslySetInnerHTML={{ __html: frdPreviewHtml }} />
                        </div>
                      </div>
                    )}

                    {/* Wireframe Generator Integration */}
                    {frdPreviewHtml && (
                      <div style={{ marginTop: 24 }}>
                        <WireframeGenerator
                          projectName={savedProjectName}
                          frdContent={frdPreviewHtml}
                          onWireframeGenerated={(html, domain) => {
                            console.log('Wireframes generated for project:', savedProjectName);
                            setMsg(`✅ Wireframes generated successfully for ${domain} domain!`);
                            setTimeout(() => setMsg(""), 3000);
                          }}
                        />
                      </div>
                    )}
                  </div>
                )}

                {documentGenerator === "BRD Creation" && (
                  <div style={{ marginTop: 18 }}>
                    <div style={{ marginBottom: 8, fontWeight: 700 }}>BRD - Inputs</div>

                    <label style={{ fontWeight: 600 }}>Project Scope Included / Excluded</label>
                    <textarea value={brdInputs.scope} onChange={(e) => updateBrdInput("scope", e.target.value)} style={{ ...inputStyle, minHeight: 80 }} />

                    <label style={{ fontWeight: 600 }}>Business Objectives</label>
                    <textarea value={brdInputs.objectives} onChange={(e) => updateBrdInput("objectives", e.target.value)} style={{ ...inputStyle, minHeight: 80 }} />

                    <label style={{ fontWeight: 600 }}>Budget Details</label>
                    <textarea value={brdInputs.budget} onChange={(e) => updateBrdInput("budget", e.target.value)} style={{ ...inputStyle }} />

                    <label style={{ fontWeight: 600 }}>Brief Business Requirements</label>
                    <textarea value={brdInputs.briefRequirements} onChange={(e) => updateBrdInput("briefRequirements", e.target.value)} style={{ ...inputStyle, minHeight: 80 }} />

                    <label style={{ fontWeight: 600 }}>Assumptions</label>
                    <textarea value={brdInputs.assumptions} onChange={(e) => updateBrdInput("assumptions", e.target.value)} style={{ ...inputStyle }} />

                    <label style={{ fontWeight: 600 }}>Constraints</label>
                    <textarea value={brdInputs.constraints} onChange={(e) => updateBrdInput("constraints", e.target.value)} style={{ ...inputStyle }} />

                    <label style={{ fontWeight: 600 }}>Validations / Acceptance Criteria</label>
                    <textarea value={brdInputs.validations} onChange={(e) => updateBrdInput("validations", e.target.value)} style={{ ...inputStyle, minHeight: 80 }} />

                    <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
                      <button onClick={handleBrdSubmit} style={{ ...topButton }}>SUBMIT</button>
                      <button onClick={() => { if (savedProjectName) handleBrdApprove(savedProjectName); else setMsg("Save project first to approve."); }} style={{ background: "#047857", color: "#fff", border: "none", padding: "8px 14px", borderRadius: 8 }}>APPROVE</button>
                      <button onClick={handleBrdClear} style={{ background: "#ef4444", color: "#fff", border: "none", padding: "8px 14px", borderRadius: 8 }}>CLEAR</button>
                    </div>

                    {brdPreviewVisible && (
                      <div style={{ marginTop: 16, border: "1px solid #e6e9ef", borderRadius: 8, overflow: "hidden", background: "#fff" }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", borderBottom: "1px solid #eef2f6" }}>
                          <div style={{ fontWeight: 700 }}>BRD Preview — Version {brdPreviewVersion}</div>
                          <div style={{ display: "flex", gap: 8 }}>
                            <button onClick={() => downloadAsWord(brdPreviewHtml, `${savedProjectName}_BRD_v${brdPreviewVersion}.doc`)} style={{ padding: "6px 10px", borderRadius: 6, background: "#fff", border: "1px solid #e6e9ef", cursor: "pointer" }}>Download</button>
                            <button onClick={() => { if (savedProjectName) handleBrdApprove(savedProjectName); else setMsg("Save project first to approve."); }} style={{ padding: "6px 10px", borderRadius: 6, background: "#047857", color: "#fff", border: "none", cursor: "pointer" }}>Approve</button>
                            <button onClick={closeBrdPreview} style={{ padding: "6px 10px", borderRadius: 6, background: "#ef4444", color: "#fff", border: "none", cursor: "pointer" }}>Close Preview</button>
                          </div>
                        </div>
                        <div style={{ padding: 16, maxHeight: 420, overflow: "auto" }}>
                          <div dangerouslySetInnerHTML={{ __html: brdPreviewHtml }} />
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {documentGenerator === "Wire Frame Generator" && (
                  <div style={{ marginTop: 18 }}>
                    <div style={{ marginBottom: 16, padding: 16, background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 8 }}>
                      <h4 style={{ margin: "0 0 8px 0", color: "#374151" }}>🎨 AI-Powered Wireframe Generation</h4>
                      <p style={{ margin: 0, color: "#6b7280", fontSize: 14 }}>
                        Generate interactive wireframes from your FRD content or user stories. Our AI analyzes your requirements 
                        and creates professional, domain-specific wireframes with clickable navigation and responsive design.
                      </p>
                    </div>

                    <WireframeGenerator
                      projectName={savedProjectName}
                      frdContent={frdPreviewHtml}
                      onWireframeGenerated={(html, domain) => {
                        console.log('Standalone wireframes generated for project:', savedProjectName);
                        setMsg(`✅ Interactive wireframes generated successfully for ${domain} domain! File downloaded.`);
                        setTimeout(() => setMsg(""), 4000);
                      }}
                    />
                  </div>
                )}

                {documentGenerator === "Prototype Generator" && (
                  <div style={{ marginTop: 18 }}>
                    <WireframeGenerator
                      projectName={savedProjectName}
                      frdContent={frdPreviewHtml}
                      isPrototypeMode={true}
                      onWireframeGenerated={(html, domain) => {
                        console.log('Interactive prototype generated for project:', savedProjectName);
                        setMsg(`✅ Interactive prototype generated successfully for ${domain} domain! File downloaded.`);
                        setTimeout(() => setMsg(""), 4000);
                      }}
                    />
                  </div>
                )}

                {documentGenerator && documentGenerator !== "BRD Creation" && documentGenerator !== "FRD Creation" && documentGenerator !== "Wire Frame Generator" && documentGenerator !== "Prototype Generator" && (
                  <div style={{ marginTop: 18 }}>
                    <p style={{ color: "#6b7280" }}>Selected: {documentGenerator}. Document editor will appear here.</p>
                  </div>
                )}
              </section>
            </div>
          </main>
        </div>

        {msg && <div style={{ position: "fixed", bottom: 20, right: 20, background: "#111827", color: "#fff", padding: "10px 14px", borderRadius: 8 }}>{msg}</div>}
      </div>
    );
  }

  return (
    <div style={pageStyle}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 18 }}>
          <h2 style={{ margin: 0, color: "#0f172a" }}>BA Assistant Tool</h2>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <button style={topButton} onClick={handleAddProject}>+ New Project</button>
            <button onClick={handleLogout} style={{ background: "transparent", border: "1px solid #e6e9ef", padding: "8px 12px", borderRadius: 8, cursor: "pointer" }}>Logout</button>
          </div>
        </div>

        {selectedSearchProject ? (
          <div style={cardStyle}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 600 }}>Project</div>
                <div style={{ marginTop: 6, fontSize: 18, fontWeight: 700, color: "#0f172a" }}>{selectedSearchProject}</div>
              </div>
              <div>
                <button onClick={() => { setSelectedSearchProject(""); setSearchTerm(""); }} style={{ background: "transparent", border: "1px solid #e6e9ef", padding: "8px 12px", borderRadius: 8 }}>Back</button>
              </div>
            </div>

            <div style={{ marginTop: 16 }}>
              <div style={{ fontWeight: 700, marginBottom: 16, fontSize: "18px" }}>Project Modules & Documents</div>
              
              {/* Module-wise Document Display */}
              <div style={{ display: "grid", gap: "16px" }}>
                {MODULES.map((module) => {
                  const moduleType = module.includes("BRD") ? "BRD" : 
                                   module.includes("FRD") ? "FRD" : 
                                   module.includes("SRS") ? "SRS" : 
                                   module.includes("Impact") ? "Impact Analysis" : 
                                   module.includes("Priortization") ? "Requirement Prioritization" :
                                   module.includes("Wireframe") ? "Wireframe" : 
                                   module.includes("Prototype") ? "Prototype" : module;
                  
                  const moduleDocuments = projects[selectedSearchProject]?.documents?.filter(d => {
                    if (module.includes("BRD")) return d.type === "BRD";
                    if (module.includes("FRD")) return d.type === "FRD";
                    if (module.includes("SRS")) return d.type === "SRS";
                    if (module.includes("Impact")) return d.type === "Impact Analysis";
                    if (module.includes("Priortization")) return d.type === "Requirement Prioritization";
                    if (module.includes("Wireframe")) return d.type === "Wireframe";
                    if (module.includes("Prototype")) return d.type === "Prototype";
                    return false;
                  }) || [];

                  const approvedDocs = moduleDocuments.filter(d => d.approved);

                  return (
                    <div key={module} style={{ 
                      border: "1px solid #e6e9ef", 
                      borderRadius: "8px", 
                      padding: "16px",
                      backgroundColor: "#fafbfc"
                    }}>
                      <div style={{ 
                        display: "flex", 
                        justifyContent: "space-between", 
                        alignItems: "center",
                        marginBottom: "12px"
                      }}>
                        <h3 style={{ 
                          margin: 0, 
                          fontSize: "16px", 
                          fontWeight: "600",
                          color: "#1f2937"
                        }}>
                          {module}
                        </h3>
                        <span style={{
                          fontSize: "12px",
                          color: "#6b7280",
                          backgroundColor: "#f3f4f6",
                          padding: "4px 8px",
                          borderRadius: "12px"
                        }}>
                          {approvedDocs.length} approved document{approvedDocs.length !== 1 ? 's' : ''}
                        </span>
                      </div>

                      {approvedDocs.length > 0 ? (
                        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                          {approvedDocs.map((d) => (
                            <div key={d.id} style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                              padding: "8px 12px",
                              backgroundColor: "#fff",
                              border: "1px solid #e5e7eb",
                              borderRadius: "6px",
                              boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)"
                            }}>
                              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                                <div style={{
                                  width: "8px",
                                  height: "8px",
                                  borderRadius: "50%",
                                  backgroundColor: "#10b981"
                                }} />
                                <span style={{ fontWeight: "500", color: "#374151" }}>
                                  {moduleType} V{d.version}
                                </span>
                                <span style={{
                                  fontSize: "11px",
                                  color: "#059669",
                                  backgroundColor: "#d1fae5",
                                  padding: "2px 6px",
                                  borderRadius: "4px",
                                  fontWeight: "500"
                                }}>
                                  ✓ APPROVED
                                </span>
                              </div>
                              <button 
                                onClick={() => handleDownloadDoc(selectedSearchProject, d)} 
                                style={{ 
                                  padding: "6px 12px", 
                                  borderRadius: "4px", 
                                  border: "1px solid #d1d5db", 
                                  background: "#fff", 
                                  cursor: "pointer",
                                  fontSize: "12px",
                                  fontWeight: "500",
                                  color: "#374151"
                                }}
                                onMouseOver={(e) => e.target.style.backgroundColor = "#f9fafb"}
                                onMouseOut={(e) => e.target.style.backgroundColor = "#fff"}
                              >
                                Download
                              </button>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div style={{
                          textAlign: "center",
                          padding: "16px",
                          color: "#9ca3af",
                          fontSize: "14px",
                          fontStyle: "italic"
                        }}>
                          No approved documents available
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* All Documents Table - Hidden by default, can be shown with a toggle */}
              <div style={{ marginTop: "24px", paddingTop: "16px", borderTop: "1px solid #e5e7eb" }}>
                <details>
                  <summary style={{ 
                    cursor: "pointer", 
                    fontWeight: "600", 
                    fontSize: "14px", 
                    color: "#6b7280",
                    marginBottom: "12px"
                  }}>
                    View All Documents (including unapproved)
                  </summary>
                  {projects[selectedSearchProject]?.documents?.length ? (
                    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
                      <thead>
                        <tr style={{ textAlign: "left", borderBottom: "1px solid #eef2f6" }}>
                          <th style={{ padding: "8px 6px" }}>Type</th>
                          <th style={{ padding: "8px 6px" }}>Version</th>
                          <th style={{ padding: "8px 6px" }}>Status</th>
                          <th style={{ padding: "8px 6px" }}>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {projects[selectedSearchProject].documents.map((d) => (
                          <tr key={d.id} style={{ borderBottom: "1px solid #f3f4f6" }}>
                            <td style={{ padding: "10px 6px" }}>{d.type}</td>
                            <td style={{ padding: "10px 6px" }}>{d.version}</td>
                            <td style={{ padding: "10px 6px" }}>
                              <span style={{
                                fontSize: "12px",
                                padding: "2px 8px",
                                borderRadius: "12px",
                                backgroundColor: d.approved ? "#d1fae5" : "#fef3c7",
                                color: d.approved ? "#059669" : "#d97706",
                                fontWeight: "500"
                              }}>
                                {d.approved ? "Approved" : "Pending"}
                              </span>
                            </td>
                            <td style={{ padding: "10px 6px" }}>
                              <button onClick={() => handleDownloadDoc(selectedSearchProject, d)} style={{ marginRight: 8, padding: "6px 10px", borderRadius: 6, border: "1px solid #e6e9ef", background: "#fff", cursor: "pointer", fontSize: "12px" }}>Download</button>
                              {!d.approved && <button onClick={() => {
                                setProjects(prev => {
                                  const copy = { ...prev };
                                  const p = copy[selectedSearchProject];
                                  if (!p) return prev;
                                  const idx = p.documents.findIndex(x => x.id === d.id);
                                  if (idx >= 0) p.documents[idx].approved = true;
                                  copy[selectedSearchProject] = p;
                                  return copy;
                                });
                                setMsg("Document approved.");
                                setTimeout(() => setMsg(""), 1200);
                              }} style={{ padding: "6px 10px", borderRadius: 6, background: "#047857", color: "#fff", border: "none", cursor: "pointer", fontSize: "12px" }}>Approve</button>}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p style={{ color: "#6b7280" }}>No documents found for this project.</p>
                  )}
                </details>
              </div>
            </div>
          </div>
        ) : (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 20 }}>
              <div style={{ ...cardStyle, padding: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 600 }}>Total Projects</div>
                    <div style={{ marginTop: 8, fontSize: 22, fontWeight: 700, color: "#111827" }}>Projects overview</div>
                  </div>
                  <div>
                    <button onClick={handleAddProject} style={{ ...topButton, padding: "6px 10px", fontSize: 13 }}>Add</button>
                  </div>
                </div>

                <div style={{ marginTop: 18, textAlign: "center", paddingTop: 12, borderTop: "1px solid #eef2f6" }}>
                  <div style={{ fontSize: 28, fontWeight: 800 }}>{Object.keys(projects).length || totalProjects}</div>
                  <div style={{ marginTop: 6, color: "#6b7280", fontSize: 13 }}>Total projects</div>
                </div>
              </div>

              <div style={{ ...cardStyle, padding: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 600 }}>Completed Projects</div>
                    <div style={{ marginTop: 8, fontSize: 22, fontWeight: 700, color: "#111827" }}>Completion status</div>
                  </div>
                  <div>
                    <button onClick={handleCompleteProject} style={{ background: "#047857", color: "#fff", padding: "6px 10px", borderRadius: 8, border: "none", cursor: "pointer", fontWeight: 600, fontSize: 13 }}>Mark Complete</button>
                  </div>
                </div>

                <div style={{ marginTop: 18, textAlign: "center", paddingTop: 12, borderTop: "1px solid #eef2f6" }}>
                  <div style={{ fontSize: 28, fontWeight: 800, color: "#059669" }}>{completedProjects}</div>
                  <div style={{ marginTop: 6, color: "#6b7280", fontSize: 13 }}>Completed projects</div>
                </div>
              </div>
            </div>

            <div style={{ marginTop: 20 }}>
              <div style={{ fontWeight: 700, marginBottom: 8 }}>Recent Projects</div>
              <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
                {Object.keys(projects).length ? Object.keys(projects).map(k => (
                  <div key={k} style={{ background: "#fff", padding: 12, borderRadius: 8, boxShadow: "0 4px 12px rgba(16,24,40,0.04)", minWidth: 200 }}>
                    <div style={{ fontWeight: 700 }}>{k}</div>
                    <div style={{ marginTop: 8 }}>
                      <button onClick={() => { setSelectedSearchProject(k); setSearchTerm(k); }} style={{ padding: "6px 10px", borderRadius: 6, border: "1px solid #e6e9ef", background: "#fff", cursor: "pointer" }}>Open</button>
                    </div>
                  </div>
                )) : <p style={{ color: "#6b7280" }}>No projects yet. Create one with + New Project.</p>}
              </div>
            </div>
          </div>
        )}

        {msg && <div style={{ position: "fixed", bottom: 20, right: 20, background: "#111827", color: "#fff", padding: "10px 14px", borderRadius: 8 }}>{msg}</div>}
      </div>
    </div>
  );
}
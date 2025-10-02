"""
Domain-Agnostic BRD Generation Service

This module implements a domain-agnostic Business Requirements Document (BRD) generation
following a standardized structure and methodology. It ensures consistent formatting,
traceability, and professional output regardless of the business domain.

Key Features:
- Domain-agnostic approach with consistent structure
- Required sections: Scope, Business Objectives, EPICs, KPIs, Risk Assessment
- Traceability with IDs: OBJ-#, EPIC-<area>-#, KPI-#, RISK-#
- TBV (To Be Validated) markers for inferred content
- Flat bullet lists and concise business language
"""

from typing import Dict, Any, List, Tuple
import re
import logging

logger = logging.getLogger(__name__)


def _safe(x: Any) -> str:
    """Safely convert any value to string."""
    return "" if x is None else str(x).strip()


def _extract_scope_items(scope_text: str) -> Tuple[List[str], List[str]]:
    """
    Extract included and excluded items from scope text.
    Returns (included_items, excluded_items)
    """
    included = []
    excluded = []
    
    if not scope_text:
        return (included, excluded)
    
    lines = scope_text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section markers
        if re.match(r'^included\s*[—-]?\s*', line, re.IGNORECASE):
            current_section = 'included'
            # Extract content after "Included —"
            content = re.sub(r'^included\s*[—-]?\s*', '', line, flags=re.IGNORECASE).strip()
            if content:
                # Split by commas ONLY, preserving parentheses
                parts = []
                current_part = ""
                paren_depth = 0
                
                for char in content:
                    if char == '(':
                        paren_depth += 1
                        current_part += char
                    elif char == ')':
                        paren_depth -= 1
                        current_part += char
                    elif char == ',' and paren_depth == 0:
                        if current_part.strip():
                            parts.append(current_part.strip())
                        current_part = ""
                    else:
                        current_part += char
                
                if current_part.strip():
                    parts.append(current_part.strip())
                
                included.extend(parts)
            continue
        elif re.match(r'^excluded\s*[—-]?\s*', line, re.IGNORECASE):
            current_section = 'excluded'
            # Extract content after "Excluded —"
            content = re.sub(r'^excluded\s*[—-]?\s*', '', line, flags=re.IGNORECASE).strip()
            if content:
                parts = [p.strip() for p in content.split(',') if p.strip()]
                excluded.extend(parts)
            continue
        
        # Add line to current section
        if current_section == 'included':
            # Check if line contains multiple items separated by commas (but not inside parens)
            parts = []
            current_part = ""
            paren_depth = 0
            
            for char in line:
                if char == '(':
                    paren_depth += 1
                    current_part += char
                elif char == ')':
                    paren_depth -= 1
                    current_part += char
                elif char == ',' and paren_depth == 0:
                    if current_part.strip():
                        parts.append(current_part.strip())
                    current_part = ""
                else:
                    current_part += char
            
            if current_part.strip():
                parts.append(current_part.strip())
            
            if parts:
                included.extend(parts)
            else:
                included.append(line)
        elif current_section == 'excluded':
            if ',' in line:
                parts = [p.strip() for p in line.split(',') if p.strip()]
                excluded.extend(parts)
            else:
                excluded.append(line)
    
    return (included, excluded)


def _extract_objectives(objectives_text: str) -> List[str]:
    """Extract business objectives from text."""
    if not objectives_text:
        return []
    
    objectives = []
    
    # First, try to split by semicolons (common separator)
    if ';' in objectives_text:
        parts = objectives_text.split(';')
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Remove bullet points and numbering
            part = re.sub(r'^[•\-*0-9\.)\]]+\s*', '', part)
            part = part.strip()
            if part:
                objectives.append(part)
        return objectives
    
    # Otherwise, split by lines
    lines = objectives_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove bullet points and numbering
        line = re.sub(r'^[•\-*0-9\.)\]]+\s*', '', line)
        line = line.strip()
        
        if line:
            objectives.append(line)
    
    return objectives


def _extract_requirements_by_area(requirements_text: str) -> Dict[str, List[str]]:
    """
    Extract requirements organized by area/module.
    Returns a dictionary mapping area names to lists of requirements.
    """
    areas = {}
    current_area = None
    
    if not requirements_text:
        return areas
    
    lines = requirements_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line defines an area (e.g., "AP:", "AR:", "GL & Close:")
        area_match = re.match(r'^([A-Z][A-Za-z\s&]+):\s*(.+)$', line)
        if area_match:
            area_name = area_match.group(1).strip()
            requirements = area_match.group(2).strip()
            
            # Split requirements by semicolon
            req_list = [r.strip() for r in requirements.split(';') if r.strip()]
            
            if area_name not in areas:
                areas[area_name] = []
            areas[area_name].extend(req_list)
            current_area = area_name
        elif current_area:
            # Continuation of current area
            if ';' in line:
                req_list = [r.strip() for r in line.split(';') if r.strip()]
                areas[current_area].extend(req_list)
            else:
                areas[current_area].append(line)
    
    return areas


def _extract_validations(validations_text: str) -> List[str]:
    """Extract validation rules from text."""
    if not validations_text:
        return []
    
    validations = []
    lines = validations_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove bullet points
        line = re.sub(r'^[•\-*0-9\.)\]]+\s*', '', line)
        line = line.strip()
        
        # Split by semicolons if present
        if ';' in line:
            parts = [p.strip() for p in line.split(';') if p.strip()]
            validations.extend(parts)
        elif line:
            validations.append(line)
    
    return validations


def _create_area_abbreviation(area_name: str) -> str:
    """Create a short abbreviation for an area name."""
    # Special cases for financial accounting
    area_upper = area_name.upper()
    if area_upper == 'AP':
        return 'AP'
    elif area_upper == 'AR':
        return 'AR'
    elif 'GL' in area_upper and 'CLOSE' in area_upper:
        return 'GL'
    elif 'BANK' in area_upper or 'CASH' in area_upper:
        return 'BANK'
    elif 'ASSET' in area_upper or area_upper == 'ASSETS':
        return 'FA'  # Fixed Assets
    elif 'REPORT' in area_upper:
        return 'REP'
    
    # For multi-word areas, use initials or first word
    words = area_name.split()
    if len(words) > 1:
        # Use first 2-3 letters of each word
        if '&' in area_name:
            return ''.join([w[0].upper() for w in words if w != '&'])
        else:
            return words[0][:3].upper() if len(words[0]) > 3 else words[0].upper()
    else:
        # Single word - use first 2-4 letters
        return area_name[:4].upper() if len(area_name) > 4 else area_name.upper()


def generate_domain_agnostic_brd_html(project: str, inputs: Dict[str, Any], version: int) -> str:
    """
    Generate a domain-agnostic BRD following the standardized structure.
    
    Args:
        project: Project name
        inputs: Dictionary containing scope, objectives, briefRequirements, assumptions, validations
        version: BRD version number
        
    Returns:
        HTML string containing the formatted BRD
    """
    logger.info(f"🎯 Generating domain-agnostic BRD for project: {project}")
    
    # Extract input sections
    scope_text = _safe(inputs.get("scope", ""))
    objectives_text = _safe(inputs.get("objectives", ""))
    requirements_text = _safe(inputs.get("briefRequirements", "") or inputs.get("requirements", ""))
    assumptions_text = _safe(inputs.get("assumptions", ""))
    validations_text = _safe(inputs.get("validations", "") or inputs.get("validation", ""))
    
    # Parse inputs
    included_scope, excluded_scope = _extract_scope_items(scope_text)
    objectives = _extract_objectives(objectives_text)
    requirements_by_area = _extract_requirements_by_area(requirements_text)
    validations = _extract_validations(validations_text)
    
    logger.info(f"📊 Parsed: {len(included_scope)} included, {len(excluded_scope)} excluded, "
                f"{len(objectives)} objectives, {len(requirements_by_area)} areas")
    
    # Build HTML
    html = f"""
<div style="font-family: Arial, Helvetica, sans-serif; color: #1f2937; padding: 24px; max-width: 1200px; margin: 0 auto;">
  <h1 style="text-align: center; color: #1e40af; margin-bottom: 8px; font-size: 28px;">
    Business Requirements Document (BRD)
  </h1>
  <h2 style="text-align: center; color: #64748b; margin-top: 4px; font-size: 20px; font-weight: normal;">
    {project} — Version {version}
  </h2>
  <hr style="border: none; border-top: 2px solid #e5e7eb; margin: 24px 0;"/>
  
"""
    
    # 1. Scope of the Project
    html += """
  <section style="margin-bottom: 32px;">
    <h3 style="color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 16px;">
      1. Scope of the Project
    </h3>
"""
    
    # In Scope
    html += """
    <h4 style="color: #374151; margin-top: 16px; margin-bottom: 8px;">In Scope</h4>
    <ul style="list-style-type: disc; margin-left: 24px; line-height: 1.8;">
"""
    if included_scope:
        for item in included_scope:
            html += f"      <li>{item}</li>\n"
    else:
        html += "      <li>To Be Validated (TBV): Scope items not explicitly provided</li>\n"
    
    html += """    </ul>
"""
    
    # Out of Scope
    html += """
    <h4 style="color: #374151; margin-top: 16px; margin-bottom: 8px;">Out of Scope</h4>
    <ul style="list-style-type: disc; margin-left: 24px; line-height: 1.8;">
"""
    if excluded_scope:
        for item in excluded_scope:
            html += f"      <li>{item}</li>\n"
    else:
        html += "      <li>To Be Validated (TBV): Out of scope items to be defined during scoping phase</li>\n"
    
    html += """    </ul>
"""
    
    # Boundaries & Dependencies
    html += """
    <h4 style="color: #374151; margin-top: 16px; margin-bottom: 8px;">Boundaries & Dependencies</h4>
    <ul style="list-style-type: disc; margin-left: 24px; line-height: 1.8;">
"""
    if assumptions_text:
        # Extract dependencies from assumptions
        assumptions_list = assumptions_text.split(';')
        for assumption in assumptions_list:
            assumption = assumption.strip()
            if assumption:
                html += f"      <li>{assumption}</li>\n"
    else:
        html += """      <li>To Be Validated (TBV): System dependencies and integration requirements</li>
      <li>To Be Validated (TBV): Infrastructure and environment requirements</li>
      <li>To Be Validated (TBV): Data source and system of record definitions</li>
"""
    
    html += """    </ul>
  </section>
"""
    
    # 2. Business Objectives
    html += """
  <section style="margin-bottom: 32px;">
    <h3 style="color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 16px;">
      2. Business Objectives
    </h3>
    <ul style="list-style-type: none; margin-left: 0; padding-left: 0; line-height: 2;">
"""
    
    if objectives:
        for idx, objective in enumerate(objectives, 1):
            # Create objective with hypothesis
            obj_text = objective.rstrip('.')
            hypothesis = "Hypothesis: TBV — success criteria and measurable outcomes to be defined"
            
            # Try to infer a simple hypothesis
            if any(word in objective.lower() for word in ['reduce', 'decrease', 'lower']):
                hypothesis = "Hypothesis: implementation of targeted capabilities will result in measurable reduction"
            elif any(word in objective.lower() for word in ['increase', 'improve', 'enhance', 'accelerate']):
                hypothesis = "Hypothesis: enhanced capabilities will lead to measurable improvement"
            elif any(word in objective.lower() for word in ['strengthen', 'ensure', 'provide']):
                hypothesis = "Hypothesis: systematic implementation will ensure consistent achievement"
            
            html += f"""      <li style="margin-bottom: 12px;">
        <strong style="color: #1e40af;">OBJ-{idx}</strong> {obj_text}; {hypothesis}.
      </li>
"""
    else:
        html += """      <li style="margin-bottom: 12px;">
        <strong style="color: #1e40af;">OBJ-1</strong> To Be Validated (TBV): Primary business objectives to be defined based on stakeholder requirements.
      </li>
"""
    
    html += """    </ul>
  </section>
"""
    
    # 3. EPICs
    html += """
  <section style="margin-bottom: 32px;">
    <h3 style="color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 16px;">
      3. EPICs
    </h3>
"""
    
    if requirements_by_area:
        epic_num = 1
        for area, capabilities in requirements_by_area.items():
            area_abbr = _create_area_abbreviation(area)
            epic_id = f"EPIC-{area_abbr}-{epic_num}"
            
            # Generate problem, value, and acceptance based on capabilities
            problem = f"Manual or inefficient {area.lower()} processes create operational bottlenecks"
            value = f"Streamlined {area.lower()} capabilities improve efficiency and accuracy"
            
            html += f"""
    <div style="margin-bottom: 24px; padding: 16px; background-color: #f9fafb; border-left: 4px solid #3b82f6; border-radius: 4px;">
      <h4 style="color: #1e40af; margin-top: 0; margin-bottom: 8px;">
        {epic_id}: {area}
      </h4>
      
      <p style="margin: 8px 0;"><strong>Problem:</strong> {problem}</p>
      <p style="margin: 8px 0;"><strong>Value:</strong> {value}</p>
      
      <p style="margin: 8px 0 4px 0;"><strong>Capabilities:</strong></p>
      <ul style="list-style-type: disc; margin-left: 24px; margin-top: 4px; line-height: 1.6;">
"""
            for capability in capabilities:
                html += f"        <li>{capability}</li>\n"
            
            html += """      </ul>
      
      <p style="margin: 8px 0 4px 0;"><strong>Constraints & Validations:</strong></p>
      <ul style="list-style-type: disc; margin-left: 24px; margin-top: 4px; line-height: 1.6;">
"""
            # Map relevant validations to this EPIC
            relevant_validations = []
            for validation in validations[:2]:  # Limit to 2 most relevant per EPIC
                relevant_validations.append(validation)
            
            if relevant_validations:
                for validation in relevant_validations:
                    html += f"        <li>{validation}</li>\n"
            else:
                html += "        <li>To Be Validated (TBV): Specific validation rules to be defined</li>\n"
            
            html += """      </ul>
      
      <p style="margin: 8px 0 4px 0;"><strong>Acceptance:</strong></p>
      <ul style="list-style-type: disc; margin-left: 24px; margin-top: 4px; line-height: 1.6;">
        <li>TBV: Measurable acceptance criteria to be defined (e.g., processing time, error rates)</li>
        <li>TBV: User acceptance and functional completeness criteria</li>
      </ul>
    </div>
"""
            epic_num += 1
    else:
        html += """
    <div style="margin-bottom: 24px; padding: 16px; background-color: #f9fafb; border-left: 4px solid #3b82f6; border-radius: 4px;">
      <h4 style="color: #1e40af; margin-top: 0;">EPIC-01: Core Business Capabilities</h4>
      <p style="margin: 8px 0;">To Be Validated (TBV): EPICs to be derived from detailed requirements and business objectives.</p>
    </div>
"""
    
    html += """  </section>
"""
    
    # 4. Success Metrics & KPIs
    html += """
  <section style="margin-bottom: 32px;">
    <h3 style="color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 16px;">
      4. Success Metrics & KPIs
    </h3>
    <ul style="list-style-type: none; margin-left: 0; padding-left: 0;">
"""
    
    # Generate domain-agnostic KPIs based on objectives
    kpis = [
        {
            "name": "Process Cycle Time",
            "formula": "Average time from initiation to completion",
            "target": "TBV: Baseline and target to be established",
            "frequency": "Monthly",
            "source": "TBV: Primary transaction system",
            "owner": "Operations Manager",
            "link": "OBJ-1"
        },
        {
            "name": "Process Accuracy Rate",
            "formula": "Successful transactions / Total transactions × 100",
            "target": "TBV: Target percentage (e.g., >95%)",
            "frequency": "Monthly",
            "source": "TBV: Quality monitoring system",
            "owner": "Quality Manager",
            "link": "OBJ-1"
        },
        {
            "name": "Automation Rate",
            "formula": "Automated transactions / Total transactions × 100",
            "target": "TBV: Target automation level",
            "frequency": "Monthly",
            "source": "TBV: Workflow system",
            "owner": "Process Excellence Lead",
            "link": "OBJ-2"
        },
        {
            "name": "User Adoption Rate",
            "formula": "Active users / Total users × 100",
            "target": "TBV: Target adoption level",
            "frequency": "Weekly",
            "source": "TBV: Usage analytics platform",
            "owner": "Change Management Lead",
            "link": "OBJ-1"
        },
        {
            "name": "Exception Rate",
            "formula": "Exceptions requiring manual intervention / Total transactions × 100",
            "target": "TBV: Target exception rate",
            "frequency": "Monthly",
            "source": "TBV: Exception management system",
            "owner": "Operations Manager",
            "link": "OBJ-2"
        },
        {
            "name": "Compliance Score",
            "formula": "Compliant transactions / Total transactions × 100",
            "target": "TBV: Target compliance level (typically 100%)",
            "frequency": "Monthly",
            "source": "TBV: Compliance monitoring system",
            "owner": "Compliance Officer",
            "link": "OBJ-3"
        }
    ]
    
    for idx, kpi in enumerate(kpis, 1):
        html += f"""
      <li style="margin-bottom: 20px; padding: 12px; background-color: #f9fafb; border-radius: 4px;">
        <strong style="color: #1e40af;">KPI-{idx}: {kpi['name']}</strong><br/>
        <span style="display: inline-block; margin-left: 16px; margin-top: 4px;">
          <strong>Formula:</strong> {kpi['formula']}<br/>
          <strong>Target:</strong> {kpi['target']}<br/>
          <strong>Frequency:</strong> {kpi['frequency']}<br/>
          <strong>Data Source:</strong> {kpi['source']}<br/>
          <strong>Owner:</strong> {kpi['owner']}<br/>
          <strong>Traceability:</strong> Linked to {kpi['link']}
        </span>
      </li>
"""
    
    html += """    </ul>
  </section>
"""
    
    # 5. Risk Assessment & Mitigation
    html += """
  <section style="margin-bottom: 32px;">
    <h3 style="color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 16px;">
      5. Risk Assessment & Mitigation
    </h3>
    <ul style="list-style-type: none; margin-left: 0; padding-left: 0;">
"""
    
    risks = [
        {
            "category": "Data Quality",
            "description": "Incomplete or inconsistent source data may impact system functionality",
            "likelihood": "Medium",
            "impact": "High",
            "score": "M×H",
            "triggers": "Data validation failures during initial load",
            "mitigation": "Conduct data profiling and cleansing prior to migration; implement validation checkpoints",
            "contingency": "Staged data migration with fallback to manual processes"
        },
        {
            "category": "Integration",
            "description": "Dependencies on external systems may cause delays or failures",
            "likelihood": "Medium",
            "impact": "High",
            "score": "M×H",
            "triggers": "Integration testing failures; API availability issues",
            "mitigation": "Early integration testing; establish SLAs with providers; implement retry logic",
            "contingency": "Manual workarounds; phased integration approach"
        },
        {
            "category": "Change Management",
            "description": "User resistance or insufficient training may limit adoption",
            "likelihood": "Medium",
            "impact": "Medium",
            "score": "M×M",
            "triggers": "Low usage metrics; high support ticket volume",
            "mitigation": "Comprehensive training program; user champions; phased rollout",
            "contingency": "Extended hypercare; additional training sessions"
        },
        {
            "category": "Scope",
            "description": "Requirement changes or scope creep may impact timeline and budget",
            "likelihood": "Medium",
            "impact": "Medium",
            "score": "M×M",
            "triggers": "Frequent change requests; stakeholder disagreements",
            "mitigation": "Robust change control process; clear requirements documentation",
            "contingency": "Defer lower priority items to future phases"
        },
        {
            "category": "Compliance",
            "description": "Regulatory requirements may evolve during implementation",
            "likelihood": "Low",
            "impact": "High",
            "score": "L×H",
            "triggers": "Regulatory updates; audit findings",
            "mitigation": "Regular compliance reviews; flexible system design",
            "contingency": "Rapid remediation process; regulatory liaison"
        },
        {
            "category": "Performance",
            "description": "System may not meet performance requirements under load",
            "likelihood": "Low",
            "impact": "Medium",
            "score": "L×M",
            "triggers": "Performance testing reveals bottlenecks",
            "mitigation": "Early performance testing; scalability design; load testing",
            "contingency": "Infrastructure scaling; optimization sprints"
        }
    ]
    
    for idx, risk in enumerate(risks, 1):
        html += f"""
      <li style="margin-bottom: 20px; padding: 12px; background-color: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 4px;">
        <strong style="color: #92400e;">RISK-{idx}: {risk['category']}</strong><br/>
        <span style="display: inline-block; margin-left: 16px; margin-top: 4px; line-height: 1.6;">
          <strong>Description:</strong> {risk['description']}<br/>
          <strong>Likelihood:</strong> {risk['likelihood']} | <strong>Impact:</strong> {risk['impact']} | <strong>Score:</strong> {risk['score']}<br/>
          <strong>Triggers:</strong> {risk['triggers']}<br/>
          <strong>Mitigation:</strong> {risk['mitigation']}<br/>
          <strong>Contingency:</strong> {risk['contingency']}
        </span>
      </li>
"""
    
    html += """    </ul>
  </section>
"""
    
    # Footer
    html += """
  <hr style="border: none; border-top: 2px solid #e5e7eb; margin: 32px 0 16px 0;"/>
  <p style="text-align: center; font-size: 12px; color: #9ca3af;">
    Generated by BA Assistant Tool — Domain-Agnostic BRD Generator
  </p>
</div>
"""
    
    logger.info(f"✅ Domain-agnostic BRD generated: {len(html)} characters")
    return html

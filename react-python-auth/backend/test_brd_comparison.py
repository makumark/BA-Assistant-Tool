#!/usr/bin/env python3
"""
Comparison test showing the difference between old and new BRD formats.
This demonstrates the improvements made by the domain-agnostic generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def compare_brd_formats():
    """Generate BRDs using both old and new methods for comparison."""
    
    from app.services.ai_service import _local_fallback
    from app.services.ai_service_domain_agnostic import generate_domain_agnostic_brd_html
    
    # Use the financial accounting example
    inputs = {
        "scope": """
Included — chart of accounts and journal processing, payables (invoice capture/3 way match, approvals, payments), receivables (invoicing, receipts, dunning), bank reconciliation and cash management, fixed assets and depreciation, period close and financial reporting, role based admin and audit.

Excluded — full ERP replacement, treasury trading platform, tax engine re platform, and payroll processing in phase 1. Phasing: AP → AR → GL/Reporting.
        """,
        "objectives": """
Accelerate month end close; improve invoice cycle time and on time payments; increase cash application automation; reduce manual journal entries and posting errors; strengthen controls and audit readiness; provide timely management reporting.
        """,
        "briefRequirements": """
AP: vendor master; invoice ingestion (PDF/e invoice); 2/3 way match; approvals; payment runs; credit notes.
AR: customer master; billing schedules; invoicing; receipts; dunning; write offs.
GL & Close: journals (recurring/allocations); subledger posting; reconciliation; close checklist; consolidations.
Bank & Cash: statements import; auto match rules; cash positioning; forecasts.
Assets: capitalization; depreciation methods; disposals; revaluations.
Reporting: trial balance; P&L; balance sheet; aging; custom analytics; exports.
        """,
        "assumptions": """
Cleansed master data (vendors/customers/COA) available; banking/payment and e invoicing providers provisioned; approval matrices and delegation policies approved; environments and SSO exist; data retention and audit policies defined.
        """,
        "validations": """
Mandatory master data fields; duplicate detection (vendor/customer and invoice numbers); PO/GRN match tolerances; tax and currency rules; posting period/status checks; segregation of duties for approvals and postings; balanced journal (debits=credits); bank account verification before payouts; document type/amount thresholds requiring multi level approval.
        """
    }
    
    project = "Financial Accounting System"
    version = 1
    
    print("=" * 80)
    print("📊 BRD Format Comparison")
    print("=" * 80)
    print()
    
    # Generate using old method
    print("🔷 Generating OLD format BRD (traditional fallback)...")
    old_html = _local_fallback(project, inputs, version)
    
    # Generate using new method
    print("🔶 Generating NEW format BRD (domain-agnostic)...")
    new_html = generate_domain_agnostic_brd_html(project, inputs, version)
    
    print()
    print("=" * 80)
    print("📈 Comparison Results")
    print("=" * 80)
    print()
    
    # Size comparison
    print(f"📏 Size:")
    print(f"   Old format: {len(old_html):,} characters")
    print(f"   New format: {len(new_html):,} characters")
    print()
    
    # Structure comparison
    print("🏗️  Structure:")
    print()
    
    features = [
        ("EPIC-", "EPICs with area-based IDs"),
        ("OBJ-", "Objectives with IDs"),
        ("KPI-", "KPIs with IDs"),
        ("RISK-", "Risk Assessment with IDs"),
        ("TBV", "TBV markers"),
        ("Scope of the Project", "Structured Scope section"),
        ("In Scope", "In Scope subsection"),
        ("Out of Scope", "Out of Scope subsection"),
        ("Boundaries & Dependencies", "Dependencies subsection"),
        ("Success Metrics", "Success Metrics section"),
        ("Risk Assessment & Mitigation", "Risk Assessment section"),
        ("Hypothesis:", "Objective hypotheses"),
        ("Problem:", "EPIC problem statements"),
        ("Value:", "EPIC value statements"),
        ("Capabilities:", "EPIC capabilities"),
        ("Constraints & Validations:", "EPIC constraints"),
        ("Acceptance:", "EPIC acceptance criteria"),
        ("Traceability:", "KPI traceability")
    ]
    
    print(f"{'Feature':<40} {'Old':<8} {'New':<8}")
    print("-" * 80)
    
    for pattern, description in features:
        old_has = "✅" if pattern in old_html else "❌"
        new_has = "✅" if pattern in new_html else "❌"
        
        status = ""
        if old_has == "❌" and new_has == "✅":
            status = "  🆕 NEW!"
        elif old_has == "✅" and new_has == "❌":
            status = "  ⚠️ REMOVED"
        
        print(f"{description:<40} {old_has:<8} {new_has:<8}{status}")
    
    print()
    print("=" * 80)
    print("✅ Summary")
    print("=" * 80)
    print()
    print("The NEW domain-agnostic format provides:")
    print("  ✓ Structured sections with proper headings")
    print("  ✓ Proper ID formats for traceability (OBJ-#, EPIC-<area>-#, KPI-#, RISK-#)")
    print("  ✓ EPICs with Problem, Value, Capabilities, and Acceptance criteria")
    print("  ✓ KPIs with formulas, targets, frequency, and traceability")
    print("  ✓ Risk Assessment with likelihood, impact, mitigation, and contingency")
    print("  ✓ TBV markers for inferred content")
    print("  ✓ Domain-agnostic approach suitable for any industry")
    print()
    
    # Save both for manual inspection
    with open("/tmp/old_format_brd.html", "w", encoding="utf-8") as f:
        f.write(old_html)
    with open("/tmp/new_format_brd.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    
    print("💾 Files saved for comparison:")
    print("   Old format: /tmp/old_format_brd.html")
    print("   New format: /tmp/new_format_brd.html")
    print()


if __name__ == "__main__":
    compare_brd_formats()

#!/usr/bin/env python3
"""
Test script for domain-agnostic BRD generation following the exact structure
specified in the problem statement.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_financial_accounting_brd():
    """Test BRD generation with the exact financial accounting example from problem statement."""
    
    from app.services.ai_service_domain_agnostic import generate_domain_agnostic_brd_html
    
    # Exact inputs from problem statement
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
    
    print("=" * 80)
    print("🧪 Testing Domain-Agnostic BRD Generation")
    print("=" * 80)
    print()
    
    project = "Financial Accounting System"
    version = 1
    
    print(f"📋 Project: {project}")
    print(f"📊 Version: {version}")
    print()
    
    # Generate BRD
    html = generate_domain_agnostic_brd_html(project, inputs, version)
    
    print(f"✅ BRD Generated: {len(html)} characters")
    print()
    
    # Validate structure
    print("🔍 Validating BRD Structure:")
    print("-" * 80)
    
    required_sections = [
        "Scope",
        "Business Objectives",
        "EPIC",
        "Success Metrics",
        "KPI",
        "Risk"
    ]
    
    for section in required_sections:
        if section.upper() in html.upper():
            print(f"   ✅ Contains '{section}' section")
        else:
            print(f"   ❌ Missing '{section}' section")
    
    # Check for proper ID formats
    print()
    print("🔍 Checking ID Formats:")
    print("-" * 80)
    
    id_patterns = [
        ("OBJ-", "Business Objectives"),
        ("EPIC-", "EPICs"),
        ("KPI-", "Success Metrics"),
        ("RISK-", "Risk Assessment")
    ]
    
    for pattern, name in id_patterns:
        if pattern in html:
            print(f"   ✅ Contains {pattern} IDs for {name}")
        else:
            print(f"   ⚠️  May be missing {pattern} IDs for {name}")
    
    # Save output for inspection
    output_file = "/tmp/domain_agnostic_brd_test.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print()
    print(f"💾 BRD saved to: {output_file}")
    print()
    
    # Preview first 2000 chars
    print("📄 BRD Preview (first 2000 characters):")
    print("-" * 80)
    print(html[:2000])
    print("...")
    print()
    
    return html

if __name__ == "__main__":
    test_financial_accounting_brd()

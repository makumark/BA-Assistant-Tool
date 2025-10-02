#!/usr/bin/env python3
"""
Quick test to verify the BRD generation works through the service layer.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_service_integration():
    """Test BRD generation through service layer."""
    
    from app.services.ai_service import generate_brd_html
    
    # Financial accounting test case
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
    print("🧪 Service Integration Test")
    print("=" * 80)
    print()
    
    project = "Financial Accounting System"
    version = 1
    
    print(f"📋 Project: {project}")
    print(f"📊 Version: {version}")
    print()
    
    print("🔄 Generating BRD through service layer...")
    html = generate_brd_html(project, inputs, version)
    
    print(f"✅ BRD Generated: {len(html):,} characters")
    print()
    
    # Validate key features
    required_features = [
        ("Scope of the Project", "Scope section"),
        ("Business Objectives", "Objectives section"),
        ("EPICs", "EPICs section"),
        ("Success Metrics", "KPIs section"),
        ("Risk Assessment", "Risk section"),
        ("OBJ-", "Objective IDs"),
        ("EPIC-AP-", "Accounts Payable EPIC"),
        ("EPIC-AR-", "Accounts Receivable EPIC"),
        ("EPIC-GL-", "General Ledger EPIC"),
        ("EPIC-BANK-", "Bank & Cash EPIC"),
        ("EPIC-FA-", "Fixed Assets EPIC"),
        ("EPIC-REP-", "Reporting EPIC"),
        ("KPI-", "KPI IDs"),
        ("RISK-", "Risk IDs"),
        ("TBV", "TBV markers"),
        ("Hypothesis:", "Objective hypotheses"),
        ("Problem:", "EPIC problems"),
        ("Value:", "EPIC values"),
        ("Capabilities:", "EPIC capabilities"),
        ("Traceability:", "KPI traceability")
    ]
    
    print("🔍 Validation Checks:")
    print("-" * 80)
    
    all_passed = True
    for pattern, description in required_features:
        if pattern in html:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ MISSING: {description}")
            all_passed = False
    
    print()
    print("=" * 80)
    
    if all_passed:
        print("✅ All validation checks PASSED!")
        print()
        print("The domain-agnostic BRD generator is working correctly through the service layer.")
        print("It provides all required sections with proper structure and traceability.")
        return 0
    else:
        print("❌ Some validation checks FAILED!")
        return 1


if __name__ == "__main__":
    exit_code = test_service_integration()
    sys.exit(exit_code)

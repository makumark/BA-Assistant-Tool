#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.ai_service import generate_brd_html

# Test with your exact banking inputs
test_inputs = {
    "scope": """Project Scope (Included & Excluded)
• Included: retail onboarding (KYC/AML), account opening and servicing, payments and transfers (IMPS/NEFT/RTGS/UPI), cards issuance and lifecycle, deposits/loans module light, bill pay, alerts/notifications, customer support tickets, dashboards and regulatory/audit reporting.
• Excluded (phase 1): treasury/trading platforms, wealth/robo advisory, full loan origination for complex products, branch hardware/POS rollout, and legacy core replacement.""",
    
    "objectives": """Business Objectives
• Reduce account opening turnaround time and drop offs, improve payment straight through processing, decrease support tickets and call AHT, raise digital adoption/active MAU, and strengthen compliance/audit readiness with complete traceability.""",
    
    "budget": """Budget Details
• Estimated ₹1.8–₹3.2 crore for design/build, KYC/AML/sanctions and credit bureau integrations, payments rails connectivity, security and performance testing, deployment/observability, data migration, training/change, and first year run/support; phased MVP → scale.""",
    
    "briefRequirements": """Brief Business Requirements
• Onboarding & KYC: digital forms, document capture, OCR/IDV, sanctions/PEP checks, e sign/e mandate, multi level review and decisioning.
• Accounts & Servicing: savings/current account setup, mandates/nominees, address/contact changes, statements, cheque services.
• Payments: UPI/net banking/NEFT/RTGS/IMPS with beneficiaries, limits, payee management, standing instructions, bill pay and recharge.
• Cards: debit card request, PIN set/reset, domestic/international controls, hotlist/reissue.
• Deposits/Loans (light): FD/RD booking/closure, prepayment simulation; simple personal loan pre eligibility and offer acceptance.
• Notifications & Comms: email/SMS/push for OTPs, transactions, service updates, and campaigns with preference center.
• Support: ticket creation from app, status, SLA timers, knowledge base; secure document upload.
• Reporting & Compliance: regulator returns extracts, suspicious activity flags, complete audit logs and data retention.
• Admin: roles/profiles, parameter/config management (limits, fees, holidays), content/CMS banners.""",
    
    "assumptions": """Assumptions
• KYC/AML, credit bureau, payments, and messaging providers are contracted with sandbox access; policies for privacy, data retention, and consent are approved; SSO and environment parity exist; product, fees, and limit matrices are finalized; core banking and switch/middleware expose stable APIs.""",
    
    "validations": """Validations
• Identity & KYC: mandatory demographics, document number formats, OCR confidence thresholds, liveness/selfie match, sanctions/PEP clearing before activation.
• Payments: beneficiary validation, risk/velocity checks, 2FA/OTP or 3DS where applicable, amount within customer/product limits, idempotency on submission, success callback before posting.
• Accounts & Cards: unique customer/account identifiers, address and PIN policies, card controls consistent with scheme/region; blocked statuses prevent transactions.
• Deposits/Loans: eligibility and limit checks, tenor/amount ranges, premature closure penalties rules, EMI and interest calculations verified.
• Security & Compliance: RBAC enforced for every sensitive action, audit trail for create/read/update/delete, encryption in transit/at rest, session timeout and device binding, WCAG 2.1 AA for customer screens.
• Data Integrity: totals and balances reconcile after each posting; failure paths roll back cleanly with clear user messaging."""
}

def test_brd_generation():
    print("🧪 Testing BRD Generation with Banking Inputs")
    print("=" * 60)
    
    # Test the generation
    result = generate_brd_html("Banking", test_inputs, 1)
    
    print(f"📄 BRD Length: {len(result)} characters")
    print("🔍 Content Analysis:")
    print(f"   - Contains HTML: {'Yes' if '<h' in result else 'No'}")
    print(f"   - Contains EPIC: {'Yes' if 'EPIC-' in result else 'No'}")
    print(f"   - Contains AI Detection: {'Yes' if '🤖 AI DOMAIN DETECTION' in result else 'No'}")
    print(f"   - Contains Fallback marker: {'Yes' if 'enhanced fallback' in result else 'No'}")
    
    # Check if assumptions are being copy-pasted
    original_assumptions = test_inputs["assumptions"]
    if original_assumptions.replace("Assumptions\n• ", "") in result:
        print("❌ ISSUE FOUND: Assumptions are copy-pasted without AI enhancement!")
    else:
        print("✅ Assumptions appear to be AI-enhanced")
    
    # Check business requirements processing
    original_reqs = test_inputs["briefRequirements"]
    if "Onboarding & KYC: digital forms" in result:
        print("❌ ISSUE FOUND: Business Requirements are copy-pasted without proper conversion!")
    else:
        print("✅ Business Requirements appear to be properly processed")
    
    print("\n" + "=" * 60)
    print("📋 First 500 characters of generated BRD:")
    print(result[:500] + "...")
    
    # Save result for inspection
    with open("test_brd_result.html", "w", encoding="utf-8") as f:
        f.write(result)
    print("\n💾 Full result saved to 'test_brd_result.html'")

if __name__ == "__main__":
    test_brd_generation()
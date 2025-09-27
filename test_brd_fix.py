#!/usr/bin/env python3
import requests
import json

# Test BRD generation to see if AI is working
test_data = {
    "project": "Banking",
    "version": 1,
    "inputs": {
        "scope": "Included: retail onboarding (KYC/AML), account opening and servicing, payments and transfers (IMPS/NEFT/RTGS/UPI), cards issuance and lifecycle, deposits/loans module light, bill pay, alerts/notifications, customer support tickets, dashboards and regulatory/audit reporting.",
        "objectives": "Reduce account opening turnaround time and drop offs, improve payment straight through processing, decrease support tickets and call AHT, raise digital adoption/active MAU, and strengthen compliance/audit readiness with complete traceability.",
        "budget": "Estimated ₹1.8–₹3.2 crore for design/build, KYC/AML/sanctions and credit bureau integrations, payments rails connectivity, security and performance testing, deployment/observability, data migration, training/change, and first year run/support; phased MVP → scale.",
        "briefRequirements": "Onboarding & KYC: digital forms, document capture, OCR/IDV, sanctions/PEP checks, e sign/e mandate, multi level review and decisioning. Accounts & Servicing: savings/current account setup, mandates/nominees, address/contact changes, statements, cheque services. Payments: UPI/net banking/NEFT/RTGS/IMPS with beneficiaries, limits, payee management, standing instructions, bill pay and recharge.",
        "assumptions": "KYC/AML, credit bureau, payments, and messaging providers are contracted with sandbox access; policies for privacy, data retention, and consent are approved; SSO and environment parity exist; product, fees, and limit matrices are finalized; core banking and switch/middleware expose stable APIs.",
        "validations": "Identity & KYC: mandatory demographics, document number formats, OCR confidence thresholds, liveness/selfie match, sanctions/PEP clearing before activation. Payments: beneficiary validation, risk/velocity checks, 2FA/OTP or 3DS where applicable, amount within customer/product limits, idempotency on submission, success callback before posting."
    }
}

try:
    print("🚀 Testing BRD generation...")
    response = requests.post("http://localhost:8001/ai/expand", json=test_data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ BRD Generation Response received!")
        print(f"📄 HTML Length: {len(result.get('html', ''))}")
        
        # Check if it contains AI-enhanced content
        html_content = result.get('html', '')
        
        if "🤖 AI DOMAIN DETECTION ACTIVE" in html_content:
            print("✅ AI Enhancement DETECTED!")
        elif "EPIC-" in html_content:
            print("✅ EPIC Structure DETECTED!")
        else:
            print("❌ Appears to be fallback mode (copy-paste)")
            
        # Save to file for inspection
        with open("test_brd_output.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("📁 Saved output to test_brd_output.html")
        
        # Check key sections
        if test_data["inputs"]["assumptions"] in html_content:
            print("❌ PROBLEM: Raw assumptions copy-pasted")
        else:
            print("✅ Assumptions appear to be AI-enhanced")
            
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
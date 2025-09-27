import React, { useState } from "react";

export default function FRDEditor({ projectDefault = "" }) {
  const [project, setProject] = useState(projectDefault);
  const [version, setVersion] = useState(1);
  const [brd, setBrd] = useState("");
  const [html, setHtml] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  
  // Prioritization state
  const [prioritizationData, setPrioritizationData] = useState(null);
  const [prioritizationLoading, setPrioritizationLoading] = useState(false);
  const [prioritizationError, setPrioritizationError] = useState("");
  const [showPrioritization, setShowPrioritization] = useState(false);
  
  // Sample healthcare BRD for demonstration
  const sampleHealthcareBRD = `Executive Summary
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
The system shall ensure compliance with healthcare regulations.

Assumptions
Users will have access to internet-enabled devices; existing hospital infrastructure (network, hardware) is sufficient; regulatory compliance standards (e.g., HIPAA) will guide implementation.

Constraints
Standard regulatory, integration and schedule constraints apply.

Validations & Acceptance Criteria
Enforce Mandatory patient demographic fields (name, DOB).
Enforce valid email.
Enforce contact number formats.
Enforce insurance ID verification.
Enforce appointment slot availability checks.
Enforce billing accuracy checks before confirmation.

Appendices
Appendix A: Glossary
Appendix B: References`;

  async function handleGenerate() {
    setError("");
    if (!project.trim()) {
      setError("Project name is required.");
      return;
    }
    if (!brd.trim()) {
      setError("BRD content is required. Please paste your Business Requirements Document.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8001/ai/frd/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project: project.trim(), brd: brd.trim(), version: Number(version) || 1 }),
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server Error ${res.status}: ${res.statusText}. ${txt}`);
      }
      const data = await res.json();
      setHtml(data.html || "");
    } catch (e) {
      console.error("FRD Generation Error:", e);
      setError(`Failed to generate FRD: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handlePrioritize() {
    setPrioritizationError("");
    
    if (!html.trim()) {
      setPrioritizationError("Please generate an FRD first before prioritizing requirements.");
      return;
    }
    
    setPrioritizationLoading(true);
    try {
      const res = await fetch("http://localhost:8001/ai/frd/prioritize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          project: project.trim(), 
          frd_html: html.trim(), 
          version: Number(version) || 1 
        }),
      });
      
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server Error ${res.status}: ${res.statusText}. ${txt}`);
      }
      
      const data = await res.json();
      setPrioritizationData(data);
      setShowPrioritization(true);
      
    } catch (e) {
      console.error("Prioritization Error:", e);
      setPrioritizationError(`Failed to prioritize requirements: ${e.message}`);
    } finally {
      setPrioritizationLoading(false);
    }
  }

  function handleClear() {
    setBrd("");
    setHtml("");
    setError("");
    setPrioritizationData(null);
    setPrioritizationError("");
    setShowPrioritization(false);
  }
  
  function handleLoadSample() {
    setProject("Healthcare Management System");
    setBrd(sampleHealthcareBRD);
    setError("");
    setHtml("");
  }

  return (
    <div style={{ marginTop: 12 }}>
      {/* Instructions */}
      <div style={{ 
        background: "#f8fafc", 
        border: "1px solid #e2e8f0", 
        borderRadius: "6px", 
        padding: "12px", 
        marginBottom: "16px" 
      }}>
        <h4 style={{ margin: "0 0 8px 0", color: "#374151" }}>How to Use:</h4>
        <ol style={{ margin: 0, paddingLeft: "20px", color: "#6b7280" }}>
          <li>Enter your project name (e.g., "Healthcare Management System", "Banking Platform")</li>
          <li>Paste your complete BRD (Business Requirements Document) in the text area below</li>
          <li>Click "Generate FRD" to let our AI agent convert it to a Functional Requirements Document</li>
          <li>The generated FRD will be domain-agnostic and follow industry standards</li>
        </ol>
      </div>

      {/* Controls */}
      <div style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap", alignItems: "center" }}>
        <input
          style={{ 
            flex: "1", 
            minWidth: "200px", 
            padding: "10px 12px", 
            border: "1px solid #d1d5db", 
            borderRadius: "4px",
            fontSize: "14px" 
          }}
          value={project}
          onChange={(e) => setProject(e.target.value)}
          placeholder="Enter project name (e.g., Healthcare Management System)"
        />
        <label style={{ color: "#6b7280", fontSize: "14px" }}>
          Version:
          <input
            style={{ 
              width: 60, 
              padding: "8px", 
              marginLeft: "6px", 
              border: "1px solid #d1d5db", 
              borderRadius: "4px" 
            }}
            type="number"
            value={version}
            onChange={(e) => setVersion(e.target.value)}
            min={1}
          />
        </label>
      </div>

      {/* Action Buttons */}
      <div style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" }}>
        <button 
          onClick={handleGenerate} 
          disabled={loading} 
          style={{ 
            padding: "10px 16px", 
            background: loading ? "#9ca3af" : "#3b82f6", 
            color: "white", 
            border: "none", 
            borderRadius: "4px",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: "14px",
            fontWeight: "500"
          }}
        >
          {loading ? "🤖 AI Agent Processing..." : "🚀 Generate FRD"}
        </button>
        <button 
          onClick={handlePrioritize} 
          disabled={prioritizationLoading || !html.trim()} 
          style={{ 
            padding: "10px 16px", 
            background: prioritizationLoading ? "#9ca3af" : (!html.trim() ? "#d1d5db" : "#7c3aed"), 
            color: "white", 
            border: "none", 
            borderRadius: "4px",
            cursor: prioritizationLoading ? "not-allowed" : (!html.trim() ? "not-allowed" : "pointer"),
            fontSize: "14px",
            fontWeight: "500"
          }}
          title={!html.trim() ? "Generate FRD first to enable prioritization" : "Prioritize requirements using MoSCoW methodology"}
        >
          {prioritizationLoading ? "🎯 Prioritizing..." : "🎯 Prioritize Requirements"}
        </button>
        <button 
          onClick={handleClear} 
          style={{ 
            padding: "10px 16px", 
            background: "#6b7280", 
            color: "white", 
            border: "none", 
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "14px"
          }}
        >
          Clear All
        </button>
        <button 
          onClick={handleLoadSample} 
          style={{ 
            padding: "10px 16px", 
            background: "#10b981", 
            color: "white", 
            border: "none", 
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "14px"
          }}
        >
          Load Healthcare Sample
        </button>
      </div>

      {/* BRD Input */}
      <div style={{ marginBottom: 16 }}>
        <label style={{ display: "block", marginBottom: "6px", fontWeight: "500", color: "#374151" }}>
          Business Requirements Document (BRD) Input:
        </label>
        <textarea
          value={brd}
          onChange={(e) => setBrd(e.target.value)}
          placeholder="Paste your complete BRD here including:
• Executive Summary
• Project Scope  
• Business Objectives
• Budget Details
• Business Requirements
• Assumptions
• Constraints
• Validations & Acceptance Criteria

The AI agent will analyze your BRD and generate a comprehensive FRD suitable for any domain."
          rows={15}
          style={{ 
            width: "100%", 
            padding: "12px", 
            fontFamily: "monospace", 
            fontSize: "13px",
            border: "1px solid #d1d5db", 
            borderRadius: "4px",
            resize: "vertical",
            minHeight: "300px"
          }}
        />
        <div style={{ fontSize: "12px", color: "#6b7280", marginTop: "4px" }}>
          Characters: {brd.length} | AI agents work best with detailed, well-structured BRDs
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{ 
          color: "#dc2626", 
          background: "#fef2f2", 
          border: "1px solid #fecaca", 
          borderRadius: "4px", 
          padding: "12px", 
          marginBottom: "16px",
          fontSize: "14px"
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Prioritization Error Display */}
      {prioritizationError && (
        <div style={{ 
          color: "#dc2626", 
          background: "#fef2f2", 
          border: "1px solid #fecaca", 
          borderRadius: "4px", 
          padding: "12px", 
          marginBottom: "16px",
          fontSize: "14px"
        }}>
          <strong>Prioritization Error:</strong> {prioritizationError}
        </div>
      )}

      {/* FRD Output */}
      <div style={{ marginTop: 16 }}>
        <h4 style={{ margin: "0 0 12px 0", color: "#374151" }}>
          Generated FRD (Functional Requirements Document)
        </h4>
        <div
          style={{
            border: "1px solid #e5e7eb",
            borderRadius: "6px",
            padding: "16px",
            minHeight: 150,
            background: "#fff",
            boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
          }}
          dangerouslySetInnerHTML={{ __html: html || '<p style="color: #9ca3af; font-style: italic;">Generated FRD will appear here after clicking "Generate FRD". The AI agent will transform your BRD into a structured FRD with functional requirements, NFRs, data models, and acceptance criteria.</p>' }}
        />
      </div>

      {/* Prioritization Results */}
      {showPrioritization && prioritizationData && (
        <div style={{ marginTop: 24 }}>
          <div style={{ 
            display: "flex", 
            justifyContent: "space-between", 
            alignItems: "center", 
            marginBottom: 16 
          }}>
            <h4 style={{ margin: 0, color: "#374151" }}>
              🎯 Requirement Prioritization Results
            </h4>
            <button
              onClick={() => setShowPrioritization(false)}
              style={{
                padding: "6px 12px",
                background: "#6b7280",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "12px"
              }}
            >
              Hide Prioritization
            </button>
          </div>

          {/* Executive Summary */}
          <div style={{ 
            display: "grid", 
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", 
            gap: 16, 
            marginBottom: 24 
          }}>
            <div style={{ 
              background: "#f8fafc", 
              padding: 16, 
              borderRadius: 8, 
              borderLeft: "4px solid #10b981" 
            }}>
              <h5 style={{ margin: "0 0 8px 0", color: "#065f46" }}>Total Requirements</h5>
              <p style={{ margin: 0, fontSize: 24, fontWeight: "bold", color: "#065f46" }}>
                {prioritizationData.total_requirements}
              </p>
              <p style={{ margin: "4px 0 0 0", fontSize: 12, color: "#6b7280" }}>
                Domain: {prioritizationData.domain}
              </p>
            </div>
            
            <div style={{ 
              background: "#fef3f2", 
              padding: 16, 
              borderRadius: 8, 
              borderLeft: "4px solid #dc2626" 
            }}>
              <h5 style={{ margin: "0 0 8px 0", color: "#7f1d1d" }}>Must Have</h5>
              <p style={{ margin: 0, fontSize: 24, fontWeight: "bold", color: "#7f1d1d" }}>
                {prioritizationData.moscow_distribution.counts["Must Have"]} 
                ({prioritizationData.moscow_distribution.percentages["Must Have"]}%)
              </p>
            </div>
            
            <div style={{ 
              background: "#fff7ed", 
              padding: 16, 
              borderRadius: 8, 
              borderLeft: "4px solid #ea580c" 
            }}>
              <h5 style={{ margin: "0 0 8px 0", color: "#9a3412" }}>Should Have</h5>
              <p style={{ margin: 0, fontSize: 24, fontWeight: "bold", color: "#9a3412" }}>
                {prioritizationData.moscow_distribution.counts["Should Have"]} 
                ({prioritizationData.moscow_distribution.percentages["Should Have"]}%)
              </p>
            </div>
            
            <div style={{ 
              background: "#f0f9ff", 
              padding: 16, 
              borderRadius: 8, 
              borderLeft: "4px solid #0284c7" 
            }}>
              <h5 style={{ margin: "0 0 8px 0", color: "#0c4a6e" }}>Could Have</h5>
              <p style={{ margin: 0, fontSize: 24, fontWeight: "bold", color: "#0c4a6e" }}>
                {prioritizationData.moscow_distribution.counts["Could Have"]} 
                ({prioritizationData.moscow_distribution.percentages["Could Have"]}%)
              </p>
            </div>
          </div>

          {/* Prioritized Requirements Table */}
          <div style={{ marginBottom: 24 }}>
            <h5 style={{ margin: "0 0 12px 0", color: "#374151" }}>📋 Prioritized Requirements</h5>
            <div style={{ 
              border: "1px solid #e5e7eb", 
              borderRadius: 6, 
              overflow: "hidden",
              background: "#fff" 
            }}>
              <div style={{ 
                background: "#f9fafb", 
                padding: "12px 16px", 
                borderBottom: "1px solid #e5e7eb",
                fontWeight: "600",
                fontSize: "14px",
                display: "grid",
                gridTemplateColumns: "auto 1fr auto auto auto auto",
                gap: 16
              }}>
                <div>Rank</div>
                <div>User Story</div>
                <div>MoSCoW</div>
                <div>Score</div>
                <div>Complexity</div>
                <div>Dependencies</div>
              </div>
              
              {prioritizationData.prioritized_requirements.slice(0, 10).map((req, idx) => {
                const categoryColors = {
                  "Must Have": "#dc2626",
                  "Should Have": "#ea580c", 
                  "Could Have": "#0284c7",
                  "Won't Have (this time)": "#6b7280"
                };
                const color = categoryColors[req.moscow_category] || "#6b7280";
                
                return (
                  <div key={req.id} style={{ 
                    padding: "12px 16px", 
                    borderBottom: idx < 9 ? "1px solid #f3f4f6" : "none",
                    display: "grid",
                    gridTemplateColumns: "auto 1fr auto auto auto auto",
                    gap: 16,
                    alignItems: "center",
                    fontSize: "13px"
                  }}>
                    <div style={{ fontWeight: "600", color: "#374151" }}>#{req.priority_rank}</div>
                    <div>
                      <div style={{ fontWeight: "500", marginBottom: 4 }}>
                        {req.id}: {req.role}
                      </div>
                      <div style={{ color: "#6b7280", fontSize: "12px" }}>
                        "{req.goal.substring(0, 50)}{req.goal.length > 50 ? '...' : ''}"
                      </div>
                    </div>
                    <div>
                      <span style={{ 
                        background: color, 
                        color: "white", 
                        padding: "2px 8px", 
                        borderRadius: "12px", 
                        fontSize: "11px",
                        fontWeight: "500"
                      }}>
                        {req.moscow_category}
                      </span>
                    </div>
                    <div style={{ fontWeight: "600", color: "#374151" }}>{req.priority_score}</div>
                    <div style={{ color: "#6b7280" }}>{req.complexity}</div>
                    <div style={{ color: "#6b7280" }}>{req.dependencies.length}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Full Report */}
          <div style={{ marginBottom: 16 }}>
            <h5 style={{ margin: "0 0 12px 0", color: "#374151" }}>📄 Detailed Prioritization Report</h5>
            <div
              style={{
                border: "1px solid #e5e7eb",
                borderRadius: "6px",
                padding: "16px",
                background: "#fff",
                boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
                maxHeight: "600px",
                overflowY: "auto"
              }}
              dangerouslySetInnerHTML={{ __html: prioritizationData.report_html }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
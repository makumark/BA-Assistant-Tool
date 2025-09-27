import React from "react";
import FRDEditor from "../components/FRDEditor";

export default function FRDPage({ initialProject }) {
  const projectDefault =
    initialProject ||
    (() => {
      try {
        const params = new URLSearchParams(window.location.search);
        return params.get("project") || "Banking";
      } catch {
        return "Banking";
      }
    })();

  return (
    <div style={{ padding: 20 }}>
      <header style={{ marginBottom: 12 }}>
        <h2 style={{ margin: 0 }}>FRD Generation</h2>
        <p style={{ marginTop: 6, color: "#6b7280" }}>
          Paste the BRD below and click "Generate FRD".
        </p>
      </header>

      <FRDEditor projectDefault={projectDefault} />
    </div>
  );
}
import React, { useState } from 'react';

const WireframeGenerator = ({ 
  projectName = 'Test Project', 
  frdContent = '', 
  userStories = [], 
  onWireframeGenerated,
  isPrototypeMode = false 
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [wireframeHtml, setWireframeHtml] = useState('');
  const [prototypeHtml, setPrototypeHtml] = useState('');
  const [error, setError] = useState('');
  const [domain, setDomain] = useState('generic');
  const [inputFrdContent, setInputFrdContent] = useState(frdContent || '');
  const [inputMode, setInputMode] = useState('frd'); // 'frd' or 'stories'
  const [outputType, setOutputType] = useState(isPrototypeMode ? 'prototype' : 'wireframes'); // 'wireframes' or 'prototype'
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');

  const domains = [
    'generic', 'healthcare', 'education', 'ecommerce', 
    'banking', 'financial', 'marketing', 'logistics', 'insurance'
  ];

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    const reader = new FileReader();
    
    reader.onload = (e) => {
      const content = e.target.result;
      setFileContent(content);
      setInputFrdContent(content);
      console.log(`📁 File uploaded: ${file.name} (${content.length} characters)`);
    };

    reader.onerror = () => {
      setError('Failed to read the uploaded file. Please try again.');
    };

    if (file.type === 'text/html' || file.name.toLowerCase().endsWith('.html')) {
      reader.readAsText(file);
    } else if (file.type === 'text/plain' || file.name.toLowerCase().endsWith('.txt')) {
      reader.readAsText(file);
    } else {
      reader.readAsText(file); // Try to read as text anyway
    }
  };

  const clearUploadedFile = () => {
    setUploadedFile(null);
    setFileContent('');
    setInputFrdContent('');
    const fileInput = document.getElementById('frd-file-upload');
    if (fileInput) fileInput.value = '';
  };

  const generateWireframes = async () => {
    if (!projectName) {
      setError('Project name is required');
      return;
    }

    const currentFrdContent = inputFrdContent || frdContent || fileContent;
    
    if (inputMode === 'frd' && !currentFrdContent) {
      setError('FRD content is required when using FRD mode. Please upload a file or paste content in the textarea.');
      return;
    }
    
    if (inputMode === 'stories' && (!userStories || userStories.length === 0)) {
      setError('User stories are required when using Stories mode');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const axios = (await import('axios')).default;
      const payload = {
        project: projectName,
        domain: domain
      };

      // Add content based on input mode
      if (inputMode === 'frd') {
        payload.frd_content = currentFrdContent;
      } else {
        payload.user_stories = userStories;
      }

      console.log(`🔄 Generating ${outputType}...`, payload);

      const endpoint = outputType === 'prototype' ? '/ai/prototype' : '/ai/wireframes';
      const response = await axios.post(
        `http://localhost:8001${endpoint}`,
        payload,
        {
          timeout: 30000,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      const result = response.data;
      const htmlContent = result.html || '';

      if (outputType === 'prototype') {
        setPrototypeHtml(htmlContent);
      } else {
        setWireframeHtml(htmlContent);
      }
      
      // Save generated content to a downloadable file
      const blob = new Blob([htmlContent], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      
      // Auto-download the generated file
      const link = document.createElement('a');
      link.href = url;
      link.download = `${projectName.replace(/\s+/g, '_')}_${outputType}.html`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      if (onWireframeGenerated) {
        onWireframeGenerated(htmlContent, result.domain);
      }

      console.log(`✅ ${outputType} generated successfully!`);

    } catch (err) {
      console.error(`❌ Error generating ${outputType}:`, err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        `Failed to generate ${outputType}. Please try again.`
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadWireframes = () => {
    if (!wireframeHtml) return;

    const blob = new Blob([wireframeHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${projectName.replace(/\s+/g, '_')}_wireframes.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const previewWireframes = () => {
    if (!wireframeHtml) return;

    // Open wireframes in a new window for preview
    const newWindow = window.open('', '_blank');
    if (newWindow) {
      newWindow.document.write(wireframeHtml);
      newWindow.document.close();
    }
  };

  return (
    <div className="wireframe-generator">
      <div className="wireframe-header">
        <h2>🎨 Wireframe Generator</h2>
        <p>Generate interactive wireframes from user stories or FRD content</p>
      </div>

      <div className="wireframe-controls">
        <div className="control-row">
          <div className="domain-selector">
            <label htmlFor="domain-select">Domain:</label>
            <select 
              id="domain-select"
              value={domain} 
              onChange={(e) => setDomain(e.target.value)}
              className="domain-dropdown"
            >
              {domains.map(d => (
                <option key={d} value={d}>
                  {d.charAt(0).toUpperCase() + d.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="input-mode-selector">
            <label>Input Method:</label>
            <div className="mode-buttons">
              <button
                type="button"
                className={`mode-button ${inputMode === 'frd' ? 'active' : ''}`}
                onClick={() => setInputMode('frd')}
              >
                📄 FRD Content
              </button>
              <button
                type="button"
                className={`mode-button ${inputMode === 'stories' ? 'active' : ''}`}
                onClick={() => setInputMode('stories')}
              >
                📋 User Stories
              </button>
            </div>
          </div>
        </div>

        {inputMode === 'frd' && (
          <div className="frd-input-section">
            <label htmlFor="frd-content">FRD Content:</label>
            
            <div className="file-upload-section">
              <input
                type="file"
                id="frd-file-upload"
                accept=".html,.txt,.doc,.docx"
                onChange={handleFileUpload}
                className="file-input"
              />
              <label htmlFor="frd-file-upload" className="file-upload-label">
                📁 Upload FRD File
              </label>
              {uploadedFile && (
                <div className="uploaded-file-info">
                  <span className="file-name">✅ {uploadedFile.name}</span>
                  <button 
                    type="button" 
                    onClick={clearUploadedFile} 
                    className="clear-file-btn"
                  >
                    ✖
                  </button>
                </div>
              )}
            </div>

            <div className="divider">OR</div>

            <textarea
              id="frd-content"
              value={inputFrdContent}
              onChange={(e) => setInputFrdContent(e.target.value)}
              placeholder="Paste your Functional Requirements Document (FRD) content here..."
              className="frd-textarea"
              rows={8}
            />
          </div>
        )}

        {inputMode === 'stories' && (
          <div className="stories-info">
            <p className="info-text">
              📋 Using provided user stories from previous FRD generation
              {userStories && userStories.length > 0 
                ? ` (${userStories.length} stories found)` 
                : ' (No user stories available)'}
            </p>
          </div>
        )}

        <div className="output-type-selector">
          <label>Output Type:</label>
          <div className="mode-buttons">
            <button
              type="button"
              className={`mode-button ${outputType === 'wireframes' ? 'active' : ''}`}
              onClick={() => setOutputType('wireframes')}
            >
              🎨 Wireframes
            </button>
            <button
              type="button"
              className={`mode-button ${outputType === 'prototype' ? 'active' : ''}`}
              onClick={() => setOutputType('prototype')}
            >
              🎯 Interactive Prototype
            </button>
          </div>
        </div>

        <button
          onClick={generateWireframes}
          disabled={isGenerating || !projectName}
          className={`generate-button ${isGenerating ? 'generating' : ''}`}
        >
          {isGenerating ? (
            <>
              <span className="spinner"></span>
              Generating {outputType === 'prototype' ? 'Prototype' : 'Wireframes'}...
            </>
          ) : (
            `Generate ${outputType === 'prototype' ? 'Interactive Prototype' : 'Wireframes'}`
          )}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {wireframeHtml && (
        <div className="wireframe-results">
          <div className="results-header">
            <h3>✅ Wireframes Generated Successfully!</h3>
            <p>Interactive wireframes with {Math.floor(wireframeHtml.length / 1000)}K+ characters</p>
          </div>

          <div className="wireframe-actions">
            <button onClick={previewWireframes} className="preview-button">
              👁️ Preview Wireframes
            </button>
            <button onClick={downloadWireframes} className="download-button">
              💾 Download HTML File
            </button>
          </div>

          <div className="wireframe-preview">
            <h4>Features Generated:</h4>
            <ul className="feature-list">
              {wireframeHtml.includes('login') && <li>🔐 Login Page</li>}
              {wireframeHtml.includes('dashboard') && <li>📊 Dashboard</li>}
              {wireframeHtml.includes('form-field') && <li>📝 Forms</li>}
              {wireframeHtml.includes('nav-item') && <li>🧭 Navigation</li>}
              {wireframeHtml.includes('onclick') && <li>⚡ Interactive Elements</li>}
              {wireframeHtml.includes('responsive') && <li>📱 Responsive Design</li>}
            </ul>
          </div>
        </div>
      )}

      <style jsx>{`
        .wireframe-generator {
          background: white;
          border-radius: 8px;
          padding: 24px;
          margin: 20px 0;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .wireframe-header {
          text-align: center;
          margin-bottom: 24px;
        }

        .wireframe-header h2 {
          color: #2d3748;
          margin-bottom: 8px;
        }

        .wireframe-header p {
          color: #718096;
        }

        .wireframe-controls {
          display: flex;
          flex-direction: column;
          gap: 20px;
          margin-bottom: 20px;
        }

        .control-row {
          display: flex;
          gap: 16px;
          align-items: center;
          justify-content: center;
          flex-wrap: wrap;
        }

        .domain-selector {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .input-mode-selector {
          display: flex;
          flex-direction: column;
          gap: 8px;
          align-items: center;
        }

        .output-type-selector {
          display: flex;
          flex-direction: column;
          gap: 8px;
          align-items: center;
        }

        .mode-buttons {
          display: flex;
          gap: 8px;
        }

        .mode-button {
          padding: 8px 16px;
          border: 1px solid #e2e8f0;
          border-radius: 6px;
          background: white;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }

        .mode-button.active {
          background: #4299e1;
          color: white;
          border-color: #4299e1;
        }

        .mode-button:hover:not(.active) {
          background: #f7fafc;
          border-color: #cbd5e0;
        }

        .frd-input-section {
          width: 100%;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .frd-input-section label {
          font-weight: 500;
          color: #2d3748;
        }

        .file-upload-section {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 8px;
        }

        .file-input {
          display: none;
        }

        .file-upload-label {
          background: #4299e1;
          color: white;
          padding: 10px 20px;
          border-radius: 6px;
          cursor: pointer;
          transition: background-color 0.2s;
          font-size: 14px;
          font-weight: 500;
          border: none;
        }

        .file-upload-label:hover {
          background: #3182ce;
        }

        .uploaded-file-info {
          display: flex;
          align-items: center;
          gap: 8px;
          background: #f0fff4;
          padding: 8px 12px;
          border-radius: 4px;
          border: 1px solid #68d391;
        }

        .file-name {
          color: #2f855a;
          font-size: 14px;
          font-weight: 500;
        }

        .clear-file-btn {
          background: #fed7d7;
          color: #e53e3e;
          border: none;
          border-radius: 4px;
          padding: 4px 8px;
          cursor: pointer;
          font-size: 12px;
          font-weight: bold;
        }

        .clear-file-btn:hover {
          background: #fbb6ce;
        }

        .divider {
          text-align: center;
          color: #a0aec0;
          font-weight: 500;
          margin: 12px 0;
          position: relative;
        }

        .divider::before,
        .divider::after {
          content: '';
          position: absolute;
          top: 50%;
          width: 40%;
          height: 1px;
          background: #e2e8f0;
        }

        .divider::before {
          left: 0;
        }

        .divider::after {
          right: 0;
        }

        .frd-textarea {
          width: 100%;
          padding: 12px;
          border: 1px solid #e2e8f0;
          border-radius: 6px;
          font-family: system-ui, -apple-system, sans-serif;
          font-size: 14px;
          line-height: 1.5;
          resize: vertical;
          min-height: 200px;
        }

        .frd-textarea:focus {
          outline: none;
          border-color: #4299e1;
          box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }

        .stories-info {
          width: 100%;
          text-align: center;
          padding: 16px;
          background: #f7fafc;
          border-radius: 6px;
          border: 1px solid #e2e8f0;
        }

        .info-text {
          margin: 0;
          color: #4a5568;
          font-size: 14px;
        }

        .domain-dropdown {
          padding: 8px 12px;
          border: 1px solid #e2e8f0;
          border-radius: 6px;
          background: white;
          font-size: 14px;
          min-width: 120px;
        }

        .generate-button {
          background: #4299e1;
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 6px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .generate-button:hover:not(:disabled) {
          background: #3182ce;
          transform: translateY(-1px);
        }

        .generate-button:disabled {
          background: #a0aec0;
          cursor: not-allowed;
          transform: none;
        }

        .generate-button.generating {
          background: #805ad5;
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid transparent;
          border-top: 2px solid white;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .error-message {
          background: #fed7d7;
          color: #c53030;
          padding: 12px;
          border-radius: 6px;
          border: 1px solid #feb2b2;
          margin: 16px 0;
          text-align: center;
        }

        .wireframe-results {
          background: #f7fafc;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          padding: 20px;
          margin-top: 20px;
        }

        .results-header {
          text-align: center;
          margin-bottom: 20px;
        }

        .results-header h3 {
          color: #38a169;
          margin-bottom: 8px;
        }

        .results-header p {
          color: #718096;
          font-size: 14px;
        }

        .wireframe-actions {
          display: flex;
          gap: 12px;
          justify-content: center;
          margin-bottom: 20px;
          flex-wrap: wrap;
        }

        .preview-button, .download-button {
          padding: 10px 20px;
          border: none;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .preview-button {
          background: #805ad5;
          color: white;
        }

        .preview-button:hover {
          background: #6b46c1;
        }

        .download-button {
          background: #38a169;
          color: white;
        }

        .download-button:hover {
          background: #2f855a;
        }

        .wireframe-preview {
          background: white;
          padding: 16px;
          border-radius: 6px;
          border: 1px solid #e2e8f0;
        }

        .wireframe-preview h4 {
          color: #2d3748;
          margin-bottom: 12px;
        }

        .feature-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
          gap: 8px;
          list-style: none;
          margin: 0;
          padding: 0;
        }

        .feature-list li {
          background: #ebf8ff;
          color: #2b6cb0;
          padding: 8px 12px;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
        }
      `}</style>
    </div>
  );
};

export default WireframeGenerator;
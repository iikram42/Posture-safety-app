import React, { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0] || null;

    setResult(null);
    setError("");

    if (!selected) {
      setFile(null);
      setPreviewUrl("");
      return;
    }

    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!file) {
      setError("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `HTTP error ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(`Prediction failed: ${err.message || "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const renderProbabilities = () => {
    if (!result?.probabilities) return null;

    const entries = Object.entries(result.probabilities);

    return (
      <ul className="prob-list">
        {entries.map(([cls, prob]) => (
          <li key={cls}>
            <span className="prob-class">{cls}</span>
            <span className="prob-value">
              {(prob * 100).toFixed(2)}%
            </span>
          </li>
        ))}
      </ul>
    );
  };

  const renderRiskBadge = () => {
    if (!result) return null;

    const { predicted_class, unsafe_score } = result;
    const percentage = (unsafe_score * 100).toFixed(1);
    const isUnsafe = predicted_class.toLowerCase() === "unsafe";

    return (
      <div className={`risk-badge ${isUnsafe ? "risk-unsafe" : "risk-safe"}`}>
        <div className="risk-title">
          {isUnsafe ? "UNSAFE POSTURE" : "SAFE POSTURE"}
        </div>
        <div className="risk-score">
          Unsafe score: <strong>{percentage}%</strong>
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <h1>Posture Safety Classifier</h1>
          <p>
            Upload a frame or image. The model will classify it as{" "}
            <strong>safe</strong> or <strong>unsafe</strong> and report the
            unsafe probability.
          </p>
        </header>

        <main className="app-main">
          <section className="card">
            <h2>1. Upload Image</h2>
            <form onSubmit={handleSubmit}>
              <label className="file-label">
                <span>Select posture image</span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                />
              </label>

              {previewUrl && (
                <div className="preview">
                  <p>Preview:</p>
                  <img src={previewUrl} alt="preview" />
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="submit-btn"
              >
                {loading ? "Analyzing..." : "Run Safety Check"}
              </button>
            </form>

            {error && <div className="error-msg">{error}</div>}
          </section>

          {result && (
            <section className="card">
              <h2>2. Model Output</h2>

              {renderRiskBadge()}

              <div className="output-row">
                <span className="output-label">Predicted class:</span>
                <span className="output-value">
                  {result.predicted_class.toUpperCase()}
                </span>
              </div>

              <div className="output-row">
                <span className="output-label">Device:</span>
                <span className="output-value">{result.device}</span>
              </div>

              <div className="output-row">
                <span className="output-label">Probabilities:</span>
              </div>

              {renderProbabilities()}
            </section>
          )}
        </main>

        <footer className="app-footer">
          <span>Backend: {API_URL}</span>
        </footer>
      </div>
    </div>
  );
}

export default App;

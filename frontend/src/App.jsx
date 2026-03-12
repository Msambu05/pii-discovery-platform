import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [stats, setStats] = useState(null);
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  const [findings, setFindings] = useState([]);
  const [inputText, setInputText] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const API_BASE = "http://127.0.0.1:8000/api";

  useEffect(() => {
    loadData();
  }, []);

  // Load dashboard data
  const loadData = async () => {
    try {
      const statsResponse = await axios.get(`${API_BASE}/dashboard-stats/`);
      setStats(statsResponse.data);

      const scansResponse = await axios.get(`${API_BASE}/scans/`);
      setScans(scansResponse.data);
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  const fetchFindings = async (scanId) => {
    try {
      const response = await axios.get(`${API_BASE}/scans/${scanId}/findings/`);
      setFindings(response.data);
      setSelectedScan(scanId);
    } catch (error) {
      console.error("Error loading findings:", error);
    }
  };

  // Upload CSV
  const uploadCSV = async () => {
    if (!selectedFile) {
      alert("Please select a CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await axios.post(`${API_BASE}/scan-csv/`, formData);

      setSelectedFile(null);
      await loadData(); // refresh dashboard
      alert("CSV scanned successfully");
    } catch (error) {
      console.error("Error uploading CSV:", error);
    }
  };

  // Scan text function
  const runTextScan = async () => {
    if (!inputText.trim()) {
      alert("Please enter text to scan");
      return;
    }

    try {
      await axios.post(`${API_BASE}/scan-text/`, {
        text: inputText,
      });

      setInputText("");
      await loadData(); // refresh dashboard
    } catch (error) {
      console.error("Error running text scan:", error);
    }
  };

  if (!stats) return <div>Loading...</div>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>PII Discovery Dashboard</h1>

      <hr />
      {/*Text scan section*/}
      <h2>Scan Text</h2>

      <textarea
        rows="4"
        cols="60"
        placeholder="Paste text to scan for PII..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />

      <br />

      <button
        type="button"
        onClick={runTextScan}
        style={{ marginTop: "10px" }}
      >
        Run Text Scan
      </button>

      {/* CSV Upload Section */}
      <hr />
      <h2>Upload CSV File</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />

      <br />

      <button
        type="button"
        onClick={uploadCSV}
        style={{ marginTop: "10px" }}
      >
        Upload & Scan CSV
      </button>

      <hr />

      {/* Stats */}
      <h2>Statistics</h2>
      <p>Total Scans: {stats.total_scans}</p>
      <p>Total Findings: {stats.total_findings}</p>
      <p>High Risk: {stats.risk_distribution.high}</p>
      <p>Medium Risk: {stats.risk_distribution.medium}</p>
      <p>Low Risk: {stats.risk_distribution.low}</p>

      <hr />

      {/* Scans */}
      <h2>Scans</h2>
      <ul>
        {scans.map((scan) => (
          <li key={scan.id}>
            Scan #{scan.id} — {scan.status} — Findings: {scan.total_findings}

            <button
              style={{ marginLeft: "10px" }}
              onClick={() => fetchFindings(scan.id)}
            >
              View Findings
            </button>
          </li>
        ))}
      </ul>

      {/* Findings */}
      {selectedScan && (
        <>
          <hr />
          <h2>Findings for Scan #{selectedScan}</h2>

          <ul>
            {findings.map((finding) => (
              <li key={finding.id}>
                {finding.pii_type} — {finding.masked_value} — Risk: {finding.risk_level}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
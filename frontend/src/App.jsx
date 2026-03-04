import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [stats, setStats] = useState(null);
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  const [findings, setFindings] = useState([]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(true);

  const API_BASE = "http://127.0.0.1:8000/api";

  // Load dashboard data
  const loadData = async () => {
    try {
      setLoading(true);

      const statsResponse = await axios.get(`${API_BASE}/dashboard-stats/`);
      setStats(statsResponse.data);

      const scansResponse = await axios.get(`${API_BASE}/scans/`);
      setScans(scansResponse.data);

      setLoading(false);
    } catch (error) {
      console.error("Error loading data:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const fetchFindings = async (scanId) => {
    try {
      const response = await axios.get(`${API_BASE}/scans/${scanId}/findings/`);
      setFindings(response.data);
      setSelectedScan(scanId);
    } catch (error) {
      console.error("Error loading findings:", error);
    }
  };

  const runScan = async () => {
    if (!inputText.trim()) return;

    try {
      await axios.post(`${API_BASE}/scan-text/`, {
        text: inputText,
      });

      setInputText("");
      await loadData(); // refresh dashboard after scan
    } catch (error) {
      console.error("Error running scan:", error);
    }
  };

  if (loading) return <div style={{ padding: "20px" }}>Loading dashboard...</div>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>PII Discovery Dashboard</h1>

      {/* Scan Input Section */}
      <hr />
      <h2>Run New Scan</h2>
      <textarea
        rows="4"
        cols="60"
        placeholder="Paste text to scan..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <br />
      <button onClick={runScan} style={{ marginTop: "10px" }}>
        Run Scan
      </button>

      <hr />

      {/* Stats Section */}
      <h2>Statistics</h2>
      <p>Total Scans: {stats.total_scans}</p>
      <p>Total Findings: {stats.total_findings}</p>
      <p>High Risk: {stats.risk_distribution.high}</p>
      <p>Medium Risk: {stats.risk_distribution.medium}</p>
      <p>Low Risk: {stats.risk_distribution.low}</p>

      <hr />

      {/* Scans Section */}
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

      {/* Findings Section */}
      {selectedScan && (
        <>
          <hr />
          <h2>Findings for Scan #{selectedScan}</h2>
          <ul>
            {findings.map((finding) => (
              <li key={finding.id}>
                {finding.pii_type} — {finding.masked_value} — Risk:{" "}
                {finding.risk_level}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
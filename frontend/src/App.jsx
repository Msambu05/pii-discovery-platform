import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [stats, setStats] = useState(null);
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  const [findings, setFindings] = useState([]);

  const API_BASE = "http://127.0.0.1:8000/api";

  useEffect(() => {
    fetchStats();
    fetchScans();
  }, []);

  const fetchStats = async () => {
    const response = await axios.get(`${API_BASE}/dashboard-stats/`);
    setStats(response.data);
  };

  const fetchScans = async () => {
    const response = await axios.get(`${API_BASE}/scans/`);
    setScans(response.data);
  };

  const fetchFindings = async (scanId) => {
    const response = await axios.get(`${API_BASE}/scans/${scanId}/findings/`);
    setFindings(response.data);
    setSelectedScan(scanId);
  };

  if (!stats) return <div>Loading...</div>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>PII Discovery Dashboard</h1>

      <h2>Statistics</h2>
      <p>Total Scans: {stats.total_scans}</p>
      <p>Total Findings: {stats.total_findings}</p>
      <p>High Risk: {stats.risk_distribution.high}</p>
      <p>Medium Risk: {stats.risk_distribution.medium}</p>
      <p>Low Risk: {stats.risk_distribution.low}</p>

      <hr />

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
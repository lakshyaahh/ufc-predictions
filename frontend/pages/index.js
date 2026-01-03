import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function DisclaimerBanner() {
  return (
    <div style={{
      backgroundColor: "#FFF3CD",
      border: "1px solid #FFC107",
      color: "#856404",
      padding: "12px 20px",
      textAlign: "center",
      fontSize: "14px",
      marginBottom: "20px"
    }}>
      ⚠️ <strong>Disclaimer:</strong> These predictions are for entertainment and analytical purposes only. Not gambling advice. Always make informed decisions.
    </div>
  );
}

function PredictionCounter({ free, isPremium }) {
  if (isPremium) {
    return (
      <div style={{
        backgroundColor: "#E8F5E9",
        border: "2px solid #4CAF50",
        padding: "12px 20px",
        borderRadius: "8px",
        textAlign: "center",
        marginBottom: "20px"
      }}>
        ✨ <strong>PREMIUM MEMBER</strong> - Unlimited predictions
      </div>
    );
  }
  
  return (
    <div style={{
      backgroundColor: "#E3F2FD",
      border: "2px solid #2196F3",
      padding: "12px 20px",
      borderRadius: "8px",
      textAlign: "center",
      marginBottom: "20px"
    }}>
      📊 <strong>Free Predictions Left:</strong> {free}/3 • <Link href="/premium"><a style={{color: "#2196F3", textDecoration: "underline"}}>Upgrade to Premium</a></Link>
    </div>
  );
}

function PredictionTable({ rows }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 10 }}>
      <thead>
        <tr style={{ backgroundColor: "#f0f0f0" }}>
          <th style={{ border: "1px solid #ddd", padding: 8, textAlign: "left" }}>Red Fighter</th>
          <th style={{ border: "1px solid #ddd", padding: 8, textAlign: "left" }}>Blue Fighter</th>
          <th style={{ border: "1px solid #ddd", padding: 8 }}>Red %</th>
          <th style={{ border: "1px solid #ddd", padding: 8 }}>Blue %</th>
          <th style={{ border: "1px solid #ddd", padding: 8 }}>Winner</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={i}>
            <td style={{ border: "1px solid #ddd", padding: 8 }}>{r.red_fighter}</td>
            <td style={{ border: "1px solid #ddd", padding: 8 }}>{r.blue_fighter}</td>
            <td style={{ border: "1px solid #ddd", padding: 8, textAlign: "center" }}>
              {Math.round((r.prob_RedFighter || 0) * 100)}%
            </td>
            <td style={{ border: "1px solid #ddd", padding: 8, textAlign: "center" }}>
              {Math.round((r.prob_BlueFighter || 0) * 100)}%
            </td>
            <td style={{ border: "1px solid #ddd", padding: 8, textAlign: "center" }}>{r.predicted_winner}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function Home() {
  const [token, setToken] = useState(null);
  const [result, setResult] = useState(null);

  const refresh = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/results", {
        headers: { "Authorization": `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to fetch results");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif", maxWidth: 1200, margin: "0 auto" }}>
      <h1>🥊 UFC Predictions</h1>
      {token && <p style={{ color: "green" }}>✅ Authenticated</p>}
      <UploadForm onDone={() => refresh()} />
      <button onClick={refresh} style={{ padding: "8px 16px", marginBottom: 10, cursor: "pointer" }}>
        📊 Refresh Results
      </button>
      {result && <ProbabilityChart data={result} />}
      {result && <PredictionTable rows={result} />}
    </div>
  );
}
  const [error, setError] = useState(null);

  const handleGetPrediction = async () => {
    if (!match) return;
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          match_id: match.id,
          red_fighter: match.red_fighter,
          blue_fighter: match.blue_fighter,
          red_stats: match.red_stats,
          blue_stats: match.blue_stats
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Prediction failed");
      }

      const data = await res.json();
      setPrediction(data);
      onPredictDone && onPredictDone(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (prediction) {
    return (
      <div style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0,0,0,0.7)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000
      }}>
        <div style={{
          backgroundColor: "white",
          borderRadius: "12px",
          padding: "24px",
          maxWidth: "500px",
          width: "90%"
        }}>
          <h2 style={{ marginTop: 0 }}>Prediction Result</h2>
          
          <div style={{ marginBottom: "20px" }}>
            <div style={{ marginBottom: "12px" }}>
              <strong>{match.red_fighter}</strong> vs <strong>{match.blue_fighter}</strong>
            </div>
            
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
              <div style={{ textAlign: "center", padding: "12px", backgroundColor: "#F5F5F5", borderRadius: "8px" }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#FF6B6B" }}>
                  {(prediction.red_probability * 100).toFixed(1)}%
                </div>
                <div style={{ fontSize: "12px", color: "#666" }}>{match.red_fighter}</div>
              </div>
              
              <div style={{ textAlign: "center", padding: "12px", backgroundColor: "#F5F5F5", borderRadius: "8px" }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#4ECDC4" }}>
                  {(prediction.blue_probability * 100).toFixed(1)}%
                </div>
                <div style={{ fontSize: "12px", color: "#666" }}>{match.blue_fighter}</div>
              </div>
            </div>

            <div style={{ backgroundColor: "#E8F5E9", padding: "12px", borderRadius: "8px", marginBottom: "16px" }}>
              <strong>Predicted Winner:</strong> {prediction.predicted_winner}
            </div>

            <div style={{ fontSize: "12px", color: "#666" }}>
              <strong>Confidence Interval (95%):</strong><br />
              {match.red_fighter}: [{(prediction.red_confidence_interval[0] * 100).toFixed(1)}% - {(prediction.red_confidence_interval[1] * 100).toFixed(1)}%]<br />
              {match.blue_fighter}: [{(prediction.blue_confidence_interval[0] * 100).toFixed(1)}% - {(prediction.blue_confidence_interval[1] * 100).toFixed(1)}%]
            </div>
          </div>

          <div style={{ fontSize: "12px", color: "#999", marginBottom: "16px" }}>
            Predictions left: {prediction.predictions_left || "unlimited"}
          </div>

          <button
            onClick={onClose}
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "#2196F3",
              color: "white",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              fontWeight: "bold"
            }}
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: "rgba(0,0,0,0.7)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: "white",
        borderRadius: "12px",
        padding: "24px",
        maxWidth: "500px",
        width: "90%"
      }}>
        <h2 style={{ marginTop: 0 }}>Fighter Comparison</h2>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "24px" }}>
          <div style={{ padding: "12px", backgroundColor: "#F5F5F5", borderRadius: "8px" }}>
            <div style={{ fontWeight: "bold", marginBottom: "8px" }}>{match.red_fighter}</div>
            <div style={{ fontSize: "12px", color: "#666" }}>
              <div>Record: {match.red_stats.record}</div>
              <div>Age: {match.red_stats.age}</div>
              <div>Reach: {match.red_stats.reach}"</div>
              <div>KO Ratio: {(match.red_stats.KO_ratio * 100).toFixed(1)}%</div>
            </div>
          </div>

          <div style={{ padding: "12px", backgroundColor: "#F5F5F5", borderRadius: "8px" }}>
            <div style={{ fontWeight: "bold", marginBottom: "8px" }}>{match.blue_fighter}</div>
            <div style={{ fontSize: "12px", color: "#666" }}>
              <div>Record: {match.blue_stats.record}</div>
              <div>Age: {match.blue_stats.age}</div>
              <div>Reach: {match.blue_stats.reach}"</div>
              <div>KO Ratio: {(match.blue_stats.KO_ratio * 100).toFixed(1)}%</div>
            </div>
          </div>
        </div>

        <button
          onClick={handleGetPrediction}
          disabled={loading}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: loading ? "not-allowed" : "pointer",
            fontWeight: "bold",
            marginBottom: "8px"
          }}
        >
          {loading ? "Generating Prediction..." : "Generate Prediction"}
        </button>

        <button
          onClick={onClose}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#EEE",
            color: "#333",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer"
          }}
        >
          Cancel
        </button>

        {error && <div style={{ color: "red", marginTop: "12px", fontSize: "12px" }}>{error}</div>}
      </div>
    </div>
  );
}

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [showPredictionModal, setShowPredictionModal] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth");
      return;
    }

    // Fetch user stats and upcoming matches
    const fetchData = async () => {
      try {
        const [statsRes, matchesRes] = await Promise.all([
          fetch(`${API_URL}/user/stats`, {
            headers: { "Authorization": `Bearer ${token}` }
          }),
          fetch(`${API_URL}/matches/upcoming`)
        ]);

        if (!statsRes.ok) throw new Error("Failed to fetch user stats");
        if (!matchesRes.ok) throw new Error("Failed to fetch matches");

        const statsData = await statsRes.json();
        const matchesData = await matchesRes.json();

        setUser(statsData);
        setMatches(matchesData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/auth");
  };

  if (loading) {
    return <div style={{ padding: "20px", textAlign: "center" }}>Loading...</div>;
  }

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <h1 style={{ margin: 0 }}>🥊 UFC Predictor</h1>
        <div style={{ fontSize: "12px" }}>
          <div style={{ marginBottom: "4px" }}>Welcome, <strong>{user?.username}</strong></div>
          <button
            onClick={handleLogout}
            style={{
              padding: "4px 8px",
              backgroundColor: "#FF6B6B",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "12px"
            }}
          >
            Logout
          </button>
        </div>
      </div>

      <DisclaimerBanner />

      {user && <PredictionCounter free={user.free_predictions_left} isPremium={user.is_premium} />}

      {error && <div style={{ color: "red", marginBottom: "20px", padding: "12px", backgroundColor: "#FFEBEE", borderRadius: "8px" }}>{error}</div>}

      <h2>Upcoming Fights</h2>
      {matches.length === 0 ? (
        <div style={{ textAlign: "center", color: "#666", padding: "40px 20px" }}>
          No upcoming fights at the moment.
        </div>
      ) : (
        matches.map((match) => (
          <MatchCard
            key={match.id}
            match={match}
            onSelectMatch={(m) => {
              setSelectedMatch(m);
              setShowPredictionModal(true);
            }}
            isPremium={user?.is_premium}
            freePredictionsLeft={user?.free_predictions_left}
            user={user}
          />
        ))
      )}

      <div style={{ marginTop: "40px", textAlign: "center" }}>
        <Link href="/history"><a style={{ color: "#2196F3", textDecoration: "none", fontWeight: "bold" }}>View Prediction History →</a></Link>
      </div>

      {showPredictionModal && selectedMatch && (
        <PredictionModal
          match={selectedMatch}
          user={user}
          onClose={() => setShowPredictionModal(false)}
          onPredictDone={() => {
            // Refresh user stats to update predictions left
            const token = localStorage.getItem("token");
            fetch(`${API_URL}/user/stats`, {
              headers: { "Authorization": `Bearer ${token}` }
            })
              .then((res) => res.json())
              .then((data) => setUser(data));
          }}
        />
      )}
    </div>
  );
}


  const winStats = {
    red: data.filter(r => r.predicted_winner === "RedFighter").length,
    blue: data.filter(r => r.predicted_winner === "BlueFighter").length,
  };

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Prediction Probabilities</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 100 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} interval={0} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Red" fill="#FF6B6B" />
          <Bar dataKey="Blue" fill="#4ECDC4" />
        </BarChart>
      </ResponsiveContainer>
      
      <h3 style={{ marginTop: 30 }}>Predicted Winners Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie data={[{ name: "Red Wins", value: winStats.red }, { name: "Blue Wins", value: winStats.blue }]} cx="50%" cy="50%" label outerRadius={100}>
            <Cell fill="#FF6B6B" />
            <Cell fill="#4ECDC4" />
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function PredictionTable({ rows }) {
  if (!rows || rows.length === 0) return <div>No predictions yet.</div>;
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 20 }}>
      <thead>
        <tr style={{ backgroundColor: "#f0f0f0" }}>
          <th style={{ padding: 10, textAlign: "left", borderBottom: "2px solid #333" }}>Red Fighter</th>
          <th style={{ padding: 10, textAlign: "left", borderBottom: "2px solid #333" }}>Blue Fighter</th>
          <th style={{ padding: 10, textAlign: "left", borderBottom: "2px solid #333" }}>Prediction</th>
          <th style={{ padding: 10, textAlign: "left", borderBottom: "2px solid #333" }}>Red %</th>
          <th style={{ padding: 10, textAlign: "left", borderBottom: "2px solid #333" }}>Confidence</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => {
          const redProb = r.prob_RedFighter || 0;
          const blueProb = r.prob_BlueFighter || 0;
          const confidence = Math.max(redProb, blueProb);
          return (
            <tr key={i} style={{ borderTop: "1px solid #ddd" }}>
              <td style={{ padding: 10 }}>{r.red_fighter}</td>
              <td style={{ padding: 10 }}>{r.blue_fighter}</td>
              <td style={{ padding: 10, fontWeight: "bold" }}>{r.predicted_winner}</td>
              <td style={{ padding: 10 }}>{Math.round(redProb * 100)}%</td>
              <td style={{ padding: 10, color: confidence > 0.65 ? "green" : confidence > 0.55 ? "orange" : "red" }}>
                {Math.round(confidence * 100)}% {confidence > 0.65 ? "🟢 High" : confidence > 0.55 ? "🟡 Med" : "🔴 Low"}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default function Home() {
  const [result, setResult] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("auth_token") || "");

  const refresh = async () => {
    try {
      const res = await fetch("http://localhost:8000/results", {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) {
        const data = await res.json();
        setResult(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif", maxWidth: 1200, margin: "0 auto" }}>
      <h1>🥊 UFC Predictions</h1>
      {token && <p style={{ color: "green" }}>✅ Authenticated</p>}
      <UploadForm onDone={() => refresh()} />
      <button onClick={refresh} style={{ padding: "8px 16px", marginBottom: 10, cursor: "pointer" }}>
        📊 Refresh Results
      </button>
      {result && <ProbabilityChart data={result} />}
      {result && <PredictionTable rows={result} />}
    </div>
  );
}


import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function History(){
  const [rows, setRows] = useState([])
  const [token, setToken] = useState(localStorage.getItem("auth_token") || "")
  const [showChart, setShowChart] = useState(false)

  const load = async () => {
    if (!token) {
      window.location.href = "/auth"
      return
    }
    try {
      const res = await fetch('http://localhost:8000/results', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.ok) {
        setRows(await res.json())
      } else {
        window.location.href = "/auth"
      }
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(()=>{load()},[])

  const chartData = rows.map((r, i) => ({
    name: i,
    redProb: Math.round((r.prob_RedFighter || 0) * 100),
    ciLow: Math.round((r.ci_low_RedFighter || 0) * 100),
    ciHigh: Math.round((r.ci_high_RedFighter || 0) * 100),
  }))

  const accuracy = rows.filter(r => r.actual_winner && r.predicted_winner === r.actual_winner).length / Math.max(rows.length, 1)

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif', maxWidth: 1200, margin: '0 auto' }}>
      <h1>📊 Prediction History</h1>
      <p>Total: {rows.length} | Accuracy: {Math.round(accuracy * 100)}%</p>
      
      {rows.length > 0 && (
        <button onClick={() => setShowChart(!showChart)} style={{ padding: '8px 16px', marginBottom: 20, cursor: 'pointer' }}>
          {showChart ? 'Hide' : 'Show'} Confidence Chart
        </button>
      )}

      {showChart && rows.length > 0 && (
        <div style={{ marginBottom: 30 }}>
          <h3>Probability with 95% Confidence Intervals</h3>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend />
              <Line type="monotone" dataKey="redProb" stroke="#FF6B6B" name="Predicted %" />
              <Line type="monotone" dataKey="ciLow" stroke="#FF6B6B" strokeDasharray="5 5" name="95% CI Low" />
              <Line type="monotone" dataKey="ciHigh" stroke="#FF6B6B" strokeDasharray="5 5" name="95% CI High" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
        <thead><tr style={{backgroundColor: '#f0f0f0'}}><th style={{padding: 8, textAlign: 'left', borderBottom: '2px solid #333'}}>Date</th><th style={{padding: 8, textAlign: 'left', borderBottom: '2px solid #333'}}>Red</th><th style={{padding: 8, textAlign: 'left', borderBottom: '2px solid #333'}}>Blue</th><th style={{padding: 8, textAlign: 'center', borderBottom: '2px solid #333'}}>Pred</th><th style={{padding: 8, textAlign: 'center', borderBottom: '2px solid #333'}}>Red %</th><th style={{padding: 8, textAlign: 'center', borderBottom: '2px solid #333'}}>95% CI</th><th style={{padding: 8, textAlign: 'center', borderBottom: '2px solid #333'}}>Actual</th><th style={{padding: 8, textAlign: 'center', borderBottom: '2px solid #333'}}>Result</th></tr></thead>
        <tbody>
          {rows.map(r => {
            const correct = r.actual_winner && r.predicted_winner === r.actual_winner
            const ciLow = Math.round((r.ci_low_RedFighter || 0) * 100)
            const ciHigh = Math.round((r.ci_high_RedFighter || 0) * 100)
            return (
              <tr key={r.id} style={{ borderTop: '1px solid #ddd', backgroundColor: correct ? '#e8f5e9' : r.actual_winner ? '#ffebee' : 'white' }}>
                <td style={{padding: 8}}>{r.date}</td>
                <td style={{padding: 8}}>{r.red_fighter?.substring(0, 15)}</td>
                <td style={{padding: 8}}>{r.blue_fighter?.substring(0, 15)}</td>
                <td style={{padding: 8, textAlign: 'center', fontWeight: 'bold'}}>{r.predicted_winner?.split('Fighter')[0]}</td>
                <td style={{padding: 8, textAlign: 'center'}}>{Math.round((r.prob_RedFighter||0)*100)}%</td>
                <td style={{padding: 8, textAlign: 'center', fontSize: 11}}>[{ciLow}% - {ciHigh}%]</td>
                <td style={{padding: 8, textAlign: 'center'}}>{r.actual_winner || '-'}</td>
                <td style={{padding: 8, textAlign: 'center'}}>{correct ? '✅' : r.actual_winner ? '❌' : '⏳'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

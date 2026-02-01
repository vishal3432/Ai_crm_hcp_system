import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, Activity, Search, Trash2, Download, Lock } from 'lucide-react';

// --- 1. LOGIN COMPONENT (Sirf ek baar) ---
function Login({ onLogin }) {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (user === 'admin' && pass === 'admin123') {
      onLogin(true);
    } else {
      alert("Invalid Credentials!");
    }
  };

  return (
    <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f3f4f6' }}>
      <form onSubmit={handleSubmit} style={{ background: 'white', padding: '40px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', width: '320px' }}>
        <h2 style={{ textAlign: 'center', color: '#2563eb', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
          <Lock /> CRM Login
        </h2>
        <input style={{ width: '100%', padding: '10px', margin: '10px 0', boxSizing: 'border-box', borderRadius: '6px', border: '1px solid #ddd' }} placeholder="Username" onChange={e => setUser(e.target.value)} />
        <input type="password" style={{ width: '100%', padding: '10px', margin: '10px 0', boxSizing: 'border-box', borderRadius: '6px', border: '1px solid #ddd' }} placeholder="Password" onChange={e => setPass(e.target.value)} />
        <button type="submit" style={{ width: '100%', padding: '12px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>Enter Dashboard</button>
      </form>
    </div>
  );
}

// --- 2. MAIN APP COMPONENT (Sirf ek baar) ---
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [msg, setMsg] = useState('');
  const [chat, setChat] = useState([]);
  const [logs, setLogs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  // Backend URL - Replace this with your Render URL when going live
  const API_BASE_URL = "https://ai-crm-hcp-system.onrender.com"; 

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/interactions`);
      setLogs(res.data);
    } catch (e) { console.error("DB Error"); }
  };

  useEffect(() => {
    if (isAuthenticated) fetchLogs();
  }, [isAuthenticated]);

  const sendMessage = async () => {
    if (!msg.trim()) return;
    const userMessage = { text: msg, role: 'user' };
    setChat([...chat, userMessage]);
    setMsg('');

    try {
      const res = await axios.post(`${API_BASE_URL}/chat`, { message: msg });
      setChat(prev => [...prev, { text: res.data.response, role: 'ai' }]);
      fetchLogs(); 
    } catch (e) {
      setChat(prev => [...prev, { text: "AI Error: Check Rate Limit or Backend Status!", role: 'ai' }]);
    }
  };

  const exportToCSV = () => {
    const headers = "ID, HCP Name, Product, Summary, Date\n";
    const rows = logs.map(l => `${l.id}, "${l.hcp_name}", "${l.product}", "${l.summary}", ${l.created_at}`).join("\n");
    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "CRM_Report.csv";
    a.click();
  };

  if (!isAuthenticated) {
    return <Login onLogin={setIsAuthenticated} />;
  }

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#f3f4f6', fontFamily: 'Inter, sans-serif' }}>
      <aside style={{ width: '300px', backgroundColor: 'white', borderRight: '1px solid #e5e7eb', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '20px', borderBottom: '1px solid #f3f4f6' }}>
          <h2 style={{ color: '#2563eb', fontSize: '1.2rem', fontWeight: 'bold' }}>HCP CRM</h2>
          <input 
            placeholder="Search Doctors..." 
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ width: '100%', padding: '8px', marginTop: '10px', borderRadius: '6px', border: '1px solid #ddd' }}
          />
          <button onClick={exportToCSV} style={{ width: '100%', marginTop: '10px', padding: '8px', background: '#10b981', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
             Download Report
          </button>
        </div>
        <div style={{ flex: 1, overflowY: 'auto', padding: '15px' }}>
          {logs.filter(l => l.hcp_name.toLowerCase().includes(searchTerm.toLowerCase())).map(log => (
            <div key={log.id} style={{ padding: '10px', background: '#f8fafc', borderRadius: '8px', marginBottom: '8px', border: '1px solid #e2e8f0' }}>
              <strong>{log.hcp_name}</strong>
              <div style={{ fontSize: '0.7rem', color: '#2563eb' }}>{log.product}</div>
            </div>
          ))}
        </div>
        <button onClick={() => setIsAuthenticated(false)} style={{ padding: '15px', background: '#fef2f2', color: '#ef4444', border: 'none', cursor: 'pointer' }}>Logout</button>
      </aside>

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
          {chat.map((c, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: c.role === 'user' ? 'flex-end' : 'flex-start', marginBottom: '15px' }}>
              <div style={{ padding: '12px', borderRadius: '12px', maxWidth: '60%', backgroundColor: c.role === 'user' ? '#2563eb' : 'white', color: c.role === 'user' ? 'white' : 'black', boxShadow: '0 1px 2px rgba(0,0,0,0.1)' }}>
                {c.text}
              </div>
            </div>
          ))}
        </div>
        <div style={{ padding: '20px', background: 'white', display: 'flex', gap: '10px' }}>
          <input 
            style={{ flex: 1, padding: '12px', borderRadius: '8px', border: '1px solid #ddd' }}
            value={msg}
            onChange={(e) => setMsg(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your interaction..."
          />
          <button onClick={sendMessage} style={{ padding: '10px 20px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}>Send</button>
        </div>
      </main>
    </div>
  );
}

export default App;
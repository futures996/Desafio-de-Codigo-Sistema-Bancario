import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard({ token }) {
  const [contas, setContas] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/contas", {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setContas(res.data));
  }, [token]);

  return (
    <div>
      <h2>Minhas Contas</h2>
      <ul>
        {contas.map(c => (
          <li key={c.numero}>{c.tipo} - R${c.saldo}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;

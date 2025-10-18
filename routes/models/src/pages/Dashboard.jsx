import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [clientes, setClientes] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/clientes")
      .then(res => setClientes(res.data));
  }, []);

  return (
    <div>
      <h1>Dashboard Bancário</h1>
      <ul>
        {clientes.map(c => (
          <li key={c.cpf}>{c.nome} - {c.cpf}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;

import React, { useState } from 'react';
import axios from 'axios';

function Transacao({ token }) {
  const [conta, setConta] = useState("");
  const [valor, setValor] = useState("");

  const enviarDeposito = async () => {
    await axios.post("http://localhost:8000/transacoes/deposito", {
      conta_numero: conta,
      valor: parseFloat(valor)
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert("Depósito realizado!");
  };

  return (
    <div>
      <h2>Depósito</h2>
      <input placeholder="Conta" value={conta} onChange={e => setConta(e.target.value)} />
      <input placeholder="Valor" value={valor} onChange={e => setValor(e.target.value)} />
      <button onClick={enviarDeposito}>Depositar</button>
    </div>
  );
}

export default Transacao;

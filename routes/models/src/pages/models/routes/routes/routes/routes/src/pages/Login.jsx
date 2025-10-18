import React, { useState } from 'react';
import axios from 'axios';

function Login({ setToken }) {
  const [cpf, setCpf] = useState("");
  const [senha, setSenha] = useState("");

  const handleLogin = async () => {
    const res = await axios.post("http://localhost:8000/login", { cpf, senha });
    setToken(res.data.access_token);
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="CPF" value={cpf} onChange={e => setCpf(e.target.value)} />
      <input placeholder="Senha" type="password" value={senha} onChange={e => setSenha(e.target.value)} />
      <button onClick={handleLogin}>Entrar</button>
    </div>
  );
}

export default Login;

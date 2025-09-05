import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/auth";
import "../styles/home.css";

export default function Login() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const nav = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    setErr(""); setLoading(true);
    try {
      await login(identifier.trim(), password);
      nav("/panel", { replace: true });
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="site-container auth-page">
      <div className="auth-card">
        <h2>Iniciar sesión</h2>
        <form onSubmit={onSubmit}>
          <div className="form-grid">
            <input
              className="input"
              type="text"
              placeholder="Usuario o correo"
              value={identifier}
              onChange={(e)=>setIdentifier(e.target.value)}
              required
            />
            <input
              className="input"
              type="password"
              placeholder="Contraseña"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              required
            />
            {err && <div className="alert">{err}</div>}
            <div className="actions">
              <button className="btn">{loading ? "Ingresando..." : "Entrar"}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

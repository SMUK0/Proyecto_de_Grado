import { useEffect, useState } from "react";
import { apiFetch, logout } from "../services/auth";

export default function Panel() {
  const [me, setMe] = useState(null);

  useEffect(() => {
    (async () => {
      const res = await apiFetch("/auth/me/");
      if (res.ok) setMe(await res.json());
    })();
  }, []);

  return (
    <div className="container" style={{marginTop: 30}}>
      <div className="card card--glass" style={{padding: 18}}>
        <h2 style={{marginTop:0}}>Panel</h2>
        {me ? (
          <p>Hola <b>{me.username}</b> ({me.email || "sin email"})</p>
        ) : (
          <p>Cargando…</p>
        )}
        <button className="btn btn--ghost" onClick={logout}>Cerrar sesión</button>
      </div>
    </div>
  );
}

// src/pages/Home.jsx
import { useEffect, useState } from "react";
import "../styles/home.css";

const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api";

export default function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API}/home/`);
        if (!res.ok) throw new Error("No se pudo cargar el home");
        const json = await res.json();
        setData(json);
      } catch {
        setData({
          brand: "Resoluciones Integrales",
          tagline:
            "Servicios de intervención terapéutica integral multidisciplinaria y personalizada.",
          about:
            "Somos un consultorio que brinda intervención terapéutica integral y personalizada. Contáctanos para recibir apoyo profesional.",
          services: [
            {
              name: "Apoyo terapéutico por adicciones",
              description:
                "Acompañamiento clínico y psicoeducativo orientado a la recuperación.",
              slug: "adicciones",
            },
            {
              name: "Intervención terapéutica integral",
              description: "Atención multidisciplinaria centrada en la persona.",
              slug: "intervencion-integral",
            },
          ],
          contact: { whatsapp: "https://walink.co/e3e2a6" },
        });
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const year = new Date().getFullYear();

  return (
    <div className="site-wrapper">
      {/* HEADER */}
      <div className="site-container header-bar">
        <div className="nav">
          <div className="nav__brand">
            <img className="nav__logo" src="/logo-ri.png" alt="Logo" />
            <span>Resoluciones Integrales</span>
          </div>
          <nav>
            <a className="btn btn--ghost" href="/login">Login</a>
          </nav>
        </div>
      </div>

      {/* CONTENIDO CENTRADO */}
      <main className="page">
        <div className="inner">
          {loading ? (
            <p className="loading">Cargando…</p>
          ) : (
            <>
              {/* HERO */}
              <section className="hero">
                <span className="chip">✨ Consultorio psicológico</span>
                <h1>{data?.brand ?? "Resoluciones Integrales"}</h1>
                <p className="lead">
                  {data?.tagline ??
                    "Servicios de intervención terapéutica integral multidisciplinaria y personalizada."}
                </p>

                <div className="center-row">
                  <a
                    className="btn"
                    href={data?.contact?.whatsapp ?? "https://walink.co/e3e2a6"}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Agendar por WhatsApp
                  </a>
                  <a className="btn btn--ghost" href="#servicios">
                    Conocer servicios
                  </a>
                </div>

                <div className="center-row gap-top">
                  <span className="chip">🔒 Confidencialidad</span>
                  <span className="chip">💙 Trato empático</span>
                  <span className="chip">🧭 Enfoque integral</span>
                </div>
              </section>

              {/* SOBRE NOSOTROS */}
              <h3 className="section-title">Sobre nosotros</h3>
              <div className="about">
                {data?.about ??
                  "Somos un consultorio que brinda intervención terapéutica integral y personalizada. Contáctanos para recibir apoyo profesional."}
              </div>

              {/* ÁREAS */}
              <h3 className="section-title">Áreas de atención</h3>
              <div className="center-row wrap">
                {[
                  "Intervención terapéutica integral",
                  "Enfoque multidisciplinario",
                  "Atención personalizada",
                  "Apoyo terapéutico por adicciones",
                ].map((t) => (
                  <span key={t} className="chip">{t}</span>
                ))}
              </div>

              {/* SERVICIOS */}
              <h3 id="servicios" className="section-title">Servicios</h3>
              <div className="services">
                {(data?.services ?? []).map((s) => (
                  <article className="card" key={s.slug}>
                    <h3>{s.name}</h3>
                    <p>{s.description}</p>
                    <a
                      className="btn btn--ghost"
                      href={data?.contact?.whatsapp ?? "https://walink.co/e3e2a6"}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Agendar ahora →
                    </a>
                  </article>
                ))}
              </div>

              {/* CTA FINAL */}
              <section className="cta">
                <h3>¿Necesitas apoyo profesional?</h3>
                <p>Escríbenos y coordinamos tu primera consulta.</p>
                <a
                  className="btn"
                  href={data?.contact?.whatsapp ?? "https://walink.co/e3e2a6"}
                  target="_blank"
                  rel="noreferrer"
                >
                  Hablar por WhatsApp
                </a>
              </section>

              {/* FOOTER */}
              <footer className="footer">© {year} Resoluciones Integrales</footer>
            </>
          )}
        </div>
      </main>
    </div>
  );
}

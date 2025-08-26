import { useEffect, useState } from "react";
import { fetchHomeInfo } from "../services/api.js";
import "../styles/home.css";

/* Iconos inline (sin librerías) */
const Sparkle = (props) => (
  <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
    <path d="M12 2l1.8 4.4L18 8.2l-4.2 1.8L12 14l-1.8-4-4.2-1.8 4.2-1.8L12 2zM5 14l1 2.4L8.5 18l-2.5 1.1L5 21.5l-1-2.4L1.5 18 4 16.4 5 14zm14 0l1 2.4L22.5 18 20 19.1l-1 2.4-1-2.4L15.5 18 18 16.4l1-2.4z" />
  </svg>
);
const Shield = (props) => (
  <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
    <path d="M12 2l8 4v6c0 5.25-3.5 9.92-8 11-4.5-1.08-8-5.75-8-11V6l8-4zm0 2.2L6 6.4v5.5c0 4.24 2.84 8.07 6 9.06 3.16-.99 6-4.82 6-9.06V6.4l-6-2.2z" />
    <path d="M10.2 12.6l-1.4-1.4L7.4 12.6l2.8 2.8 6-6-1.4-1.4-4.6 4.6z" />
  </svg>
);
const Heart = (props) => (
  <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
    <path d="M12 21s-6.7-4.2-9.3-7.3C.5 11.2 1 7.7 3.7 6.1 6.2 4.7 8.8 5.9 10 7.2c1.2-1.3 3.8-2.5 6.3-1.1 2.7 1.6 3.2 5.1.9 7.6C18.7 16.8 12 21 12 21z" />
  </svg>
);

export default function Home() {
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");

  const logoUrl =
    "https://scontent.flpb3-1.fna.fbcdn.net/v/t39.30808-6/312812677_551248810339846_7588325461411501304_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=uf6ocv1OhT8Q7kNvwEWsHY-&_nc_oc=AdnzcHLyUyxe6V7IA-yPxHVYJwaaDQm1CtJf8EB1BiTS-SiUmksozXzEP_nKTFe2ooo&_nc_zt=23&_nc_ht=scontent.flpb3-1.fna&_nc_gid=yl3jc3jmxajyBDEWcnfr_g&oh=00_AfVO7IymOKocItzo02ugtGSKfSZfexd1jFeybEs4E251HQ&oe=68B3381E";

  useEffect(() => {
    fetchHomeInfo().then(setData).catch((e) => setErr(e.message));
  }, []);

  const whatsapp = data?.contact?.whatsapp || "#";

  return (
    <main className="page">
      {/* NAV — logo + botón Login a la derecha */}
      <nav className="nav container" role="navigation" aria-label="principal">
        <a className="brand" href="#">
          <img className="brand-logo" src={logoUrl} alt="Logo Resoluciones Integrales" />
          <span className="brand-text">{data?.brand || "Resoluciones Integrales"}</span>
        </a>

        <div className="nav-actions">
          <a className="btn btn--login" href="/login">Login</a>
        </div>
      </nav>

      {/* HERO */}
      <header className="hero container">
        <div className="hero-badge">
          <Sparkle className="icon" />
          Consultorio psicológico
        </div>
        <h1 className="hero-title">{data?.brand || "Resoluciones Integrales"}</h1>
        <p className="hero-sub">
          {data?.tagline ||
            "Servicios de intervención terapéutica integral, multidisciplinaria y personalizada."}
        </p>
        <div className="cta-row">
          <a className="btn btn--primary" href={whatsapp} target="_blank" rel="noreferrer">
            Agendar por WhatsApp
          </a>
          <a className="btn btn--ghost" href="#servicios">Conocer servicios</a>
        </div>

        <div className="hero-stats">
          <div className="stat"><Shield className="icon" /> Confidencialidad</div>
          <div className="stat"><Heart className="icon" /> Trato empático</div>
          <div className="stat"><Sparkle className="icon" /> Enfoque integral</div>
        </div>
      </header>

      {/* SOBRE NOSOTROS */}
      <section className="section container">
        <h2 className="section-title">Sobre nosotros</h2>
        <div className="card card--glass">
          {err ? (
            <p><strong>Error:</strong> {err}</p>
          ) : data ? (
            <p>
              {data.about ??
                "Somos un consultorio que brinda intervención terapéutica integral y personalizada. Nuestro enfoque es multidisciplinario con atención centrada en la persona."}
            </p>
          ) : (
            <div className="skeleton">
              <div className="skel skel-title"></div>
              <div className="skel skel-line"></div>
              <div className="skel skel-line"></div>
              <div className="skel skel-line w-70"></div>
            </div>
          )}
        </div>
      </section>

      {/* ÁREAS DE ATENCIÓN (extraído de su comunicación en redes) */}
      <section className="section container">
        <h2 className="section-title">Áreas de atención</h2>
        <div className="chip-row">
          <span className="chip">Intervención terapéutica integral</span>
          <span className="chip">Enfoque multidisciplinario</span>
          <span className="chip">Atención personalizada</span>
          <span className="chip chip--accent">Apoyo terapéutico por adicciones</span>
        </div>
      </section>

      {/* SERVICIOS */}
      <section id="servicios" className="section container">
        <h2 className="section-title">Servicios</h2>
        <div className="grid">
          {(data?.services || [
            { name: "Apoyo terapéutico por adicciones", slug: "adicciones",
              description: "Acompañamiento clínico con enfoque integral." },
            { name: "Intervención terapéutica integral", slug: "intervencion-integral",
              description: "Atención multidisciplinaria centrada en la persona." },
          ]).map((s, i) => (
            <article className="card card--elev" key={s?.slug ?? i}>
              <div className="card-icon-wrap">
                {s?.slug?.includes("adiccion") ? (
                  <Shield className="icon-xl" />
                ) : i % 2 === 0 ? (
                  <Heart className="icon-xl" />
                ) : (
                  <Sparkle className="icon-xl" />
                )}
              </div>
              <div className="card-body">
                <h3 className="card-title">{s?.name || "Servicio"}</h3>
                <p className="card-text">
                  {s?.description || "Atención centrada en la persona y su contexto."}
                </p>
                <a className="card-cta" href={whatsapp} target="_blank" rel="noreferrer">
                  Agendar ahora →
                </a>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* CÓMO TRABAJAMOS (metodología simple) */}
      <section className="section container">
        <h2 className="section-title">¿Cómo trabajamos?</h2>
        <div className="steps">
          <div className="step"><span className="step-num">1</span> Evaluación inicial y objetivos.</div>
          <div className="step"><span className="step-num">2</span> Plan de intervención personalizado.</div>
          <div className="step"><span className="step-num">3</span> Acompañamiento y seguimiento continuo.</div>
        </div>
      </section>

      {/* CTA compacta */}
      <section className="cta-band">
        <div className="container cta-band-inner">
          <h3>¿Necesitas apoyo profesional?</h3>
          <a className="btn btn--light" href={whatsapp} target="_blank" rel="noreferrer">
            Hablar por WhatsApp
          </a>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer container">
        <span>© {new Date().getFullYear()} {data?.brand || "Resoluciones Integrales"}</span>
      </footer>
    </main>
  );
}

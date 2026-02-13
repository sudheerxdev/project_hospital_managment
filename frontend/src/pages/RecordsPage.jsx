import React, { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function RecordsPage() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    apiRequest("/services/").then((data) => setServices(data.results || []));
  }, []);

  return (
    <section className="page-stack">
      <section className="panel">
        <div className="panel-head">
          <h2>Service Requests</h2>
        </div>
        <ul className="list">
          {services.map((s) => (
            <li key={s.id} className="list-item">
              <div>
                <strong>{s.title || `Request #${s.id}`}</strong>
                <p className="meta">Guest {s.guest} | {s.record_type}</p>
              </div>
              <div className="item-right">
                <span className="badge subtle">v{s.current_version}</span>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

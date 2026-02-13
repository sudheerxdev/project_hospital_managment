import React, { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function NotificationsPage() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    apiRequest("/notifications/").then((data) => setLogs(data.results || []));
  }, []);

  return (
    <section className="page-stack">
      <section className="panel">
        <div className="panel-head">
          <h2>Guest Notification Activity</h2>
        </div>
        <ul className="list">
          {logs.map((n) => (
            <li key={n.id} className="list-item">
              <div>
                <strong>{n.recipient}</strong>
                <p className="meta">{n.message}</p>
              </div>
              <div className="item-right">
                <span className="badge subtle">{n.channel.toUpperCase()}</span>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

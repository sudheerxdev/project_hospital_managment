import React, { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function AppointmentsPage() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    apiRequest("/bookings/?upcoming=true").then((data) => setBookings(data.results || []));
  }, []);

  return (
    <section className="page-stack">
      <section className="panel">
        <div className="panel-head">
          <h2>Upcoming Bookings</h2>
        </div>
        <ul className="list">
          {bookings.map((b) => (
            <li key={b.id} className="list-item">
              <div>
                <strong>Booking #{b.id}</strong>
                <p className="meta">Guest {b.guest} | Room {b.room}</p>
              </div>
              <div className="item-right">
                <span className="badge">{b.status}</span>
                <p className="meta">{new Date(b.check_in).toLocaleString()} - {new Date(b.check_out).toLocaleString()}</p>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

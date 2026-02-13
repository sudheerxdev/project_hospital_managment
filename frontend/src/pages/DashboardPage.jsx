import React, { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function DashboardPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    apiRequest("/dashboard/").then(setData).catch(() => setData(null));
  }, []);

  if (!data) return <p className="muted">Loading dashboard...</p>;

  return (
    <section className="page-stack">
      <div className="stat-grid">
        <article className="stat-card"><h3>Guests</h3><p>{data.total_guests}</p></article>
        <article className="stat-card"><h3>Rooms</h3><p>{data.total_rooms}</p></article>
        <article className="stat-card"><h3>Occupied Rooms</h3><p>{data.occupied_rooms}</p></article>
        <article className="stat-card"><h3>Pending Invoices</h3><p>{data.pending_invoices}</p></article>
      </div>

      <section className="panel">
        <div className="panel-head">
          <h2>Upcoming Bookings</h2>
        </div>
        <ul className="list">
          {(data.upcoming_bookings || []).map((booking) => (
            <li key={booking.id} className="list-item">
              <div>
                <strong>Booking #{booking.id}</strong>
                <p className="meta">Guest {booking.guest_id} | Room {booking.room_id}</p>
              </div>
              <div className="item-right">
                <span className="badge">{booking.status}</span>
                <p className="meta">{new Date(booking.check_in).toLocaleString()}</p>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

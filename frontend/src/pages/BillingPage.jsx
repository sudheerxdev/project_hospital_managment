import React, { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function BillingPage() {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    apiRequest("/invoices/").then((data) => setInvoices(data.results || []));
  }, []);

  return (
    <section className="page-stack">
      <section className="panel">
        <div className="panel-head">
          <h2>Invoices and Payments</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Booking</th>
                <th>Total</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((i) => (
                <tr key={i.id}>
                  <td>{i.id}</td>
                  <td>{i.booking}</td>
                  <td>${i.total}</td>
                  <td><span className="badge">{i.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

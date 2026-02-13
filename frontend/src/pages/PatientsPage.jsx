import React, { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function PatientsPage() {
  const [guests, setGuests] = useState([]);
  const [search, setSearch] = useState("");

  const loadGuests = async (term = "") => {
    const result = await apiRequest(`/guests/?search=${encodeURIComponent(term)}`);
    setGuests(result.results || []);
  };

  useEffect(() => {
    loadGuests();
  }, []);

  return (
    <section className="page-stack">
      <section className="panel">
        <div className="toolbar">
          <input
            placeholder="Search by name, email, or phone"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button onClick={() => loadGuests(search)}>Search</button>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Date of Birth</th>
                <th>Phone</th>
              </tr>
            </thead>
            <tbody>
              {guests.map((g) => (
                <tr key={g.id}>
                  <td>{g.id}</td>
                  <td>{g.first_name} {g.last_name}</td>
                  <td>{g.date_of_birth}</td>
                  <td>{g.phone || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

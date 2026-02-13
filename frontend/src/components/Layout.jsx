import React from "react";
import { Link, useLocation } from "react-router-dom";
import { canAccess, normalizeRole } from "../auth/rbac";

const links = [
  { path: "/dashboard", label: "Dashboard" },
  { path: "/guests", label: "Guests" },
  { path: "/bookings", label: "Bookings" },
  { path: "/services", label: "Services" },
  { path: "/invoices", label: "Invoices" },
  { path: "/notifications", label: "Notifications" },
];

function titleFromPath(pathname) {
  const found = links.find((item) => item.path === pathname);
  return found ? found.label : "Hotel Management";
}

export default function Layout({ children, onLogout, user }) {
  const location = useLocation();
  const role = normalizeRole(user?.role || "");
  const visibleLinks = links.filter((link) => canAccess(role, link.path));

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-wrap">
          <p className="eyebrow">Hotel Management</p>
          <h2>StayFlow PMS</h2>
          <p className="role-pill">{role || "Unknown role"}</p>
        </div>

        <nav>
          {visibleLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={location.pathname === link.path ? "active" : ""}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <button className="logout" onClick={onLogout}>Sign out</button>
      </aside>

      <main className="content">
        <header className="page-header">
          <div>
            <p className="eyebrow">Front Office Console</p>
            <h1>{titleFromPath(location.pathname)}</h1>
          </div>
          <div className="profile-chip">
            <strong>{user?.first_name || user?.username || "User"}</strong>
            <span>{user?.email || ""}</span>
          </div>
        </header>
        {children}
      </main>
    </div>
  );
}

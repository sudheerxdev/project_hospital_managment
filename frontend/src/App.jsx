import React, { useMemo, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { login, signup } from "./api/client";

import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import PatientsPage from "./pages/PatientsPage";
import AppointmentsPage from "./pages/AppointmentsPage";
import RecordsPage from "./pages/RecordsPage";
import BillingPage from "./pages/BillingPage";
import NotificationsPage from "./pages/NotificationsPage";
import { canAccess, firstAllowedRoute, normalizeRole } from "./auth/rbac";

function ProtectedRoute({ user, path, element }) {
  const role = normalizeRole(user?.role || "");
  if (!canAccess(role, path)) {
    return <Navigate to={firstAllowedRoute(role)} replace />;
  }
  return element;
}

export default function App() {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("current_user");
    return raw ? JSON.parse(raw) : null;
  });

  const isAuthenticated = useMemo(() => Boolean(localStorage.getItem("access_token") && user), [user]);

  const onLogin = async (username, password) => {
    const result = await login(username, password);
    localStorage.setItem("access_token", result.access);
    localStorage.setItem("refresh_token", result.refresh);
    localStorage.setItem("current_user", JSON.stringify(result.user));
    setUser(result.user);
  };

  const onSignup = async (payload) => signup(payload);

  const onLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("current_user");
    setUser(null);
  };

  if (!isAuthenticated) {
    return <LoginPage onLogin={onLogin} onSignup={onSignup} />;
  }

  const defaultRoute = firstAllowedRoute(normalizeRole(user?.role || ""));

  return (
    <Layout onLogout={onLogout} user={user}>
      <Routes>
        <Route path="/" element={<Navigate to={defaultRoute} replace />} />
        <Route path="/dashboard" element={<ProtectedRoute user={user} path="/dashboard" element={<DashboardPage />} />} />
        <Route path="/guests" element={<ProtectedRoute user={user} path="/guests" element={<PatientsPage />} />} />
        <Route path="/bookings" element={<ProtectedRoute user={user} path="/bookings" element={<AppointmentsPage />} />} />
        <Route path="/services" element={<ProtectedRoute user={user} path="/services" element={<RecordsPage />} />} />
        <Route path="/invoices" element={<ProtectedRoute user={user} path="/invoices" element={<BillingPage />} />} />
        <Route path="/notifications" element={<ProtectedRoute user={user} path="/notifications" element={<NotificationsPage />} />} />
        <Route path="*" element={<Navigate to={defaultRoute} replace />} />
      </Routes>
    </Layout>
  );
}

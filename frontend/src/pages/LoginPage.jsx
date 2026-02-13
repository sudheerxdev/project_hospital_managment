import React, { useState } from "react";
import heroImage from "../assets/images/hotel-hero.svg";
import logoImage from "../assets/images/stayflow-logo.svg";

const initialSignupState = {
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  phone: "",
  password: "",
};

export default function LoginPage({ onLogin, onSignup }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [signupData, setSignupData] = useState(initialSignupState);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  const submitLogin = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await onLogin(username, password);
      setError("");
      setNotice("");
    } catch (err) {
      setError(err.message || "Login failed. Check your credentials.");
      setNotice("");
    } finally {
      setBusy(false);
    }
  };

  const submitSignup = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      const result = await onSignup({ ...signupData });
      setError("");
      setNotice(result.warning || "Account created. Please login with your new credentials.");
      setMode("login");
      setPassword("");
      setSignupData(initialSignupState);
    } catch (err) {
      setError(err.message || "Signup failed. Try a different username or email.");
      setNotice("");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="login-shell">
      <section className="auth-hero">
        <img src={logoImage} alt="StayFlow logo" className="auth-logo" />
        <h1>StayFlow Hotel Suite</h1>
        <p>
          Complete hotel operations for reservations, check-in/out, service requests, and invoicing.
        </p>
        <img src={heroImage} alt="Hotel dashboard illustration" className="auth-illustration" />
      </section>

      <section className="centered-card">
        <div className="auth-tabs">
          <button
            type="button"
            className={mode === "login" ? "tab active" : "tab"}
            onClick={() => {
              setMode("login");
              setError("");
              setNotice("");
            }}
          >
            Login
          </button>
          <button
            type="button"
            className={mode === "signup" ? "tab active" : "tab"}
            onClick={() => {
              setMode("signup");
              setError("");
              setNotice("");
            }}
          >
            Sign up
          </button>
        </div>

        {mode === "login" ? (
          <form onSubmit={submitLogin} className="form-grid">
            <p className="eyebrow">Secure Access</p>
            <h2>Welcome back</h2>
            <label htmlFor="username">Username</label>
            <input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {notice && <p className="success">{notice}</p>}
            {error && <p className="error">{error}</p>}
            <button type="submit" disabled={busy}>{busy ? "Please wait..." : "Login"}</button>
          </form>
        ) : (
          <form onSubmit={submitSignup} className="form-grid">
            <p className="eyebrow">Guest Registration</p>
            <h2>Create account</h2>

            <label htmlFor="first_name">First name</label>
            <input
              id="first_name"
              value={signupData.first_name}
              onChange={(e) => setSignupData({ ...signupData, first_name: e.target.value })}
              required
            />

            <label htmlFor="last_name">Last name</label>
            <input
              id="last_name"
              value={signupData.last_name}
              onChange={(e) => setSignupData({ ...signupData, last_name: e.target.value })}
              required
            />

            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={signupData.email}
              onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
              required
            />

            <label htmlFor="signup_username">Username</label>
            <input
              id="signup_username"
              value={signupData.username}
              onChange={(e) => setSignupData({ ...signupData, username: e.target.value })}
              required
            />

            <label htmlFor="phone">Phone</label>
            <input
              id="phone"
              value={signupData.phone}
              onChange={(e) => setSignupData({ ...signupData, phone: e.target.value })}
            />

            <label htmlFor="signup_password">Password</label>
            <input
              id="signup_password"
              type="password"
              value={signupData.password}
              onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
              required
            />

            {notice && <p className="success">{notice}</p>}
            {error && <p className="error">{error}</p>}
            <button type="submit" disabled={busy}>{busy ? "Please wait..." : "Create account"}</button>
          </form>
        )}
      </section>
    </div>
  );
}

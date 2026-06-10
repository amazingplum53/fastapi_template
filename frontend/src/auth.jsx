// frontend/src/components/AuthForm.jsx
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function AuthForm({ mode, endpoint }) {
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    const form = event.currentTarget;
    const data = Object.fromEntries(new FormData(form));

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      navigate("/auth/success");
      return;
    }

    const result = await response.json();
    setError(result.detail ?? `${mode} failed`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>{mode}</h1>

      <input name="email" type="email" placeholder="Email" required />
      <input name="password" type="password" placeholder="Password" required />

      {error && <p>{error}</p>}

      <button type="submit">{mode}</button>

      {mode === "Login" ? (
        <p>
          No account? <Link to="/auth/signup">Sign up</Link>
        </p>
      ) : (
        <p>
          Already have an account? <Link to="/auth/login">Log in</Link>
        </p>
      )}
    </form>
  );
}
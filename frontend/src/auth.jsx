import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function AuthForm({ mode, endpoint }) {
  const [error, setError] = useState("");

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
      window.location.href = "/auth/success";
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
          No account? <a href="/signup">Sign up</a>
        </p>
      ) : (
        <p>
          Already have an account? <a href="/login">Log in</a>
        </p>
      )}
    </form>
  );
}

const rootElement = document.getElementById("auth-form");

if (rootElement) {
  createRoot(rootElement).render(
    <AuthForm
      mode={rootElement.dataset.mode}
      endpoint={rootElement.dataset.endpoint}
    />
  );
}
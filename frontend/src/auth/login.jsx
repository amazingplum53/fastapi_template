import React from "react";
import { createRoot } from "react-dom/client";

function LoginForm() {
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const form = event.currentTarget;
    const data = Object.fromEntries(new FormData(form));

    const response = await fetch("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      window.location.href = "/";
      return;
    }

    const error = await response.json();
    setError(error.detail ?? "Login failed");
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" placeholder="Email" required />
      <input name="password" type="password" placeholder="Password" required />

      {error && <p>{error}</p>}

      <button type="submit">Login</button>
    </form>
  );
}

createRoot(document.getElementById("login-form")).render(<LoginForm />);
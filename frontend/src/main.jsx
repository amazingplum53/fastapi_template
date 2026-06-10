// frontend/src/main.jsx
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import AuthForm from "./auth.jsx";

function SuccessPage() {
  return <h1>Success</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/auth/login"
          element={<AuthForm mode="Login" endpoint="/auth/login" />}
        />
        <Route
          path="/auth/signup"
          element={<AuthForm mode="Sign up" endpoint="/auth/signup" />}
        />
        <Route path="/auth/success" element={<SuccessPage />} />
      </Routes>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")).render(<App />);
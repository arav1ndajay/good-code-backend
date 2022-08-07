// @ts-nocheck

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { ThemeProvider } from "@primer/react";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider colorMode="auto">
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

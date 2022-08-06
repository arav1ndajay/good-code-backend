import { Box, Button, NavList } from "@primer/react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Home } from "./pages/Home";
export default function App() {
  return (
    <BrowserRouter>
		<Routes>
			<Route index element={<Home />} />
		</Routes>
	</BrowserRouter>
  );
}

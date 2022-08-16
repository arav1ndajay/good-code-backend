import { Box, Button, Header, NavList } from "@primer/react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Category } from "./pages/Category";
import { Docusign } from "./pages/Docusign";
import { Home } from "./pages/Home";
import Account from "./pages/Home/components/Account";
export default function App() {
  return (
    <Box
      minHeight={"100vh"}
      display="flex"
      flexDirection={"column"}
      backgroundColor="canvas.default"
	  position="relative"
	  overflowX="hidden"
    >
      <Header>
        <Header.Item full>
          <Box
            sx={{
              objectFit: "contain",
            }}
          >
            <img
              src="/logo.png"
              style={{
                maxHeight: "40px",
              }}
            />
          </Box>
        </Header.Item>
        <Header.Item>
          <Account />
        </Header.Item>
      </Header>

      <BrowserRouter>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/:categoryId" element={<Category />} />
		  <Route path="/docusign" element={<Docusign />} />
        </Routes>
      </BrowserRouter>
    </Box>
  );
}

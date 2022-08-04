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

{/* <Box
      width={"100vw"}
      height={"100vh"}
      display="flex"
      alignItems="center"
      justifyContent={"center"}
    >
      <Box
        borderColor="border.default"
        p={3}
        borderWidth={1}
        borderStyle="solid"
      >
        <h1>Login</h1>
        <p>
          Since MediaValet needs to be updated after approval, we need you to<br></br>
          give us permission to access the photos on MediaValet
        </p>
        <Button>Login to MediaValet</Button>
      </Box>
    </Box> */}
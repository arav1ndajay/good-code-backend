import { Box, Button } from "@primer/react";
import Logo from "../../public/logo.png";

export function Home() {
  return (
    <Box minHeight={"100vh"} display="flex" flexDirection={"column"}>
      <Box position={"sticky"} top={0} zIndex={1}>
        <Box
          padding={15}
          backgroundColor="canvas.default"
          height={40}
          display="flex"
          justifyContent={"space-between"}
        >
          <Box sx={{
			objectFit: "contain"
		  }}>
            <img
              src="/logo.png"
              style={{
                maxHeight: "40px",
              }}
            />
          </Box>
		  <Box>
			<Button variant="primary">Login</Button>
		  </Box>
        </Box>
      </Box>
    </Box>
  );
}

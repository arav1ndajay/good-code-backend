import { Box, Button, Dialog, Text, Spinner } from "@primer/react";
import { useState, useEffect } from "react";
import Logo from "../../public/logo.png";
import { useParams, useSearchParams } from "react-router-dom";
import request from "superagent";

export function Home() {
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");

    if (code != null) {
      request
        .post("http://localhost:3001/api/authorize")
        .send({ code: code })
        .then((res) => {
          console.log("yay got " + JSON.stringify(res.body));
        });
    }
  }, []);

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
          <Box>
            <Button
              variant="primary"
              onClick={() => {
                setIsLoggingIn(true);
                window.open(
                  "https://login.mediavalet.com/connect/authorize?client_id=7f495f1f-21dc-4f9b-9071-4b56e5375e9f&response_type=code&scope=openid%20api&redirect_uri=http://localhost:3000&state=state-296bc9a0",
                  "_blank"
                );
              }}
            >
              Login
            </Button>
          </Box>
        </Box>
      </Box>
      <Dialog
        isOpen={isLoggingIn}
        onDismiss={() => setIsLoggingIn(false)}
        aria-labelledby="header-id"
      >
        <Dialog.Header id="header-id">Title</Dialog.Header>
      </Dialog>
    </Box>
  );
}

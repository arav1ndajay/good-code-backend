import { Box, Button, Dialog, Text, Spinner } from "@primer/react";
import { useState, useEffect } from "react";
import Logo from "../../public/logo.png";
import { useParams, useSearchParams } from "react-router-dom";
import request from "superagent";
import Account from "../components/Account";

export function Home() {
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");
    const access_token = window.localStorage.getItem("access-token");
    if (code != null && access_token == null) {
      request
        .post("http://localhost:3001/api/authorize")
        .send({ code: code })
        .then((res) => {
          console.log("yay got " + JSON.stringify(res.body));
          if (res.body.access_token !== undefined) {
            localStorage.setItem("access-token", res.body["access_token"]);
          }
        });
    }
  }, []);

  return (
    <Box minHeight={"100vh"} display="flex" flexDirection={"column"}>
      <Box position={"sticky"} top={0} zIndex={1}>
        <Box
          padding={15}
          backgroundColor={"neutral.muted"}
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
          <Box sx={{
			display: "flex",
			alignItems: "center",
		  }}>
            <Account />
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

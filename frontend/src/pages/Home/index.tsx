import { Box, Button, Dialog, Text, Spinner, Header } from "@primer/react";
import { useState, useEffect } from "react";
import Logo from "../../public/logo.png";
import { Outlet, useParams, useSearchParams } from "react-router-dom";
import request from "superagent";
import Account from "./components/Account";
import { Get } from "../../api/Api";
import { useQuery } from "@tanstack/react-query";

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

  const { data, isLoading, isError, error } = useQuery(["folders"], () =>
    Get("http://localhost:3001/categories")
  );

  return (
    <Box minHeight={"100vh"} display="flex" flexDirection={"column"} backgroundColor="canvas.default">
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
      {data && (
        <Box display="grid" gridTemplateColumns="1fr 1fr" gridGap={3}>
          {data?.body.map((folder: { name: string }) => {
            return (
              <Box
                p={3}
                borderColor="border.muted"
                borderWidth={1}
                borderStyle="solid"
              >
                <Text>{folder.name}</Text>
              </Box>
            );
          })}
        </Box>
      )}
    </Box>
  );
}

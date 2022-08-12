import {
  Box,
  Button,
  Dialog,
  Text,
  Spinner,
  Header,
  Link,
  StyledOcticon,
  Heading,
} from "@primer/react";
import { useState, useEffect } from "react";
import Logo from "../../public/logo.png";
import { Outlet, useParams, useSearchParams } from "react-router-dom";
import request from "superagent";
import Account from "./components/Account";
import { Get, NotLoggedInError } from "../../api/Api";
import { useQuery } from "@tanstack/react-query";
import {
  DeviceCameraIcon,
  FileDirectoryFillIcon,
  FileDirectoryIcon,
  KeyIcon,
} from "@primer/octicons-react";
import { Link as RouteLink } from "react-router-dom";

export function Home() {
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");
    const access_token = window.localStorage.getItem("access-token");
    if (code != null && access_token == null) {
      request
        .post("https://api.hackathonjgi.software/api/authorize")
        .send({ code: code })
        .then((res) => {
          console.log("yay got " + JSON.stringify(res.body));
          if (res.body.access_token !== undefined) {
            localStorage.setItem("access-token", res.body["access_token"]);
            localStorage.setItem("refresh-token", res.body["refresh_token"]);
          }
        });
    }
  }, []);

  const { data, isLoading, isError, error } = useQuery(["folders"], () =>
    Get("https://api.hackathonjgi.software/categories")
  );

  var message = "";

  if (isError && error instanceof NotLoggedInError) {
    message = "Please log in to continue";
  } else if (isError) {
    message = "Unexpected error occurred";
  }

  return (
    <>
      <Box p={5} display={"flex"} flexDirection="column" alignItems={"center"}>
        {isLoading && (
          <Spinner
            sx={{
              color: "fg.default",
            }}
          />
        )}
		<Text>{message}</Text>
        {data && (
          <>
            <Box display={"flex"} flexDirection="column">
              <Heading
                as={"h1"}
                sx={{
                  color: "fg.default",
                  mb: 5,
                }}
              >
                Please select a camera trap to view its details
              </Heading>
            </Box>

            <Box display="grid" gridTemplateColumns="1fr 1fr 1fr" gridGap={3}>
              {data?.body.map(
                (folder: { name: string; date: string; id: string }) => {
                  return (
                    <Box
                      p={3}
                      borderColor="border.muted"
                      borderWidth={1}
                      borderStyle="solid"
                      backgroundColor={"neutral.subtle"}
                      borderRadius={6}
                      display="flex"
                      alignItems="center"
                    >
                      <StyledOcticon
                        icon={DeviceCameraIcon}
                        color="fg.default"
                        sx={{
                          mr: 3,
                        }}
                      />
                      <Box display={"flex"} flexDirection="column">
                        <Link
                          as={RouteLink}
                          to={"/" + folder.id + `?date=${folder.date}&camera_id=${folder.name}`}
                          color={"fg.default"}
                        >
                          {folder.name}
                        </Link>
                        <Text
                          sx={{
                            color: "fg.subtle",
                            fontSize: "0.7rem",
                            mt: 1,
                          }}
                        >
                          {folder.date}
                        </Text>
                      </Box>
                    </Box>
                  );
                }
              )}
            </Box>
          </>
        )}
      </Box>
    </>
  );
}

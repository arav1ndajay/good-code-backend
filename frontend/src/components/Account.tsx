import { Button, Spinner, Text } from "@primer/react";
import { useQuery } from "@tanstack/react-query";
import request from "superagent";
import { Get, NotLoggedInError } from "../api/Api";

export default function Account() {
  const { isLoading, data, isError, error } = useQuery(["username"], () =>
    Get("https://api.mediavalet.com/users/current")
  );
  if (isLoading) {
    return <Spinner />;
  }
  if (isError) {
    if (!(error instanceof NotLoggedInError)) {
      localStorage.removeItem("access-token");
    }
    return (
      <Button
        variant="primary"
        onClick={() => {
          window.location.href =
            "https://login.mediavalet.com/connect/authorize?client_id=7f495f1f-21dc-4f9b-9071-4b56e5375e9f&response_type=code&scope=openid%20api&redirect_uri=http://localhost:3000&state=state-296bc9a0";
        }}
      >
        Login
      </Button>
    );
  }

  if (data) {
    return (
      <Text as="p" fontWeight="bold">
        {data.body.payload.userName}
      </Text>
    );
  }

  console.log("error");

  return <div></div>;
}

async function getUsername() {
  if (localStorage.getItem("access-token") != null) {
    const res = await request
      .get("https://api.mediavalet.com/users/current")
      .set("Authorization", `Bearer ${localStorage.getItem("access-token")}`)
      .set("Ocp-Apim-Subscription-Key", import.meta.env.VITE_OCPMID);
    return res;
  } else {
    throw Error("Not logged in");
  }
}

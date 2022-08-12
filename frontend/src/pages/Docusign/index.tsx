import { Box, Button, Spinner, Text } from "@primer/react";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import request from "superagent";
import { Get } from "../../api/Api";

export function Docusign() {
  const [searchParams] = useSearchParams();
  useEffect(() => {
    request
      .get(
        `https://api.hackathonjgi.software/docusign/authorize?code=${searchParams.get(
          "code"
        )}`
      )
      .then((res) => {
        if (res.statusCode == 200) {
          localStorage.setItem("docusign-token", res.body.access_token);
          localStorage.setItem("base_uri", res.body.base_uri);
          localStorage.setItem("account_id", res.body.account_id);
        }
      });
  });

  const { data, isLoading, isError, error } = useQuery(["folders"], () =>
    Get(
      `https://api.hackathonjgi.software/categories/${localStorage.getItem(
        "temp"
      )}`
    )
  );

  return (
    <Box
      display={"flex"}
      width="100%"
      justifyContent={"center"}
      alignItems="center"
    >
      {" "}
      {isLoading && <Spinner />}
      {isError && <Text>Unexpected error occurred</Text>}
      {data && (
        <Button
          variant="primary"
          sx={{
            m: 5,
          }}
          onClick={async () => {
            const res = await request
              .post("https://api.hackathonjgi.software/docusign/notify")
              .send({
                assets: data.body,
                account_id: localStorage.getItem("account_id"),
                access_token: localStorage.getItem("docusign-token"),
                base_uri: localStorage.getItem("base_uri") + "/restapi",
                ds_return_url: "https://hackathonjgi.software",
              });
            window.location.href = res.body["redirect_url"];
          }}
        >
          Ask for approvals
        </Button>
      )}
    </Box>
  );
}

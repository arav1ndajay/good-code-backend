import { Button } from "@primer/react";

export default function Account() {
  return (
    <Button
      variant="primary"
      onClick={() => {
        window.open(
          "https://login.mediavalet.com/connect/authorize?client_id=7f495f1f-21dc-4f9b-9071-4b56e5375e9f&response_type=code&scope=openid%20api&redirect_uri=http://localhost:3000&state=state-296bc9a0",
          "_blank"
        );
      }}
    >
      Login
    </Button>
  );
}

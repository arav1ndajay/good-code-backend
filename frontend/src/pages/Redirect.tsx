import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Redirect() {
  let params = useParams();

  useEffect(() => {
    localStorage.setItem("userId", params.userId!);
  }, [params]);

  return <div>Redirecting...</div>;
}

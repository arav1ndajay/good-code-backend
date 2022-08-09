import { Box } from "@primer/react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { Get } from "../../api/Api";

export function Category() {
  const params = useParams();
  const { data } = useQuery(["folders"], () =>
    Get(`http://localhost:3001/categories/${params.categoryId}`)
  );
  return (
    <Box
      sx={{
        color: "fg.default",
      }}
    >
      {data && <img src={data.body[0].link} />}
    </Box>
  );
}

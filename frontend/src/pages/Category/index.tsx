import { Box, Button, Heading, useOnOutsideClick } from "@primer/react";
import { useQuery } from "@tanstack/react-query";
import { Masonry } from "masonic";
import { useCallback, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { Get } from "../../api/Api";
import { motion } from "framer-motion";
import MapDisplay from "../../components/map";

export function Category() {
  const params = useParams();
  const { data, isError, isLoading } = useQuery(["folders"], () =>
    Get(`http://localhost:3001/categories/${params.categoryId}`)
  );
  const [open, setOpen] = useState(false);

  const drawerRef = useRef(null);

  const closeDrawer = useCallback(() => {
    setOpen(false);
  }, [setOpen, open]);

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flex: 1,
          overflowX: "hidden",
          position: "relative",
        }}
      >
        <MapDisplay x={100} y={100} />
        <Button
          onClick={() => {
            setOpen(!open);
          }}
          sx={{
            position: "absolute",
            right: 30,
            top: 30,
          }}
        >
          View Details
        </Button>
      </Box>
      <Box
        ref={drawerRef}
        as={motion.div}
        sx={{
          position: "absolute",
          top: 0,
          zIndex: 99,
          height: "100vh",
          width: 500,
          backgroundColor: "canvas.default",
          boxShadow: "shadow.small",
          display: "flex",
        }}
        initial={{
          right: -500,
        }}
        animate={{
          right: open ? 0 : -500,
        }}
      >
        <Box
          p={20}
          display="flex"
          justifyContent={"space-between"}
          alignItems="start"
          width={"100%"}
        >
			<Heading>Details Panel</Heading>
          <Button
            onClick={() => {
              closeDrawer();
            }}
          >
            Close
          </Button>
        </Box>
      </Box>
      {/* <Box>
        <Box display={"flex"} flexWrap={"wrap"} justifyContent="center">
          {data &&
            data.body.map((image: { link: string }) => (
              <img src={image.link}></img>
            ))}
        </Box>
      </Box> */}
    </>
  );
}

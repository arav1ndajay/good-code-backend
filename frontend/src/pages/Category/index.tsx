import {
  Box,
  Button,
  Heading,
  Spinner,
  useOnOutsideClick,
  Text
} from "@primer/react";
import { useQuery } from "@tanstack/react-query";
import { useCallback, useRef, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { Get, NotLoggedInError, Post } from "../../api/Api";
import { motion } from "framer-motion";
import MapDisplay from "../../components/map";
import { Question } from "./components/question";

export function Category() {
  const params = useParams();
  const { data, isError, isLoading } = useQuery(["folders"], () =>
    Get(`https://api.hackathonjgi.software/categories/${params.categoryId}`)
  );
  const [open, setOpen] = useState(false);
  const [searchParams] = useSearchParams();

  const {
    data: details,
    isLoading: isMapLoading,
    isSuccess,
    isError: isMapError,
    error: mapError,
  } = useQuery(["details"], () =>
    Post(
      {
        camera_id: searchParams.get("camera_id")!.toLowerCase().charAt(0).toUpperCase() + searchParams.get("camera_id")!.toLowerCase().slice(1),
        date: searchParams.get("date"),
      },
      "https://api.hackathonjgi.software/survey123"
    )
  );

  const drawerRef = useRef(null);

  const closeDrawer = useCallback(() => {
    setOpen(false);
  }, [setOpen, open]);

  var message = "";

  if (isMapError && mapError instanceof NotLoggedInError) {
    message = "Please log in to continue";
  } else if (isError) {
    message = "Unexpected error occurred";
  }

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
        {isLoading && (
          <Box
            width={"100%"}
            m={5}
            display={"flex"}
            alignItems={"center"}
            justifyContent="center"
          >
            {isMapError ? <Text>{message}</Text> : <Spinner />}
          </Box>
        )}
        {isSuccess && (
          <MapDisplay
            x={details.body["X"]}
            y={details.body["Y"]}
            details={details.body}
          />
        )}
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
          flexDirection: "column",
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
        >
          <Heading>Details Panel</Heading>
          <Button
            onClick={() => {
              closeDrawer();
            }}
            variant="danger"
          >
            Close
          </Button>
        </Box>
        {details && data && (
          <Question question={details.body} images={data.body} />
        )}
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

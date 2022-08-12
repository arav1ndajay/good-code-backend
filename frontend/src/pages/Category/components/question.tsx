import { Box, Heading, Text } from "@primer/react";

export function Question({
  question,
  images,
}: {
  question: { [key: string]: string };
  images: Array<{ link: string }>;
}) {
  return (
    <Box overflowY={"scroll"}>
      {Object.keys(question).map((key) => (
        <Box display={"flex"} flexDirection="column">
          <Heading
            as={"h6"}
            sx={{
              fontSize: 3,
              m: 4,
            }}
          >
            {key}
          </Heading>
          <Text marginX={4}>{question[key]}</Text>
        </Box>
      ))}
      <Heading
        as={"h6"}
        sx={{
          fontSize: 3,
          m: 4,
        }}
      >
        Images
      </Heading>
      {images &&
        images.map((image: { link: string }) => <img src={image.link} style={{
			width: "100%"
		}}></img>)}
    </Box>
  );
}

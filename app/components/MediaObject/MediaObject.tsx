import { AspectRatio, Box, Image, Overlay } from "@mantine/core";
import type { Media } from "~/api";
import { Carousel } from "@mantine/carousel";

function MediaDisplay(props: { media: Media }) {
  let media;
  let bgUrl =
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixid=M3wxMTI1OHwwfDF8cmFuZG9tfHx8fHx8fHx8MTc0MDQ4OTMxOXw&ixlib=rb-4.0.3&q=85&w=2640";

  switch (props.media.type) {
    case "image":
      media = (
        <Image
          style={{ zIndex: 1 }}
          fit="contain"
          src={`/api/media/${props.media.id}`}
        />
      );
      bgUrl = `/api/media/${props.media.id}`;
      break;
    case "video":
      media = (
        <video
          style={{ objectFit: "contain", marginBottom: "-0.5rem" }}
          src={`/api/media/${props.media.id}`}
          controls
        />
      );
      break;
    case "audio":
      media = (
        <audio
          style={{ objectFit: "contain" }}
          src={`/api/media/${props.media.id}`}
          controls
        />
      );
      break;
    default:
      media = "oops";
  }

  return (
    <AspectRatio ratio={3 / 2}>
      <Box pos="absolute" style={{ zIndex: -1 }}>
        <Image h="100%" w="100%" src={bgUrl} />
        <Overlay color="#000" backgroundOpacity={0.35} blur={15} />
      </Box>
      {media}
    </AspectRatio>
  );
}

export function MediaObject(props: { mediaList: Media[] }) {
  const slides = props.mediaList.map((media) => (
    <Carousel.Slide key={media.id}>
      <MediaDisplay media={media} />
    </Carousel.Slide>
  ));

  if (props.mediaList.length === 0) {
    return;
  } else if (props.mediaList.length === 1) {
    return (
      <Box pos="relative" style={{ zIndex: 0 }}>
        <MediaDisplay media={props.mediaList[0]} />
      </Box>
    );
  } else {
    return <Carousel withIndicators>{slides}</Carousel>;
  }
}

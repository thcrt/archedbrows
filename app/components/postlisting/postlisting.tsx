import {
  Anchor,
  AspectRatio,
  Box,
  Card,
  Group,
  Image,
  Overlay,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import ReactTimeAgo from "react-time-ago";
import type { Media, Post } from "~/api";
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

export function PostMedia(props: { mediaList: Media[] }) {
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

export function PostListing(post: Post) {
  return (
    <Card w="100%" maw="60rem" shadow="sm" radius="md" withBorder>
      <Card.Section
        component="a"
        py="sm"
        inheritPadding
        style={{ textDecoration: "none", color: "inherit" }}
        href={`/posts/${post.id}`}
      >
        <Title order={3} fw={500} size="xl">
          {post.title}
        </Title>
        <Text c="dimmed" size="xs">
          <Anchor>{post.author}</Anchor>{" "}
          <ReactTimeAgo
            date={new Date(post.time_created!)}
            timeStyle="round-minute"
          />{" "}
          <Anchor href={post.source_url} target="_blank">
            {post.source}
          </Anchor>
        </Text>
      </Card.Section>

      <Card.Section>
        <PostMedia mediaList={post.media} />
      </Card.Section>

      {post.text ? (
        <Card.Section
          component="a"
          py="sm"
          inheritPadding
          style={{ textDecoration: "none", color: "inherit" }}
          href={`/posts/${post.id}`}
        >
          <Text size="sm" c="dimmed">
            {post.text}
          </Text>
        </Card.Section>
      ) : (
        ""
      )}
    </Card>
  );
}

export function PostDisplay(post: Post) {
  return (
    <Stack w="100%" maw="80rem" mx="auto">
      <Stack gap="0">
        <Title order={3} fw={500} size="xl">
          {post.title}
        </Title>
        <Text c="dimmed" size="xs">
          posted by <Anchor>{post.author}</Anchor>{" "}
          <ReactTimeAgo
            date={new Date(post.time_created!)}
            timeStyle="round-minute"
          />
          , archived from{" "}
          <Anchor href={post.source_url} target="_blank">
            {post.source}
          </Anchor>{" "}
          <ReactTimeAgo date={new Date(post.time_added!)} timeStyle="round-minute"/>{" "}
        </Text>
      </Stack>
      <PostMedia mediaList={post.media} />
      <Text>{post.text}</Text>
    </Stack>
  );
}

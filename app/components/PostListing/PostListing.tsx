import { Anchor, Card, Text, Title } from "@mantine/core";
import ReactTimeAgo from "react-time-ago";
import type { Post } from "~/api";
import { MediaObject } from "../MediaObject/MediaObject";

export function PostListing({ post }: { post: Post }) {
  return (
    <Card
      w="100%"
      maw="60rem"
      shadow="sm"
      radius="md"
      withBorder
    >
      <Card.Section
        pt="sm"
        inheritPadding
        style={{ textDecoration: "none", color: "inherit" }}
      >
        <Anchor
          style={{ textDecoration: "none", color: "inherit" }}
          href={`/posts/${post.id.toString()}`}
        >
          <Title
            order={3}
            fw={500}
            size="xl"
          >
            {post.title}
          </Title>
        </Anchor>
        <Text
          c="dimmed"
          size="xs"
        >
          <Anchor>{post.author}</Anchor>{" "}
          {post.time_created ? (
            <ReactTimeAgo
              date={new Date(post.time_created)}
              timeStyle="round-minute"
            />
          ) : (
            ""
          )}{" "}
          <Anchor
            href={post.source_url}
            target="_blank"
          >
            {post.source}
          </Anchor>
        </Text>
      </Card.Section>

      {post.media.length ? (
        <Card.Section pt="sm">
          <MediaObject mediaList={post.media} />
        </Card.Section>
      ) : (
        ""
      )}

      {post.text ? (
        <Card.Section
          component="a"
          py="sm"
          inheritPadding
          style={{ textDecoration: "none", color: "inherit" }}
          href={`/posts/${post.id.toString()}`}
        >
          <Text
            size="sm"
            c="dimmed"
            lineClamp={4}
          >
            {post.text}
          </Text>
        </Card.Section>
      ) : (
        ""
      )}
    </Card>
  );
}

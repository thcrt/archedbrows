import { Anchor, Card, Text, Title } from "@mantine/core";
import ReactTimeAgo from "react-time-ago";
import type { Post } from "~/api";
import { MediaObject } from "../MediaObject/MediaObject";

export function PostListing({ post }: { post: Post }) {
  return (
    <Card w="100%" maw="60rem" shadow="sm" radius="md" withBorder>
      <Card.Section
        py="sm"
        inheritPadding
        style={{ textDecoration: "none", color: "inherit" }}
      >
        <Anchor
          style={{ textDecoration: "none", color: "inherit" }}
          href={`/posts/${post.id}`}
        >
          <Title order={3} fw={500} size="xl">
            {post.title}
          </Title>
        </Anchor>
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
        <MediaObject mediaList={post.media} />
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

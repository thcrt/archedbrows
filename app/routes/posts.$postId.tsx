import type { Route } from "./+types/posts.$postId";
import { PostDisplay } from "~/components/PostDisplay/PostDisplay";
import { ActionIcon, Anchor, Text } from "@mantine/core";
import ReactTimeAgo from "react-time-ago";
import type { Post } from "~/api";
import { IconPencil } from "@tabler/icons-react";
import { MediaObject } from "~/components/MediaObject/MediaObject";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const res = await fetch(`/api/posts/${params.postId}`);
  const post: Post = await res.json();
  return post;
}

export default function ShowPost({ loaderData }: Route.ComponentProps) {
  const post = loaderData;

  return (
    <PostDisplay
      title={post.title}
      back="/"
      meta={
        <>
          posted by <Anchor>{post.author}</Anchor>{" "}
          <ReactTimeAgo
            date={new Date(post.time_created!)}
            timeStyle="round-minute"
          />
          , archived from{" "}
          <Anchor href={post.source_url} target="_blank">
            {post.source}
          </Anchor>{" "}
          <ReactTimeAgo
            date={new Date(post.time_added!)}
            timeStyle="round-minute"
          />{" "}
        </>
      }
      buttons={
        <ActionIcon
          component="a"
          href={`/posts/${post.id}/edit`}
          h="100%"
          w="auto"
          px="sm"
          variant="default"
        >
          <IconPencil />
        </ActionIcon>
      }
    >
      <MediaObject mediaList={post.media} />
      <Text>{post.text}</Text>
    </PostDisplay>
  );
}

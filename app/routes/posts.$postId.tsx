import type { Route } from "./+types/posts.$postId";
import { PostDisplay } from "~/components/PostDisplay/PostDisplay";
import { Anchor, Text } from "@mantine/core";
import ReactTimeAgo from "react-time-ago";
import type { Post } from "~/api";
import { IconPencil } from "@tabler/icons-react";
import { MediaObject } from "~/components/MediaObject/MediaObject";
import { LinkButton } from "~/components/Button/Button";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const res = await fetch(`/api/posts/${params.postId}`);
  const post = (await res.json()) as Post;
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
          {post.time_created ? (
            <ReactTimeAgo
              date={new Date(post.time_created)}
              timeStyle="round-minute"
            />
          ) : (
            ""
          )}
          , archived from{" "}
          <Anchor
            href={post.source_url}
            target="_blank"
          >
            {post.source}
          </Anchor>{" "}
          <ReactTimeAgo
            date={new Date(post.time_added)}
            timeStyle="round-minute"
          />{" "}
        </>
      }
      buttons={
        <LinkButton
          href={`/posts/${post.id.toString()}/edit`}
          variant="default"
        >
          <IconPencil />
        </LinkButton>
      }
    >
      <MediaObject mediaList={post.media} />
      <Text>{post.text}</Text>
    </PostDisplay>
  );
}

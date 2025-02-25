import type { Post } from "~/api";
import type { Route } from "./+types/posts.$postId_.edit";
import { PostDisplay } from "~/components/PostDisplay/PostDisplay";
import { Group, Stack, Text, Title, ActionIcon } from "@mantine/core";
import {
  IconDeviceFloppy,
  IconTrash,
  IconArrowLeft,
} from "@tabler/icons-react";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const res = await fetch(`/api/posts/${params.postId}`);
  const post: Post = await res.json();
  return post;
}

export default function ShowPost({ loaderData }: Route.ComponentProps) {
  const post = loaderData;

  return (
    <PostDisplay
      title={`Editing post #${post.id}`}
      back={`/posts/${post.id}`}
      buttons={
        <>
          <ActionIcon component="a" h="100%" w="auto" px="sm" color="red">
            <IconTrash />
          </ActionIcon>
          <ActionIcon
            component="a"
            display="block"
            h="100%"
            w="5.6rem"
            color="green"
          >
            <IconDeviceFloppy />
          </ActionIcon>
        </>
      }
    >
      editing
    </PostDisplay>
  );
}

import type { Post } from "~/api";
import type { Route } from "./+types/posts.$postId_.edit";
import { PostDisplay } from "~/components/PostDisplay/PostDisplay";
import {
  IconDeviceFloppy,
  IconTrash,
} from "@tabler/icons-react";
import { ActionButton, LinkButton } from "~/components/Button/Button";

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
          <LinkButton color="red" href="#">
            <IconTrash />
          </LinkButton>
          <ActionButton color="green" w="5.6rem" onClick={() => alert("saved!")}>
            <IconDeviceFloppy />
          </ActionButton>
        </>
      }
    >
      editing
    </PostDisplay>
  );
}

import { Shell } from "../shell";
import type { Post } from "~/api";
import type { Route } from "./+types/posts.$postId";
import { PostDisplay } from "~/components/postlisting/postlisting";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const res = await fetch(`/api/posts/${params.postId}`);
  const post: Post = await res.json();
  return post;
}

export default function ShowPost({ loaderData }: Route.ComponentProps) {
  const post = loaderData;

  return <PostDisplay {...post} />;
}

import type { Route } from "./+types/_index";
import type { Post } from "~/api";
import { PostListing } from "~/components/postlisting/postlisting";
import { Stack } from "@mantine/core";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const res = await fetch(`/api/posts`);
  const posts: Post[] = await res.json();
  return posts;
}

export default function IndexPosts({ loaderData }: Route.ComponentProps) {
  const posts = loaderData.map((post) => (
    <PostListing key={post.id} {...post} />
  ));

  return <Stack align="center">{posts}</Stack>;
}

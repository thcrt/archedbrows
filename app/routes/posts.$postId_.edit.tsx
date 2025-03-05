import type { Post } from "~/api";
import type { Route } from "./+types/posts.$postId_.edit";
import { PostDisplay } from "~/components/PostDisplay/PostDisplay";
import {
  IconCalendarClock,
  IconDeviceFloppy,
  IconLink,
} from "@tabler/icons-react";
import { ActionButton } from "~/components/Button/Button";
import { Stack, TextInput } from "@mantine/core";
import { DateTimePicker } from "@mantine/dates";
import { useForm } from "@mantine/form";
import validator from "validator";
import { redirect, useFetcher } from "react-router";
import DeletePostButton from "~/components/DeletePostButton/DeletePostButton";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  const res = await fetch(`/api/posts/${params.postId}`);
  const post = (await res.json()) as Post;
  return post;
}

export async function clientAction({
  request,
  params,
}: Route.ClientActionArgs) {
  const data = await request.formData();
  const id = params.postId;
  const intent = data.get("intent");

  // Prevent intent being passed to backend as field to update
  data.delete("intent");

  if (intent === "edit") {
    return await fetch(`/api/posts/${id}`, {
      method: "PATCH",
      body: data,
    });
  } else if (intent === "delete") {
    const confirmation = data.get("confirmation");
    if (
      typeof confirmation === "string" &&
      confirmation.toLowerCase() === "delete"
    ) {
      await fetch(`/api/posts/${id}`, {
        method: "DELETE",
      });
      return redirect("/");
    } else {
      return { ok: false, error: "Please confirm deletion" };
    }
  } else {
    throw new Error(`Invalid intent!`);
  }
}

export default function ShowPost({ loaderData }: Route.ComponentProps) {
  const post = loaderData;
  const fetcher = useFetcher();

  const form = useForm({
    initialValues: {
      ...post,
      time_created: post.time_created
        ? new Date(post.time_created + "")
        : undefined,
    },
    validateInputOnChange: true,

    validate: {
      source_url: (value) =>
        !validator.isURL(value) ? "Must be a valid URL" : null,
    },
  });

  return (
    <fetcher.Form method="post">
      <PostDisplay
        title={`Editing post #${post.id.toString()}`}
        back={`/posts/${post.id.toString()}`}
        buttons={
          <>
            <DeletePostButton />
            <ActionButton
              color="green"
              w="5.6rem"
              type="submit"
              name="intent"
              value="edit"
            >
              <IconDeviceFloppy />
            </ActionButton>
          </>
        }
      >
        <Stack>
          <TextInput
            label="Title"
            name="title"
            key={form.key("title")}
            {...form.getInputProps("title")}
          />
          <TextInput
            label="Author"
            name="author"
            key={form.key("author")}
            {...form.getInputProps("author")}
          />
          <TextInput
            label="Source"
            name="source"
            key={form.key("source")}
            {...form.getInputProps("source")}
          />
          <DateTimePicker
            withSeconds
            label="Posted"
            name="time_created"
            leftSection={<IconCalendarClock size="1.25em" />}
            key={form.key("time_created")}
            {...form.getInputProps("time_created")}
          />
          <TextInput
            label="URL"
            name="source_url"
            leftSection={<IconLink size="1.25em" />}
            key={form.key("source_url")}
            {...form.getInputProps("source_url")}
          />
        </Stack>
      </PostDisplay>
    </fetcher.Form>
  );
}

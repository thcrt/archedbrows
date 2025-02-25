import { ActionIcon, TextInput } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { modals } from "@mantine/modals";

export function CreateButton() {
  const addPost = () =>
    modals.open({
      title: "Add post",
      size: "xl",
      children: (
        <form method="post" action="/api/posts/add">
          <TextInput
            label="URL"
            size="md"
            placeholder="https://example.com/posts/12345"
            data-autofocus
            name="url"
            rightSection={
              <ActionIcon
                type="submit"
                variant="filled"
                color="green"
                size="var(--input-height)"
                radius="0 var(--input-radius) var(--input-radius) 0"
              >
                <IconPlus />
              </ActionIcon>
            }
          />
        </form>
      ),
    });

  return (
    <ActionIcon
      onClick={addPost}
      variant="filled"
      color="green"
      w="3rem"
      h="2rem"
    >
      <IconPlus />
    </ActionIcon>
  );
}

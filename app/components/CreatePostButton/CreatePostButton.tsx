import { ActionIcon, TextInput, Modal, Input } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { ActionButton } from "../Button/Button";
import { useDisclosure } from "@mantine/hooks";

export default function CreatePostButton() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <ActionButton
        onClick={open}
        color="green"
        w="8rem"
      >
        <IconPlus stroke={4} />
      </ActionButton>

      <Modal
        opened={opened}
        onClose={close}
        title="Add post"
        size="xl"
      >
        <form
          method="post"
          action="/api/posts"
        >
          <Input
            type="hidden"
            name="auto"
            value=""
          ></Input>
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
                size="100%"
                radius="0 var(--input-radius) var(--input-radius) 0"
              >
                <IconPlus />
              </ActionIcon>
            }
          />
        </form>
      </Modal>
    </>
  );
}

import { ActionIcon, TextInput, Modal, Input } from "@mantine/core";
import { IconLink, IconPlus } from "@tabler/icons-react";
import { ActionButton } from "../Button/Button";
import { useDisclosure } from "@mantine/hooks";
import { useForm } from "@mantine/form";
import validator from "validator";

export default function CreatePostButton() {
  const [opened, { open, close }] = useDisclosure(false);

  const form = useForm({
    initialValues: {
      url: "",
    },
    validateInputOnChange: true,
    validateInputOnBlur: true,
    onSubmitPreventDefault: "validation-failed",
    validate: {
      url: (value) => (!validator.isURL(value) ? "Must be a valid URL" : null),
    },
  });

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
          onSubmit={form.validate}
        >
          <Input
            type="hidden"
            name="auto"
            value=""
          ></Input>
          <TextInput
            key={form.key("url")}
            {...form.getInputProps("url")}
            label="URL"
            size="md"
            placeholder="https://example.com/posts/12345"
            data-autofocus
            name="url"
            required
            leftSection={<IconLink size="1.25em" />}
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

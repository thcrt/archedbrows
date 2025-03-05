import { IconTrash } from "@tabler/icons-react";
import { ActionButton } from "~/components/Button/Button";
import { Modal, Text, Stack, Code, PinInput } from "@mantine/core";
import { useFetcher } from "react-router";
import { useDisclosure } from "@mantine/hooks";

export default function DeletePostButton() {
  const fetcher = useFetcher();
  const [opened, { open, close }] = useDisclosure(false);

  let confirmDeletionError = false;
  if (
    "error" in fetcher.data &&
    (fetcher.data as { ok: boolean; error: string }).error ===
      "Please confirm deletion"
  ) {
    confirmDeletionError = true;
  }

  return (
    <>
      <ActionButton
        color="red"
        onClick={open}
      >
        <IconTrash />
      </ActionButton>

      <Modal
        opened={opened}
        onClose={close}
        size="xl"
        title="Delete Post"
      >
        <Stack
          align="center"
          gap="xs"
        >
          <Text>
            Are you <b>sure</b> you want to delete this post? This can&apos;t be
            undone!
          </Text>
          <Text {...(confirmDeletionError ? { c: "red" } : {})}>
            To confirm, please type <Code>delete</Code> into the field below.
          </Text>
          <fetcher.Form method="post">
            <PinInput
              my="2rem"
              type={/[deleteDELETE]/}
              length={6}
              name="confirmation"
              size="lg"
              autoFocus={true}
              getInputProps={(i) => {
                return {
                  placeholder: "delete"[i],
                  autoComplete: "off",
                };
              }}
            />
            <ActionButton
              type="submit"
              name="intent"
              value="delete"
              variant="filled"
              color="red"
              disabled={fetcher.state === "submitting"}
              w="100%"
            >
              Permanently delete this post
            </ActionButton>
          </fetcher.Form>
        </Stack>
      </Modal>
    </>
  );
}

import { ActionIcon, AppShell, Burger, Flex, TextInput } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Brand } from "./components/brand/brand";
import { IconPlus } from "@tabler/icons-react";
import { modals } from "@mantine/modals";

export function Shell() {
  const addPost = () =>
    modals.open({
      title: "Add post",
      size: "xl",
      children: (
        <TextInput
          label="URL"
          size="md"
          placeholder="https://example.com/posts/12345"
          data-autofocus
          rightSection={
            <ActionIcon
              onClick={modals.closeAll}
              variant="filled"
              color="green"
              size="var(--input-height)"
              radius="0 var(--input-radius) var(--input-radius) 0"
            >
              <IconPlus />
            </ActionIcon>
          }
        />
      ),
    });

  const [opened, { toggle }] = useDisclosure();

  return (
    <AppShell header={{ height: "3rem" }} padding="md">
      <AppShell.Header>
        <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
        <Flex justify="space-between" align="center" h="100%" px="xs">
          <Brand />
          <ActionIcon
            onClick={addPost}
            variant="filled"
            color="green"
            w="3rem"
            h="2rem"
          >
            <IconPlus />
          </ActionIcon>
        </Flex>
      </AppShell.Header>

      <AppShell.Main>Main</AppShell.Main>
    </AppShell>
  );
}

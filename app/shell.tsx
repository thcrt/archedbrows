import { AppShell, Flex, Group } from "@mantine/core";
import { Brand } from "./components/Brand/Brand";
import CreatePostButton from "./components/CreatePostButton/CreatePostButton";
import { LinkButton } from "./components/Button/Button";
import { IconPencilPlus } from "@tabler/icons-react";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell
      header={{ height: "3.5rem" }}
      padding="md"
      h="100%"
    >
      <AppShell.Header>
        <Flex
          justify="space-between"
          align="center"
          h="100%"
          px="xs"
        >
          <Brand />
          <Group gap="xs">
            <LinkButton
              variant="outline"
              color="green"
              href="/posts/create"
            >
              <IconPencilPlus />
            </LinkButton>
            <CreatePostButton />
          </Group>
        </Flex>
      </AppShell.Header>

      <AppShell.Main h="100%">{children}</AppShell.Main>
    </AppShell>
  );
}

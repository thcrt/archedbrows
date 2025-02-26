import { AppShell, Flex } from "@mantine/core";
import { Brand } from "./components/Brand/Brand";
import { CreatePostButton } from "./components/CreatePostButton/CreatePostButton";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell header={{ height: "3.5rem" }} padding="md">
      <AppShell.Header>
        <Flex justify="space-between" align="center" h="100%" px="xs">
          <Brand />
          <CreatePostButton />
        </Flex>
      </AppShell.Header>

      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}

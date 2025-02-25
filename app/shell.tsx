import { AppShell, Flex } from "@mantine/core";
import { Brand } from "./components/brand/brand";
import { CreateButton } from "./components/createbutton/createbutton";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <AppShell header={{ height: "3rem" }} padding="md">
      <AppShell.Header>
        <Flex justify="space-between" align="center" h="100%" px="xs">
          <Brand />
          <CreateButton />
        </Flex>
      </AppShell.Header>

      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}

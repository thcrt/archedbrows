import { AppShell, Burger, Flex } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Brand } from "./components/brand/brand";
import { CreateButton } from "./components/createbutton/createbutton";

export function Shell({ children }: { children: React.ReactNode }) {
  const [opened, { toggle }] = useDisclosure();

  return (
    <AppShell header={{ height: "3rem" }} padding="md">
      <AppShell.Header>
        <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
        <Flex justify="space-between" align="center" h="100%" px="xs">
          <Brand />
          <CreateButton />
        </Flex>
      </AppShell.Header>

      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}

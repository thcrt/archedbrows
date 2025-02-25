import { ActionIcon, Group, Stack, Text, Title } from "@mantine/core";
import { IconArrowLeft } from "@tabler/icons-react";

export function PostDisplay({
  back,
  title,
  meta,
  buttons,
  children,
}: {
  back?: string;
  title: string;
  meta?: React.ReactNode;
  buttons: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <Stack w="100%" maw="80rem" mx="auto">
      <Group
        display="flex"
        style={{ alignItems: "center" }}
        pos="relative"
        h="3rem"
      >
        {back ? (
          <ActionIcon
            component="a"
            h="100%"
            href={back}
            pos="absolute"
            left="-4rem"
            w="auto"
            px="sm"
            variant="subtle"
            color="grey"
          >
            <IconArrowLeft />
          </ActionIcon>
        ) : (
          ""
        )}

        <Stack
          gap="0"
          style={{ justifyContent: "space-between" }}
          h="100%"
          mr="auto"
        >
          <Title my="auto" order={3} fw={500} size="xl">
            {title}
          </Title>
          {meta ? (
            <Text c="dimmed" size="xs">
              {meta}
            </Text>
          ) : (
            ""
          )}
        </Stack>
        {buttons}
      </Group>
      {children}
    </Stack>
  );
}

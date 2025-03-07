import { Group, Stack, Text, Title, type StackProps } from "@mantine/core";
import { IconArrowLeft } from "@tabler/icons-react";
import { LinkButton } from "../Button/Button";

interface PostDisplayProps extends StackProps {
  back?: string;
  title: string;
  meta?: React.ReactNode;
  buttons: React.ReactNode;
  children: React.ReactNode;
}

export function PostDisplay({
  back,
  title,
  meta,
  buttons,
  children,
  ...props
}: PostDisplayProps) {
  return (
    <Stack
      w="100%"
      maw="80rem"
      mx="auto"
      {...props}
    >
      <Group
        style={{ alignItems: "start", flexWrap: "nowrap" }}
        pos="relative"
        mih="3rem"
      >
        {back ? (
          <LinkButton
            href={back}
            pos="absolute"
            left="-4rem"
            variant="subtle"
            color="grey"
          >
            <IconArrowLeft />
          </LinkButton>
        ) : (
          ""
        )}

        <Stack
          gap="0"
          style={{ alignSelf: "center", justifyContent: "space-between" }}
          h="100%"
          mr="auto"
        >
          <Title
            my="auto"
            order={3}
            fw={500}
            size="xl"
          >
            {title}
          </Title>
          {meta ? (
            <Text
              c="dimmed"
              size="xs"
            >
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

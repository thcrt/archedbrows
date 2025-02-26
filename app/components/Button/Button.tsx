import {
  ActionIcon,
  type ActionIconProps,
  type ElementProps,
} from "@mantine/core";

interface ActionButtonProps
  extends ActionIconProps,
    ElementProps<"button", keyof ActionIconProps> {}

export function ActionButton(props: ActionButtonProps) {
  return (
    <ActionIcon h="3rem" fw={500} p="sm" w="auto" miw="3rem" {...props}>
      {props.children}
    </ActionIcon>
  );
}

interface LinkButtonProps
  extends ActionIconProps,
    ElementProps<"a", keyof ActionIconProps> {}

export function LinkButton(props: LinkButtonProps) {
  return (
    <ActionIcon
      component="a"
      h="3rem"
      fw={500}
      p="sm"
      w="auto"
      miw="3rem"
      {...props}
    >
      {props.children}
    </ActionIcon>
  );
}

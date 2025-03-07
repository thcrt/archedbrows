import { PostDisplay } from "~/components/PostDisplay/PostDisplay";
import {
  IconCalendarClock,
  IconDeviceFloppy,
  IconFileUnknown,
  IconLink,
  IconTrash,
} from "@tabler/icons-react";
import { ActionButton, LinkButton } from "~/components/Button/Button";
import {
  Text,
  Image,
  Stack,
  TextInput,
  Textarea,
  Group,
  Paper,
} from "@mantine/core";
import { DateTimePicker } from "@mantine/dates";
import { useForm } from "@mantine/form";
import validator from "validator";
import { IconUpload, IconPhoto, IconX } from "@tabler/icons-react";
import { Dropzone, type FileWithPath } from "@mantine/dropzone";
import { useRef, useState } from "react";
import MIMEType from "whatwg-mimetype";

export default function ShowPost() {
  const [media, setMedia] = useState<FileWithPath[]>([]);
  const mediaInput = useRef<HTMLInputElement>(null);

  const previews = media.map((file, index) => {
    switch (new MIMEType(file.type).type) {
      case "image": {
        const imageUrl = URL.createObjectURL(file);
        return (
          <Image
            key={index}
            flex={1}
            src={imageUrl}
            h="8rem"
            onLoad={() => {
              URL.revokeObjectURL(imageUrl);
            }}
          />
        );
      }
      default: {
        return (
          <Paper
            h="8rem"
            flex={1}
            key={index}
            withBorder
            p="sm"
          >
            <Stack align="center">
              <IconFileUnknown size="4rem" />
              <Text
                c="dimmed"
                lineClamp={1}
              >
                {file.name}
              </Text>
            </Stack>
          </Paper>
        );
      }
    }
  });

  const form = useForm({
    initialValues: {
      source_url: "",
    },
    validateInputOnChange: true,
    validate: {
      source_url: (value) =>
        !validator.isURL(value) ? "Must be a valid URL" : null,
    },
  });

  return (
    <form
      method="post"
      encType="multipart/form-data"
      action="/api/posts"
      style={{
        height: "100%",
      }}
    >
      <PostDisplay
        title={`Create new post`}
        back={`/`}
        h="100%"
        buttons={
          <>
            <LinkButton
              color="red"
              href="/"
            >
              <IconTrash />
            </LinkButton>
            <ActionButton
              color="green"
              w="5.6rem"
              type="submit"
            >
              <IconDeviceFloppy />
            </ActionButton>
          </>
        }
      >
        <Stack
          h="100%"
          pb="xl"
        >
          <TextInput
            label="Title"
            name="title"
            key={form.key("title")}
            {...form.getInputProps("title")}
          />
          <TextInput
            label="Author"
            name="author"
            key={form.key("author")}
            {...form.getInputProps("author")}
          />
          <TextInput
            label="Source"
            name="source"
            key={form.key("source")}
            {...form.getInputProps("source")}
          />
          <DateTimePicker
            withSeconds
            label="Posted"
            name="time_created"
            leftSection={<IconCalendarClock size="1.25em" />}
            key={form.key("time_created")}
            {...form.getInputProps("time_created")}
          />
          <TextInput
            label="URL"
            name="source_url"
            leftSection={<IconLink size="1.25em" />}
            key={form.key("source_url")}
            {...form.getInputProps("source_url")}
          />
          <Textarea
            label="Text"
            name="text"
            style={{
              flexGrow: 1,
            }}
            pb="2rem"
            styles={{
              wrapper: {
                height: "100%",
              },
              input: {
                height: "100%",
              },
            }}
            key={form.key("text")}
            {...form.getInputProps("text")}
          />
          <input
            {...form.getInputProps("media")}
            type="file"
            multiple
            name="media"
            key={form.key("media")}
            hidden
            ref={mediaInput}
          />
          <Dropzone
            onDrop={(newMedia) => {
              setMedia([...media, ...newMedia]);
              if (mediaInput.current?.files) {
                const dt = new DataTransfer();
                for (const m of [...mediaInput.current.files, ...newMedia]) {
                  dt.items.add(m);
                }
                mediaInput.current.files = dt.files;
              }
            }}
          >
            <Stack
              align="center"
              justify="center"
              mih="12rem"
              gap="xs"
              style={{ pointerEvents: "none" }}
            >
              <Dropzone.Accept>
                <IconUpload
                  size={52}
                  color="var(--mantine-color-blue-6)"
                  stroke={1.5}
                />
              </Dropzone.Accept>
              <Dropzone.Reject>
                <IconX
                  size={52}
                  color="var(--mantine-color-red-6)"
                  stroke={1.5}
                />
              </Dropzone.Reject>
              <Dropzone.Idle>
                <Group>
                  {previews.length === 0 ? (
                    <IconPhoto
                      size={52}
                      color="var(--mantine-color-dimmed)"
                      stroke={1.5}
                    />
                  ) : (
                    previews
                  )}
                </Group>
              </Dropzone.Idle>
              <Text c="dimmed">Drag files here or click to add media</Text>
            </Stack>
          </Dropzone>
        </Stack>
      </PostDisplay>
    </form>
  );
}

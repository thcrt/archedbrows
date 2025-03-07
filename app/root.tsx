import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";
import {
  ColorSchemeScript,
  MantineProvider,
  mantineHtmlProps,
  Loader,
  Center,
  createTheme,
} from "@mantine/core";
import { Shell } from "./shell";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
import { DatesProvider } from "@mantine/dates";

dayjs.extend(customParseFormat);

import "@mantine/core/styles.css";
import "@mantine/carousel/styles.css";
import "@mantine/dates/styles.css";
import "@mantine/dropzone/styles.css";

TimeAgo.addDefaultLocale(en);

export function meta() {
  return [
    {
      title: "archedbrows",
    },
    {
      name: "apple-mobile-web-app-title",
      content: "archedbrows",
    },
  ];
}

export function links() {
  return [
    {
      rel: "icon",
      sizes: "96x96",
      type: "image/png",
      href: "/favicon-96x96.png",
    },
    {
      rel: "icon",
      type: "image/svg+xml",
      href: "/favicon.svg",
    },
    {
      rel: "shortcut icon",
      href: "/favicon.ico",
    },
    {
      rel: "apple-touch-icon",
      sizes: "180x180",
      href: "/apple-touch-icon.png",
    },
    {
      rel: "manifest",
      href: "/site.webmanifest",
    },
  ];
}

export function HydrateFallback() {
  return (
    <Center
      pos="fixed"
      h="100%"
      w="100%"
    >
      <Loader
        color="currentColor"
        size="xl"
      />
    </Center>
  );
}

const theme = createTheme({
  fontFamily: "Inter, Helvetica Neue, Helvetica, Arial, sans-serif",
});

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      {...mantineHtmlProps}
    >
      <head>
        <meta charSet="utf-8" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1"
        />
        <ColorSchemeScript defaultColorScheme="auto" />
        <Meta />
        <Links />
      </head>
      <body
        style={{
          height: "100svh",
        }}
      >
        <MantineProvider
          theme={theme}
          defaultColorScheme="auto"
        >
          <DatesProvider settings={{}}>
            <Shell>{children}</Shell>
          </DatesProvider>
        </MantineProvider>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}

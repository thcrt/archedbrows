import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";
import {
  ColorSchemeScript,
  MantineProvider,
  mantineHtmlProps,
  Loader,
  Center,
  createTheme,
} from "@mantine/core";
import { ModalsProvider } from "@mantine/modals";
import type { Route } from "./routes/+types/_index";
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

TimeAgo.addDefaultLocale(en);

export function meta({}: Route.MetaArgs) {
  return [{ title: "archedbrows" }];
}

export function HydrateFallback() {
  return (
    <Center pos="fixed" h="100%" w="100%">
      <Loader color="currentColor" size="xl" />
    </Center>
  );
}

const theme = createTheme({
  fontFamily: "Inter, Helvetica Neue, Helvetica, Arial, sans-serif",
});

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" {...mantineHtmlProps}>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <ColorSchemeScript defaultColorScheme="auto" />
        <Meta />
        <Links />
      </head>
      <body>
        <MantineProvider theme={theme} defaultColorScheme="auto">
          <ModalsProvider>
            <DatesProvider settings={{}}>
              <Shell>{children}</Shell>
            </DatesProvider>
          </ModalsProvider>
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

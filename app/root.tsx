import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";
import type { Route } from "./routes/+types/_index";
import { Shell } from "./shell";

import "./app.css";
import {
  ColorSchemeScript,
  MantineProvider,
  mantineHtmlProps,
  Loader,
  Center,
} from "@mantine/core";
import { ModalsProvider } from "@mantine/modals";

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
        <MantineProvider defaultColorScheme="auto">
          <ModalsProvider>
            <Shell>{children}</Shell>
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

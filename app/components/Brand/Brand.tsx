import { Title } from "@mantine/core";
import classes from "./Brand.module.css";

export function Brand() {
  return (
    <a className={classes.link} href="/">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        viewBox="0 16.875 100 67.5"
        className={classes.logo}
      >
        <path
          fill="currentColor"
          d="m92.133 48.926c-0.13281-0.49219-0.49219-0.88281-0.96875-1.0586-10.969-4.043-48.195-10.344-48.195-10.344-0.28516-0.046876-0.57422-0.015626-0.83984 0.089843l-36.461 14.582c-0.75391 0.30469-1.1484 1.1328-0.91406 1.9141 0.24219 0.77344 1.0352 1.2422 1.8281 1.0664 0 0 30.336-6.7344 35.953-6.1172 5.6641 0.62109 50.789 13.383 50.789 13.383 0.53906 0.15234 1.1211 0.003906 1.5234-0.39062 0.39844-0.39844 0.55859-0.97656 0.41406-1.5195l-3.125-11.605z"
          fill-rule="evenodd"
        />
      </svg>
      <Title lh={1} fw={500} size="var(--mantine-spacing-xl)">
        archedbrows
      </Title>
    </a>
  );
}

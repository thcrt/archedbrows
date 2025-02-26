export type Post = {
  id: number;
  source: string;
  source_url: string;
  title: string;
  author?: string;
  time_created?: string;
  time_added: string;
  text?: string;
  media: Media[];
};

export type Media = {
  id: number;
  filename?: string;
  type?: string;
};

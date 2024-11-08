declare module '#content/server' {
  const serverQueryContent: typeof import('/workspace/frontend/node_modules/@nuxt/content/dist/runtime/legacy/types').serverQueryContent
  const parseContent: typeof import('/workspace/frontend/node_modules/@nuxt/content/dist/runtime/server').parseContent
}
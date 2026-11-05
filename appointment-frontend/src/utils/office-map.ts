const officeMaps = import.meta.glob<string>(
  '../assets/img/officemaps/*.png',
  {
    eager: true,
    query: '?url',
    import: 'default'
  }
)

export function getOfficeMapUrl (filename: string): string {
  const url = officeMaps[`../assets/img/officemaps/${filename}`]

  if (!url) {
    throw new Error(`Office map not found: ${filename}`)
  }

  return url
}

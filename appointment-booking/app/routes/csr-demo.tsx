import { useSyncExternalStore } from 'react'
import { Link } from 'react-router'

function useIsClient() {
  return useSyncExternalStore(
    () => () => {},
    () => true,
    () => false,
  )
}

export default function CsrDemo() {
  const isClient = useIsClient()

  if (!isClient) {
    return (
      <noscript>
        <p>
          JavaScript is disabled. This page is client-side rendered — there is no meaningful content
          in the initial HTML.
        </p>
      </noscript>
    )
  }

  return (
    <>
      <h1>Client-Side Rendered (CSR) Demo</h1>

      <p>
        This content was rendered in the browser by JavaScript. It is not in the server HTML
        response.
      </p>

      <p>
        Compare with the <Link to="/locations">locations page</Link>, which is prerendered at build
        time for SEO. With JavaScript disabled, locations still shows the full office table; this
        page does not.
      </p>

      <ul>
        <li>Victoria — 847 Fort Street</li>
        <li>Vancouver — 1181 Melville Street</li>
        <li>Duncan — 1040 Duncan Street</li>
      </ul>
    </>
  )
}

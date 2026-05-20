import { StrictMode } from 'react'
import { renderToString } from 'react-dom/server'
import App from './App'

export function render(url: string) {
  void url

  const appHtml = renderToString(
    <StrictMode>
      <App />
    </StrictMode>,
  )

  return { appHtml }
}

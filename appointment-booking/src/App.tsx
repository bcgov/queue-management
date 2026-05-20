import { useEffect, useState } from 'react'
import { Layout, Page } from '@/components/common'
import { ApiClient, ApiClientError } from '@/services/api-client.service'
import { getOffices } from '@/services/booking-api.service'
import { loadRuntimeConfig } from '@/services/runtime-config.service'
import type { RuntimeConfig } from '@/models/runtime-config'
import './App.css'

function App() {
  const [config, setConfig] = useState<RuntimeConfig | null>(null)
  const [configError, setConfigError] = useState<string | null>(null)
  const [apiStatus, setApiStatus] = useState('Loading app settings...')

  useEffect(() => {
    async function bootstrap() {
      try {
        const runtimeConfig = await loadRuntimeConfig()
        setConfig(runtimeConfig)
        setConfigError(null)

        const apiClient = new ApiClient(runtimeConfig)
        await getOffices(apiClient)
        setApiStatus('Booking API connection established.')
      } catch (error) {
        if (error instanceof ApiClientError) {
          setApiStatus(`Booking API unavailable: ${error.message}`)
        } else {
          setConfigError('Failed to initialize application settings.')
          setApiStatus('Booking API connection not attempted due to config error.')
        }
      }
    }

    void bootstrap()
  }, [])

  return (
    <Layout>
      <Page title="Appointment Booking">
        <p>Runtime settings and booking API groundwork are active.</p>
        <p>{config ? `API base URL: ${config.apiBaseUrl}` : 'API base URL: loading...'}</p>
        <p>{apiStatus}</p>
        {configError ? <p role="alert">{configError}</p> : null}
      </Page>
    </Layout>
  )
}

export default App

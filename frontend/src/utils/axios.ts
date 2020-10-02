/* eslint-disable indent */

import URLConfig from '../../config'
import axios from 'axios'

const instance = axios.create({
    baseURL: URLConfig.APP_API_URL,
    withCredentials: true,
    headers: {
        Accept: 'application/json'
        // Authorization: `Bearer ${bearer}`
    }
})

export function Axios (context) {
    const bearer = typeof context === 'object' ? context.state.bearer : context

    return instance.interceptors.request.use((config) => {
        config.headers.common.Authorization = `Bearer ${bearer}`
        return config
    })
}

export default instance

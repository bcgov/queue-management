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

    // return (
    //     axios.create({
    //         baseURL: URLConfig.APP_API_URL,
    //         withCredentials: true,
    //         headers: {
    //             Accept: 'application/json',
    //             Authorization: `Bearer ${bearer}`
    //         }
    //     })
    // )
}

// instance.interceptors.request.use((config) => {
//     config.headers.get['Content-Type'] = 'application/json'
//     config.headers.post['Content-Type'] = 'application/json'
//     config.headers.put['Content-Type'] = 'application/json'
//     config.headers.patch['Content-Type'] = 'application/json'
//     config.headers.delete['Content-Type'] = 'application/json'
//     config.headers.common.Authorization = `Bearer ${sessionStorage.getItem(
//         'keycloak_token'
//     )}`
//     return config
// })

// Add a response interceptor
// instance.interceptors.response.use(
//     (response) => {
//         return response
//     },
//     async (error) => {
//         // redirect unathorized request to unathorized page
//         if (error.response.status === 401) {
//             store.dispatch('ProjectInfoModule/resetprogress')
//             await router.push('/unauthorized')
//         }
//         return Promise.reject(error)
//     }
// )

export default instance

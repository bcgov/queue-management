import axios from 'axios'

export function Axios(context) {
  return( 
    axios.create({
      baseURL: process.env.API_URL,
      withCredentials: true,
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${context.state.bearer}`
      }
    })
  )
}
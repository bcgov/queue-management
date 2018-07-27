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

export const invitedCitizen = {
  ticket_number: null,
  service_reqs: [
    {
      start_time: null,
      channel: {
        channel_name: null,
        channel_id: null
      }
    }
  ]
}

export const formData = {
  citizen:'',
  setup:'',
  comments: '',
  channel: '',
  search: '',
  category: '',
  service:'',
  quick: false
}
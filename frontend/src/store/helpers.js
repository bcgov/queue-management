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
    citizen_comments: null,
    ticket_number: null,
    citizen_id: null,
    qt_xn_citizen_ind: null,
    start_time: null,
    priority: null,
    service_reqs: [
      {
        start_time: null,
        service: {
          parrent: {}
        },
        service_id: null,
        sr_id: null,
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
  quick: false,
  priority: 2
}

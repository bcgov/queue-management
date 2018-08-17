/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/



<template>
  <div id="smartboard">
    It is {{ date() }} at {{ now() }}
  </div>
</template>

<script>
import Socket from './Socket'
import axios from 'axios'

export default {
  name: 'Smartboard',
  
  data() {
    return {
      options: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
      data: {
        "office_type": "callbynumber",
        "citizens": [
          {
              "ticket_number": "F18",
              "state": "Invited"
          },
          {
              "ticket_number": "F19",
              "state": "Waiting"
          },
          {
              "ticket_number": "F20",
              "state": "Waiting"
          },
          {
              "ticket_number": "G10",
              "state": "Invited"
          },
          {
              "ticket_number": "G11",
              "state": "Waiting"
          }
        ]
      },
      Axios: axios.create({
        baseURL: process.env.API_URL,
        withCredentials: true,
        headers: {
          'Accept': 'application/json'
        }
      }),
      time: new Date()
    }
  },
  
  methods: {
    date() {
      let d = new Date()
      return d.toLocaleDateString('en-CA', this.options)
    },
    now() {
      return null
    },
    getSomething() {
      this.Axios('/smartboard/').then( resp => {
        this.hello = resp.data.office_type
      })
    }
  }
}
</script>



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
  <b-row align-v="center">
    <b-col cols="6">
      <Dash />
    </b-col>
    <b-col cols="2" />
    <b-col cols="4">
      <ClientInput />
    </b-col>
  </b-row>
</template>

<script>
  import Dash from './dash'
  import ClientInput from './ClientInput'

  export default {
    name: 'Controls',
    components: {
      Dash,
      ClientInput
    }
  }

</script>



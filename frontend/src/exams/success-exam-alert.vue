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
  <div>
    <b-alert
      variant="success"
      dismissible
      v-model="countdown"
      @dismissed="setExamEditSuccess(0)"
       style="h-align: center; font-size:1rem; border-radius: 0px;">
      Success!
    </b-alert>
  </div>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

export default {
  name: 'SuccessExamAlert',

  computed: {
    ...mapState(['editExamSuccessCount']),
    countdown: {
      get() { return this.editExamSuccessCount },
      set(e) {
        this.setEditExamSuccess(e)
      }
    }
  },
  methods: {
    ...mapMutations(['setEditExamSuccess']),
  }
}
</script>

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
      variant="danger"
      dismissible
      v-model="countdown"
      @dismissed="setEditExamFailure(0)"
      style="justify-content: center; font-size: 1rem; border-radius: 0px"
    >
      Something Went Wrong! Please submit feedback and tell us about this issue.
    </b-alert>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Mutation, State } from 'vuex-class'

@Component
export default class FailureExamAlert extends Vue {
  @State('editExamFailureCount') private editExamFailureCount!: any
  @Mutation('setEditExamFailure') public setEditExamFailure: any

  get countdown () {
    return this.editExamFailureCount
  }

  set countdown (e) {
    this.setEditExamFailure(e)
  }
}
</script>

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
  <div v-if="is_ita_designate"
       id="EXAMALERT">
    <b-alert
             variant="primary"
             dismissible
             :show="examDismissCount"
             style="h-align: center; font-size:1rem; border-radius: 0px;"
             @dismissed="onDismissedExam">
      {{ examAlertMessage }}
      <b-button id="showExams"
                variant="primary"
                @click="goShow"
                size="sm">
        Show
      </b-button>
    </b-alert>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapState } from 'vuex'

export default {
  name: 'ExamAlert',
  computed: {
    ...mapGetters([ 'is_ita_designate' ]),
    ...mapState([ 'examAlertMessage',
                  'examDismissCount',
                  'groupExam',
                  'individualExam'])
  },
  methods: {
    ...mapMutations(['examDismissCountDown',
                     'setInventoryFilters']),
    goShow() {
      this.$router.push('/exams')
      if(this.groupExam && this.individualExam){
        this.setInventoryFilters({type:'groupFilter', value:'both'})
        this.setInventoryFilters({type:'requireAttentionFilter', value:'both'})
      }
      else if(this.groupExam && !this.individualExam){
        this.setInventoryFilters({type:'groupFilter', value:'group'})
        this.setInventoryFilters({type:'requireAttentionFilter', value:'both'})
      }
      else if(!this.groupExam && this.individualExam){
        this.setInventoryFilters({type:'groupFilter', value:'individual'})
        this.setInventoryFilters({type:'requireAttentionFilter', value:'both'})
      }
    },
    onDismissedExam() {
      this.examDismissCountDown(999)
    }
  }
}
</script>

<style>
  #showExams {
    position: relative;
    float: right;
    bottom: 6px;
  }
</style>

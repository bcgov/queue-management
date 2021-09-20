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
  <div v-if="is_office_manager || role_code === 'GA'" id="EXAMALERT">
    <b-alert
      variant="primary"
      dismissible
      :show="examDismissCount"
      style="justify-content: center; font-size: 1rem; border-radius: 0px"
      @dismissed="onDismissedExam"
    >
      {{ examAlertMessage }}
      <b-button id="showExams" variant="primary" @click="goShow" size="sm">
        Show
      </b-button>
    </b-alert>
  </div>
</template>

<script lang="ts">

import { Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class ExamAlert extends Vue {
  @State('examDismissCount') private examDismissCount!: any
  @State('examAlertMessage') private examAlertMessage!: any

  @Getter('is_office_manager') private is_office_manager!: any;
  @Getter('role_code') private role_code!: any;

  @Mutation('examDismissCountDown') public examDismissCountDown: any
  @Mutation('setInventoryFilters') public setInventoryFilters: any
  @Mutation('setSelectedExamType') public setSelectedExamType: any
  @Mutation('setSelectedExamTypeFilter') public setSelectedExamTypeFilter: any
  @Mutation('setSelectedQuickAction') public setSelectedQuickAction: any
  @Mutation('setSelectedQuickActionFilter') public setSelectedQuickActionFilter: any

  goShow () {
    this.$router.push('/exams')
    this.setSelectedExamType('all')
    this.setSelectedExamTypeFilter('All')
    this.setSelectedQuickAction('oemai')
    this.setSelectedQuickActionFilter('Office Exam Manager Action Items')
    this.setInventoryFilters({ type: 'groupFilter', value: 'all' })
    this.setInventoryFilters({ type: 'requireOEMAttentionFilter', value: 'both' })
    // }
    // else if(this.groupExam && !this.individualExam && this.groupIndividualExam){
    //   this.setSelectedExamType('group')
    //   this.setSelectedExamTypeFilter('Group')
    //   this.setSelectedQuickAction('oemai')
    //   this.setSelectedQuickActionFilter('Office Exam Manager Exam Items')
    //   this.setInventoryFilters({type:'groupFilter', value:'group'})
    //   this.setInventoryFilters({type:'requireOEMAttentionFilter', value:'both'})
    // }
    // else if(this.groupExam && !this.individualExam && !this.groupIndividualExam){
    //   this.setSelectedExamType('group')
    //   this.setSelectedExamTypeFilter('Group')
    //   this.setSelectedQuickAction('oemai')
    //   this.setSelectedQuickActionFilter('Office Exam Manager Exam Items')
    //   this.setInventoryFilters({type:'groupFilter', value:'group'})
    //   this.setInventoryFilters({type:'requireAttentionFilter', value: 'group'})
    // }
    // else if(this.groupExam && this.individualExam && !this.groupIndividualExam){
    //   this.setSelectedExamType('all')
    //   this.setSelectedExamTypeFilter('All')
    //   this.setSelectedQuickAction('oemai')
    //   this.setSelectedQuickActionFilter('Office Exam Manager Exam Items')
    //   this.setInventoryFilters({type:'groupFilter', value:'all'})
    //   this.setInventoryFilters({type:'requireOEMAttentionFilter', value: 'both'})
    // }
    // else if(!this.groupExam && this.individualExam && this.groupIndividualExam){
    //   this.setSelectedExamType('all')
    //   this.setSelectedExamTypeFilter('All')
    //   this.setSelectedQuickAction('oemai')
    //   this.setSelectedQuickActionFilter('Office Exam Manager Exam Items')
    //   this.setInventoryFilters({type:'groupFilter', value:'all'})
    //   this.setInventoryFilters({type:'requireOEMAttentionFilter', value: 'both'})
    // }
    // else if(!this.groupExam && this.individualExam && !this.groupIndividualExam){
    //   this.setSelectedExamType('individual')
    //   this.setSelectedExamTypeFilter('Individual')
    //   this.setSelectedQuickAction('oemai')
    //   this.setSelectedQuickActionFilter('Office Exam Manager Exam Items')
    //   this.setInventoryFilters({type:'groupFilter', value:'individual'})
    //   this.setInventoryFilters({type:'requireOEMAttentionFilter', value: 'both'})
    // }
    // else if(!this.groupExam && !this.individualExam && this.groupIndividualExam){
    //   this.setSelectedExamType('all')
    //   this.setSelectedExamTypeFilter('ALl')
    //   this.setSelectedQuickAction('oemai')
    //   this.setSelectedQuickActionFilter('Office Exam Manager Exam Items')
    //   this.setInventoryFilters({type:'groupFilter', value:'all'})
    //   this.setInventoryFilters({type:'requireOEMAttentionFilter', value: 'both'})
    // }
  }

  onDismissedExam () {
    this.examDismissCountDown(0)
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

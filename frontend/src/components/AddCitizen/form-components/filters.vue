<template>
  <div>
    <b-form-row no-gutters>
      <b-col :cols="simplified ? 12 : 7">
        <input
          ref="filterref"
          style="height: 38px; font-size: .8rem;"
          class="form-control"
          v-model="search"
          placeholder="Type service here"
          id="simplified_service_input"
          autocomplete="off"
        />
      </b-col>
      <b-col>
        <b-select
          id="add_citizen_catagories_select"
          style="height: 38px; font-size: .8rem;"
          :options="categories_options"
          v-model="category"
          size="sm"
          placeholder="Filter by category"
        />
      </b-col>
    </b-form-row>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Watch } from 'vue-property-decorator'
import { Getter, Mutation, State } from 'vuex-class'

@Component({})
export default class Filters extends Vue {
  @State('addModalSetup') private addModalSetup!: string | undefined
  @State('categories') private categories!: any
  @State('suspendFilter') private suspendFilter!: boolean | undefined
  @State('selectedItem') private selectedItem!: string | undefined

  @Getter('form_data') private formData!: any;
  // eslint-disable-next-line camelcase
  @Getter('categories_options') private categories_options!: any;

  @Mutation('updateAddModalForm') public updateAddModalForm: any
  @Mutation('setDisplayServices') public setDisplayServices: any

  @Watch('categories')
  onCategoriesChange (newVal: any, oldVal: any) {
    if (newVal && newVal.length > 0) {
      if (['/booking', '/exams'].includes(this.$route.path)) {
        const { service_id } = newVal.find((cat: any) => cat.service_name === 'Exams')
        this.updateAddModalForm({ type: 'category', value: service_id })
      }
    }
  }

  get simplified () {
    if (this.$route.path !== '/queue') {
      return true
    }
    return false
  }

  get search () {
    if (this.suspendFilter) {
      return this.selectedItem
    } else if (!this.suspendFilter) {
      return this.formData.search
    }
  }

  get category () { return this.formData.category }
  set category (value) { this.updateAddModalForm({ type: 'category', value }) }

  set search (value) {
    if (this.suspendFilter) {
      this.updateAddModalForm({ type: 'suspendFilter', value: false })
    } else if (!this.suspendFilter) {
      this.updateAddModalForm({ type: 'search', value })
    }
  }

  focus () {
    if (this.$refs && this.$refs.inputref) {
      (this.$refs.inputref as any).focus()
    }
  }

  mounted () {
    this.$root.$on('focusfilter', () => {
      if (this.$refs && this.$refs.filterref) {
        (this.$refs.filterref as any).focus()
      }
      if (this.categories && this.categories.length > 0) {
        if (['/booking', '/exams'].includes(this.$route.path)) {
          this.setDisplayServices('All')
          const { service_id } = this.categories.find((cat: any) => cat.service_name === 'Exams')
          this.updateAddModalForm({ type: 'category', value: service_id })
        }
      }
    })
  }
}

</script>

<style scoped>
.b-col {
  padding: 0px;
  margin: 0px;
}
* {
  border-radius: 0;
}
</style>

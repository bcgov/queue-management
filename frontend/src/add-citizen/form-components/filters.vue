<template>
  <div>
    <b-form-row no-gutters>
      <b-col :cols="simplified ? 12 : 7">
          <input ref="filterref"
                 style="height: 38px; font-size: .8rem;"
                 class="form-control"
                 v-model="search"
                 placeholder="Type service here"
                 id="simplified_service_input"
                 ></input>
      </b-col>
      <b-col>
        <b-select id="add_citizen_catagories_select"
                  style="height: 38px; font-size: .8rem;"
                  :options="categories_options"
                  v-model="category"
                  size="sm"
                  placeholder="Filter by category" />
      </b-col>
    </b-form-row>
  </div>
</template>

<script>
  import { mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: 'Filters',
    mounted() {
      this.$root.$on('focusfilter', () => {
        if (this.$refs && this.$refs.filterref) {
          this.$refs.filterref.focus()
        }
        if (this.categories && this.categories.length > 0) {
          if (['/booking', '/exams'].includes(this.$route.path)) {
            let { service_id } = this.categories .find(cat => cat.service_name === 'Exams')
            this.updateAddModalForm({type: 'category', value: service_id})
          }
        }
      })
    },
    computed: {
      ...mapGetters(['categories_options', 'form_data']),
      ...mapState({
        addModalSetup: 'addModalSetup',
        categories: state => state.categories,
        suspendFilter: state => state.addModalForm.suspendFilter,
        selectedItem: state => state.addModalForm.selectedItem,
      }),
      simplified() {
        if (this.$route.path !== '/queue') {
          return true
        }
        return false
      },
      search: {
        get() {
          if (this.suspendFilter) {
            return this.selectedItem
          } else if (!this.suspendFilter) {
            return this.form_data.search
          }
        },
        set(value) {
          if (this.suspendFilter) {
            this.updateAddModalForm({type: 'suspendFilter', value: false})
          } else if (!this.suspendFilter) {
            this.updateAddModalForm( { type: 'search', value } )
          }
        }
      },
      category: {
        get() { return this.form_data.category },
        set(value) { this.updateAddModalForm({type: 'category', value}) }
      }
    },
    watch: {
      categories(newVal, oldVal) {
        if (newVal && newVal.length > 0) {
          if (['/booking', '/exams'].includes(this.$route.path)) {
            let { service_id } = newVal.find(cat => cat.service_name === 'Exams')
            this.updateAddModalForm({type: 'category', value: service_id})
          }
        }
      }
    },
    methods: {
      ...mapMutations(['updateAddModalForm']),
      focus() {
        if (this.$refs && this.$refs.inputref) {
          this.$refs.inputref.focus()
        }
      }
    }
  }
</script>

<style scoped>
  b-col {
    padding: 0px;
    margin: 0px;
  }
  * {
      border-radius: 0;
  }
</style>

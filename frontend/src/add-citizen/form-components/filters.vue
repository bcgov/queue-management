<template>
  <b-container class="add_citizen_form mt-2">
    <b-form-row no-gutters>
      <b-col>
        <label>Type service here</label>
      </b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
          <input ref="filterref"
                 class="form-control"
                 style="height: 38px; font-size: 15px"
                 v-model="search"
                />
      </b-col>
      <b-col>
          <b-select id="add_citizen_catagories_select"
                    :options="categories_options" 
                    v-model="category"
                    size="sm"
                    placeholder="Filter by category"
                    />
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
  import { mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: 'Filters',

    mounted() {
      this.$root.$on('focusfilter', () => {this.$refs.filterref.focus()})
    },

    computed: {
      ...mapGetters(['categories_options', 'form_data']),
      ...mapState({
                    suspendFilter: state => state.addModalForm.suspendFilter,
                    selectedItem: state => state.addModalForm.selectedItem
      }),

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
          }
          this.updateAddModalForm({type: 'search', value})
        }
      },
      category: {
        get() { return this.form_data.category },
        set(value) {
          this.updateAddModalForm({type: 'category', value})
        }
      }
    },

    methods: {
      ...mapMutations(['updateAddModalForm']),

      focus() {
        this.$refs.inputref.focus()
      }
    }
  }
</script>

<style scoped>
  b-col {
    padding: 0px;
    margin: 0px;
  }
</style>

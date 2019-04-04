<template>
  <div>
    <b-form-row no-gutters>
      <b-col :cols="simplified ? 12 : 7">
          <input ref="filterref"
                 style="height: 38px; font-size: .8rem;"
                 class="form-control"
                 v-model="search"
                 placeholder="Type service here"
                 ></input>
      </b-col>
      <b-col v-if="!simplified">
          <b-select id="add_citizen_catagories_select"
                    style="height: 38px; font-size: .8rem;"
                    :options="categories_options"
                    v-model="category"
                    size="sm"
                    placeholder="Filter by category"></b-select>
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
      })
    },

    computed: {
      ...mapGetters({
        categories_options: 'categories_options',
        form_data: 'form_data',
      }),
      ...mapState({
        addModalSetup: 'addModalSetup',
        suspendFilter: state => state.addModalForm.suspendFilter,
        selectedItem: state => state.addModalForm.selectedItem,
      }),
      simplified() {
        if (this.$route.path !== '/queue') {
          return true
        }
        return false
      },
      simplifiedModal() {
        if (this.simplified && this.addModalSetup !== 'edit_mode') {
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
        set(value) {
          this.updateAddModalForm({type: 'category', value})
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

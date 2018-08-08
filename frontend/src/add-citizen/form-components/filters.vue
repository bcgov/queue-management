<template>
  <b-container class="add_citizen_form mt-2">
    <b-form-row no-gutters>
      <b-col>
        <label>Type service here</label>
      </b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
          <input ref="inputref"
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
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Filters',
    mounted() {
      this.$root.$on('focusinput', () => {this.$refs.inputref.focus()})
    },
    computed: {
      ...mapGetters(['categories_options', 'form_data']),
      search: {
        get() { return this.form_data.search },
        set(value) {
          this.$store.commit('updateAddModalForm',{type: 'search', value})
        }
      },
      category: {
        get() { return this.form_data.category },
        set(value) {
          this.$store.commit('updateAddModalForm',{type: 'category', value})
        }
      }
    },
    methods: {
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
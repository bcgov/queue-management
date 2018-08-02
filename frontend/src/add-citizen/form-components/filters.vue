<template>
  <b-container class="add_citizen_form mt-2">
    <b-form-row no-gutters>
      <b-col>
        <label>Type service here</label>
      </b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
          <b-input id="add_citizen_search_input"
                   v-model="search" 
                   size="sm"
                   placeholder="Filter by name"
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
    }
  }
</script>

<style scoped>
  b-col {
    padding: 0px;
    margin: 0px;
  }
</style>
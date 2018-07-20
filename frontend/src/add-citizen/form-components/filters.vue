<template>
  <div>
  <b-form-row>
    <b-col class="px-0 pb-0 pt-1 m-0">
      <label>Type service here</label>
    </b-col>
  </b-form-row>
  <b-form-row>
    <b-col class="px-0 pb-1 pt-0 m-0">
        <b-input id="add_citizen_search_input"
                 v-model="search" 
                 size="sm"
                 placeholder="Filter by name"
                 />
    </b-col>
    <b-col class="px-0 pb-1 pt-0 m-0">
        <b-select id="add_citizen_catagories_select"
                  :options="categories_options" 
                  v-model="category"
                  size="sm"
                  placeholder="Filter by category"
                  />

    </b-col>
  </b-form-row>
    
  </div>
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
          this.$store.commit('updateModalForm',{type: 'search', value})
        }
      },
      category: {
        get() { return this.form_data.category },
        set(value) {
          this.$store.commit('updateModalForm',{type: 'category', value})
        }
      }
    }
  }
</script>

<style scoped>
</style>
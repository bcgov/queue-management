<template>
  <div id='modal_form_filters'
       style="padding-top:12px"
       >
    <label>Type service here</label>
    <b-form inline class="pb-2">
      <b-input id="add_citizen_search_input"
               v-model="search" 
               size="sm"
               class="w-50 px-1"
               placeholder="Filter by name"
               />
      <b-select id="add_citizen_catagories_select"
                :options="categories_options" 
                v-model="category"
                size="sm"
                class="w-50 px-1"
                placeholder="Filter by category"
                />
    </b-form>
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
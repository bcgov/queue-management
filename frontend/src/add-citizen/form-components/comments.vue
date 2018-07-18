<template>
  <b-form-group label="Comments"
                class="mt-0 mb-0"
                >
    <b-textarea id="add_citizen_comment_textarea"
                v-model="comments"
                :rows="4"
                size="sm"
                placeholder="add comments here..."
                />
  </b-form-group>
</template>

<script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Comments',
    computed: {
      ...mapGetters(['form_data']),
      comments: {
        get() { return this.form_data.comments },
        set(value) {
          this.$store.commit('updateModalForm',{type: 'comments', value})
        }
      }
    }
  }
</script>
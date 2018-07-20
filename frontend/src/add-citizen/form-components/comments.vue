<template>
  <div>
    <b-form-row>
      <b-col class="px-0 pb-0 pt-0 m-0">
        <label>Comments</label>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col class="px-0 pb-0 pt-0 m-0">
        <b-textarea id="add_citizen_comment_textarea"
                    v-model="comments"
                    :rows="4"
                    size="sm"
                    placeholder="add comments here..."
                    />
      </b-col>
    </b-form-row>
  </div>
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
<template>
  <b-container fluid class="add_citizen_form">
    <b-form-row no-gutters>
      <b-col>
        <label>Comments</label>
      </b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
        <b-textarea id="add_citizen_comment_textarea"
                    ref="commentsref"
                    v-model="comments"
                    :rows="4"
                    size="sm"
                    placeholder="add comments here">

        </b-textarea>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
  import { mapGetters } from 'vuex'
  
  export default {
    name: 'Comments',

    mounted() {
      this.$root.$on('focuscomments', () => {this.$refs.commentsref.focus()})
    },

    computed: {
      ...mapGetters(['form_data']),

      comments: {
        get() { return this.form_data.comments },
        set(value) {
          this.$store.commit('updateAddModalForm',{type: 'comments', value})
        }
      }
    }
  }
</script>

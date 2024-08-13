<template>
  <div class="add_citizen_form mt-0">
    <b-alert
      :show="commentsTooLong"
      style="justify-content: center"
      variant="danger"
    >You have entered more than the 1,000 characters allowed for comments.</b-alert>
    <b-form-row no-gutters></b-form-row>
    <b-form-row no-gutters>
      <b-col cols="auto">
        <label class="add_citizen_form_label" for="add_citizen_comment_textarea">Comments:</label>
      </b-col>
      <b-col>
        <b-textarea
          id="add_citizen_comment_textarea"
          ref="commentsref"
          v-model="comments"
          :rows="2"
          size="sm"
          maxlength="1000"
          placeholder="add comments here"
        ></b-textarea>
      </b-col>
    </b-form-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Getter } from 'vuex-class'

@Component({})
export default class Comments extends Vue {
  @Getter('form_data') private formData!: any;
  @Getter('commentsTooLong') private commentsTooLong!: any;

  get comments () { return this.formData.comments }
  set comments (value) {
    this.$store.commit('updateAddModalForm', { type: 'comments', value })
  }

  mounted () {
    this.$root.$on('focuscomments', () => {
      if (this.$refs && this.$refs.commentsref) {
        (this.$refs.commentsref as any).focus()
      }
    })
  }
}

</script>

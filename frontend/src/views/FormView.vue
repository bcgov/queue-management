<template>
    <div>
        <FormViewSubmission
          v-if="form_id && submission_id"
          :formid="form_id"
          :submissionid="submission_id"
        />
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import FormViewSubmission from "camunda-formio-tasklist-vue/src/components/FormViewSubmission.vue";

@Component({
  components: {
    FormViewSubmission
  }
})
export default class FormView extends Vue {
  private form_id: string = "";
  private submission_id: string = "";

  mounted() {
    this.form_id = this.$route.params.form_id;
    this.submission_id = this.$route.params.submission_id;
  }
}
</script>

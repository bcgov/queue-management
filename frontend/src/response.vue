<template>
  <b-modal size="sm"
           :centered="t"
           :hide-footer="t"
           :hide-header="t"
           :ok-disabled="t"
           :cancel-disabled="t"
           :visible="showResponseModal"
           @hidden="hideResponseModal"
           >
    Thank-you for submitting your feedback.  We'll get right on it.

  </b-modal>
</template>

<script>
  import { mapState, mapMutations } from 'vuex'

  export default {
    name: 'Response',

    data() {
      return {
        t: true,
        f: false
      }
    },

    computed: {
      ...mapState(['showResponseModal'])
    },

    methods: {
      ...mapMutations(['hideResponseModal'])
    }
  }
</script>

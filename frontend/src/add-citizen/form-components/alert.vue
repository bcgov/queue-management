<template>
    <b-alert show>
      Please fill in all the required fields
    </b-alert>
</template>

<script>
export default {
  name: 'Alert',
  computed: {
    showAlert() {
      return this.$store.state.addCitizenModal.showAlert
    },
    missingNotice() {
      let items = this.$store.getters.add_citizen_form_ready
      if (Array.isArray(items)) {
        let length = items.length()
          if (length === 2) {
            return `You must specify both a service and a channel before submitting.`
          } else if (length === 1) {
            let item = items.toString()
            return `You have not specified a ${item}.  This information is required to submit`
          }
      }
    }
  }
}
</script>

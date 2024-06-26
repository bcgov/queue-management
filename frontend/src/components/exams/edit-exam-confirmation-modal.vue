<template>
  <div v-if="visible" class="confirmation-modal">
    <div class="modal-content">
      <p>Room booking for the exam will be deleted. Are you sure you want to proceed?</p>
      <div class="button-container">
        <b-btn class="btn-primary" @click="$emit('cancel')">Cancel</b-btn>
        <b-btn class="btn-danger mr-2" @click="$emit('confirm')">Confirm</b-btn>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.confirmation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure it's above the parent component */
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  max-width: 25%;
  text-align: center;
}

.modal-content p {
  margin-bottom: 20px;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* Adjust margin as needed */
}
</style>

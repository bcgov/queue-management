<template>
  <div class="inv-filters-container">
    <b-form>
      <b-form-row>
        <b-col cols="6>
          <b-btn variant="outline-primary" :pressed="expired">Expired</b-btn>
        </b-col>
        <b-col cols="6">
          <b-btn variant="outline-primary" :pressed="written">Written</b-btn>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col cols="6>
          <b-btn variant="outline-primary" :pressed="unreturn">Expired</b-btn>
        </b-col>
        <b-col cols="6">
          <b-btn variant="outline-primary" :pressed="expired">Written</b-btn>
        </b-col>
      </b-form-row>
    </b-form>
  </div>
</template>

<script>
  export default {
    name: "InventoryFilters",
    data() {
      return {
        expired: false,
        written: false,

      }
    }
  }
</script>

<style scoped>

</style>
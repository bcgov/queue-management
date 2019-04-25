<template>
  <b-col class="mb-2">
    <div class="q-info-display-grid-container">
      <div class="q-id-grid-outer">
        <div class="q-id-grid-head" v-if="displayData.title">{{ displayData.title }}</div>
        <template v-for="item, i in displayData.items">
          <div :key="i" class="q-id-grid-col">
            <div :key="i+'label'" class="mr-1">{{ item.key }}</div>
            <div :key="i+'item'">{{ item.value }}</div>
          </div>
        </template>
      </div>
    </div>
  </b-col>
</template>

<script>
  export default {
    name: "DataSummaryTable",
    props: ['displayData']
  }
</script>
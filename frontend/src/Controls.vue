<template>
  <b-row>
    <b-col cols="6">
      <ClientTable />
    </b-col>
    <b-col cols="2" />
    <b-col cols="4">
      <ClientInput />
    </b-col>
  </b-row>
</template>

<script>
  import ClientTable from './ClientTable'
  import ClientInput from './ClientInput'

  export default {
    name: 'controls',
    components: {
      ClientTable,
      ClientInput
    }
  }

</script>



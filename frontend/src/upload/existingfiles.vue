<template>
  <b-container fluid
               class="existing_files"
               style="border: 1px solid dimgrey;
                      margin: 0px;
                      padding-left: 0px;
                      padding-right: 0px;
                      padding-bottom: 5px;"
                      >
    <b-form-row no-gutters class="m-0 existing_files_header">
      <b-col class="m-0 p-0">File Name</b-col>
      <b-col class="m-0 p-0">File Modified</b-col>
      <b-col class="m-0 p-0">File Size</b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
        <div id="innertable"
             style="height: 200px;
                    overflow-y: scroll;
                    margin: 0px;
                    background-color: #fcfcfc">
          <b-table :items="videofiles"
                   :fields="fields"
                   sort-by="name"
                   id="table2"
                   class="existing_files_table">
                   <!--@row-clicked="rowClicked"-->
            <template slot="Name" slot-scope="data">
              <div>
                <span v-bind:title="data.item.name">
                  {{data.item.name}}
                </span>
                <div style="display: none">
                  {{ data.item.service_id==form_data.service ?
                      data.item._rowVariant='active' : data.item._rowVariant='' }}
                </div>
              </div>
            </template>
          </b-table>
        </div>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>

  import { mapState } from 'vuex'

  export default {
    name: 'ExistingFiles',

    computed: {
      ...mapState(['videofiles', 'manifestdata']),
      fields() {
        return [
          { key: 'name', label: 'Name', sortable: false, thClass: 'd-none', tdClass: 'file-td',},
          { key: 'date', label: 'Date', sortable: false, thClass: 'd-none', tdClass: 'file-td',},
          { key: 'size', label: 'Size', sortable: false, thClass: 'd-none', tdClass: 'file-td',}
        ]
      },

    },
  }

</script>

  export default {
    name: 'Upload'
  }

<style scoped>

  .existing_files_table {
    padding: 0px;
  }

  .existing_files {
    padding-bottom: 2px;
  }

  .existing_files_header {
    background-color: rgb(179, 183, 186);
    color: white;
    height: 35px;
    padding-top: 6px;
    padding-left: 0px;
    text-align: center;
    font-size: 17px;
    text-shadow: 0px 0px 2px #a5a5a5;
  }

  .addcit-td {
    cursor: pointer;
  }

</style>

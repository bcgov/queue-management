<template>
  <b-container
    fluid
    class="existing_files"
    style="
      border: 1px solid dimgrey;
      margin: 0px;
      padding-left: 0px;
      padding-right: 0px;
      padding-bottom: 5px;
    "
  >
    <b-table
      :fields="fields"
      :items="videofiles"
      head-variant="light"
      class="m-0 p-0 align-left"
      small
      id="video-files"
      fixed
      bordered
    >

      <!--  This is the file name -->
      <template #cell(name)="row">
        {{ row.item.name }}
      </template>

      <!--  This is the delete button -->
      <template #cell(deleteBut)="row">
        <div>
          <b-button size="sm" @click="clickDelete(row.item.name)" variant="link"
            >Delete
          </b-button>
        </div>
      </template>
    </b-table>
    <div style="font-size: 15px; font-weight: 700">
      Disk Space ->
      <span style="padding-left: 1em"
        >Total: {{ numberWithCommas(diskspace.total) }}Mb,</span
      >
      <span style="padding-left: 1em"
        >Used: {{ numberWithCommas(diskspace.used) }}Mb,</span
      >
      <span style="padding-left: 1em"
        >Free: {{ numberWithCommas(diskspace.freespace) }}Mb</span
      >
    </div>
  </b-container>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class ExistingFiles extends Vue {
  @State('videofiles') private videofiles!: any
  @State('manifestdata') private manifestdata!: any
  @State('diskspace') private diskspace!: any

  @Action('clickDeleteFile') public clickDeleteFile: any

  @Mutation('setMainAlert') public setMainAlert: any

  get fields () {
    return [
      { key: 'name', label: 'Name', thStyle: 'text-align: left' },
      { key: 'date', label: 'Date', thStyle: 'text-align: left' },
      { key: 'size', label: 'Size', thStyle: 'text-align: right', tdClass: 'file-size' },
      { key: 'deleteBut', label: 'Delete file', thStyle: 'text-align: center;', tdClass: 'delete-file' }
    ]
  }

  numberWithCommas (x) {
    if (x) { return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') } else { return '' }
  }

  clickDelete (name) {
    if (this.manifestdata.includes(name)) {
      this.setMainAlert('You may not delete file ' + name + '.  It is used in manifest.json.')
    } else {
      this.clickDeleteFile({ name: name })
    }
  }
}

</script>

<style>
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

table .file-size {
  text-align: right;
}

table .delete-file {
  text-align: center;
}
</style>

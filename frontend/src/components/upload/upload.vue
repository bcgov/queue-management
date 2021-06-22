<template>
  <div>
    <div style="position: relative" class="q-upload-margins">
      <div v-if="this.isUploadingFile">
        <div class="q-loader"></div>
      </div>
      <br />

      <div class="container-fluid">
        <div class="row">
          <b-col col cols="2">
            <label class="btn-primary mr-1" id="myLabel">
              <input
                type="file"
                name="myfile"
                id="myfile"
                ref="myfile"
                accept="video/mp4"
                required
                @change="handleFileUpload($event)"
              /><br />
              <span>Select Digital Video file to upload: </span>
            </label>
          </b-col>
          <b-col col cols="3" style="text-align: left" class="pr-2">
            <span class="file_information">{{ fileName }}</span>
          </b-col>
          <b-col col cols="2">
            <span class="file_information">Optional new filename: </span>
          </b-col>
          <b-col col cols="*" class="file_information">
            <input
              type="text"
              style="width: 100%"
              v-model="newfilename"
              placeholder="Type optional new filename here"
            />
          </b-col>
        </div>
        <hr />
        <div class="row">
          <b-col col cols="5">
            <button class="btn btn-success btn-secondary" @click="uploadFile">
              Upload Video and Manifest Files
            </button>
          </b-col>
          <b-col col cols="*" style="text-align: left" class="pr-2">
            <button
              class="btn btn-success btn-secondary"
              @click="uploadManifest"
            >
              Update Manifest File Only
            </button>
          </b-col>
        </div>
        <hr />
        <div class="row">
          <b-col col cols="5">
            <div class="file_header">Existing Files</div>
            <ExistingFiles />
          </b-col>
          <b-col col cols="*" style="text-align: left" class="pr-2">
            <div class="file_header">Manifest File</div>
            <div>
              <b-textarea
                id="serve_comment_textarea"
                v-model="userdata"
                :rows="15"
                size="sm"
              />
            </div>
          </b-col>
        </div>
        <br /><br />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

import ExistingFiles from './existingfiles.vue'

@Component({
  components: {
    ExistingFiles
  }
})
export default class Upload extends Vue {
  @State('videofiles') private videofiles!: any
  @State('manifestdata') private manifestdata!: any
  @State('isUploadingFile') private isUploadingFile!: any
  @State('diskspace') private diskspace!: any

  @Action('clickUploadFile') public clickUploadFile: any
  @Action('requestVideoFileInfo') public requestVideoFileInfo: any

  @Mutation('setMainAlert') public setMainAlert: any

  private file: any = ''
  private isLoading: boolean = false
  private newfilename: string = ''

  get userdata () {
    return this.manifestdata
  }

  set userdata (value) {
    this.$store.commit('setManifestData', value)
  }

  get filesCount () {
    if (this.file) { return 1 } else { return 0 }
  }

  get fileName () {
    if (this.file) { return this.file.name } else { return 'No file selected' }
  }

  uploadFile () {
    if (this.filesCount === 0) {
      this.setMainAlert('Select a file to upload before pressing Upload File')
    } else {
      const file_size = this.file.size / Math.pow(2, 20)
      const space_left = this.diskspace.freespace
      if (space_left < file_size) {
        this.setMainAlert('File too large (' + file_size.toFixed(1) +
          'Mb) to upload to disk (' + space_left.toFixed(1) + 'Mb free)')
      } else {
        const request = { file: this.file, data: this.userdata, newname: this.newfilename }
        this.isLoading = true
        this.clickUploadFile(request)
      }
    }
  }

  uploadManifest () {
    const request = { data: this.userdata }
    this.isLoading = true
    this.clickUploadFile(request)
  }

  handleFileUpload () {
    this.file = (this.$refs.myfile as any).files[0]
  }

  getCurrentFileinfo () {
    this.requestVideoFileInfo()
  }

  mounted () {
    this.getCurrentFileinfo()
    this.newfilename = ''
  }
}

</script>

  export default {
    name: 'Upload'
  }

<style scoped>
#myfile {
  position: absolute;
  top: -1000px;
}

.top-buffer {
  margin-top: 25px;
}

.q-upload-margins {
  margin-top: -15px;
  margin-left: 15px;
  margin-right: 15px;
  padding: 0px;
  overflow: no-display;
}

#myLabel {
  border-radius: 0.25rem;
  padding: 1px 15px 10px 15px;
  margin: 2px;
  font: 400 13.33px Arial, sans-serif;
}
.file_header {
  font-size: 20px;
  font-weight: 700;
  /* width: 75px; */
  text-align: left;
  line-height: 38px;
}
.file_information {
  font-size: 15px;
  font-weight: 400;
  /* width: 75px; */
  text-align: left;
  line-height: 38px;
}
.file_info_border {
  border-style: solid;
  border-width: 1px;
}

.formatted-text {
  white-space: pre;
}
</style>

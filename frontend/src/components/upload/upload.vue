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
              <span>Select Video file</span>
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
              Upload Video files and Manifest
            </button>
          </b-col>
          <b-col
            v-if="editManifest"
            col
            cols="*"
            style="text-align: left"
            class="pr-2"
          >
            <button
              v-if="editManifest"
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
          <b-col
            col
            cols="*"
            style="text-align: left"
            v-if="editManifest"
            class="pr-2"
          >
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
import mime from 'mime'
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
  @State('user') private user!: any

  @Action('clickUploadFile') public clickUploadFile: any
  @Action('requestVideoFileInfo') public requestVideoFileInfo: any
  @Action('findOfficenumber') public findOfficenumber: any

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

  get userdatabyOffice () {
    var menifestData = JSON.parse(this.manifestdata);
    var finalMenifestdata = {};
    var officeNumber = this.$store.state.user.office.office_number;
    Object.keys(menifestData).forEach((videoId) => {
      const videoInfo = menifestData[videoId];
      if (videoId == officeNumber) {
        finalMenifestdata = {
          videoId,
          videoInfo
        };
      }
    });
    return finalMenifestdata;
  }

  get filesCount () {
    if (this.file) {
      return 1;
    } else {
      return 0;
    }
  }

  get fileName () {
    if (this.file) {
      return this.file.name;
    } else {
      return "No file selected";
    }
  }

  async validateMp4File (file) {
    const buffer = await file.slice(0, 16).arrayBuffer();
    const arr = new Uint8Array(buffer);

    const ftyp = [0x66, 0x74, 0x79, 0x70];

    for (let i = 4; i <= 8; i++) {
      if (arr.slice(i, i + 4).toString() === ftyp.toString()) {
        return true;
      }
    }
    return false;
  }

  async uploadFile () {
    if (this.filesCount === 0) {
      this.setMainAlert("Select a file to upload before pressing Upload File");
    } else {
      const file_size = this.file.size / Math.pow(2, 20);
      const space_left = this.diskspace.freespace;
      if (space_left < file_size) {
        this.setMainAlert(
          "File too large (" +
            file_size.toFixed(1) +
            "Mb) to upload to disk (" +
            space_left.toFixed(1) +
            "Mb free)"
        );
      } else {
        const isValidMp4 = await this.validateMp4File(this.file);
        if (!isValidMp4) {
          this.setMainAlert("Invalid file type. Only MP4 videos are allowed.");
          return;
        }
        const request = {
          file: this.file,
          data: this.userdata,
          newname: this.newfilename
        };
        this.isLoading = true;
        this.clickUploadFile(request).then(() => {
          this.newfilename = "";
          this.file = null;
        });
      }
    }
  }

  get editManifest() {
    if (this.user && this.user.role && this.user.role.role_code) {
      if (this.user.role.role_code == "SUPPORT") {
        return true;
      }
    }
    return false;
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

export default { name: 'Upload' }

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

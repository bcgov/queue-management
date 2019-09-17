<template>
  <fragment>
    <div style="position: relative" class="q-upload-margins">

      <br>
      <label class="btn-primary mr-1" id="myLabel">
        <!--<input type="file" name="myfile" id="myfile" accept="video/mp4" required><br>-->
        <input type="file" name="myfile" id="myfile" ref="myfile" accept="video/mp4" required multiple
               @change="handleFileUpload($event)"><br>
        <span>Select Digital Video file to upload: </span>
      </label>
      <span class="file_information">{{fileName}}</span>
      <br><br>
      <button class="btn btn-success btn-secondary" @click="uploadFile">Upload File</button>
      <br>
      <div v-if="this.isUploadingFile">
        <div class="q-loader" />
      </div>

      <br>
      <div class="container-fluid">
        <div class="row">
          <b-col col cols="5" >
            <div class="file_header">Existing Files</div>
            <ExistingFiles />
          </b-col>
          <b-col col cols="*" style="text-align: left" class="pr-2">
            <div class="file_header">Manifest File</div>
            <div>
              <b-textarea id="serve_comment_textarea"
                          v-model="userdata"
                          :rows="15"
                          size="sm" />
            </div>
          </b-col>
        </div>
        <br><br>
      </div>
    </div>
  </fragment>
</template>

<script>

  import { mapActions, mapMutations, mapState } from 'vuex'
  import ExistingFiles from './existingfiles'

  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  export default {
    name: 'Upload',
    components: {ExistingFiles},
    data() {
      return {
        file: '',
        isLoading: false
      }
    },
    mounted() {
      this.getCurrentFileinfo();
    },

    computed: {
      ...mapState(['videofiles', 'manifestdata', 'isUploadingFile']),
      userdata: {
        get() {
          return this.manifestdata;
        },
        set(value) {
          this.$store.commit('setManifestData', value)
        }
      },
      filesCount() {
        if (this.file) { return 1; }
        else { return 0; }
      },
      fileName() {
        if (this.file) { return this.file.name; }
        else { return "No file selected"; }
      }
    },
    methods: {
      ...mapActions(['clickUploadFile', 'requestVideoFileInfo']),
      ...mapMutations(['setMainAlert']),
      uploadFile() {

        if (this.filesCount == 0) {
          this.setMainAlert('Select a file to upload before pressing Upload File')
        }
        else {
          let request = { "file" : this.file, "data" : this.userdata}
          this.isLoading = true;
          this.clickUploadFile(request);
        }
      },
      handleFileUpload() {
        this.file = this.$refs.myfile.files[0];
      },
      getCurrentFileinfo() {
        this.requestVideoFileInfo();
      }
    },
  }

</script>

  export default {
    name: 'Upload'
  }

<style scoped>

  #myfile {
    position:absolute;
    top: -1000px;
  }

  .q-upload-margins {
    margin-top: -15px;
    margin-left: 15px;
    margin-right: 15px;
    padding: 0px;
    overflow: no-display;
  }

  #myLabel {
    border-radius: .25rem;
    padding: 1px 15px 10px 15px;
    margin: 2px;
    font: 400 13.33px Arial;
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

/*
  #myLabel:hover {
    background: #CCC;
  }
  #myLabel:active {
    background: #CCF;
  }
  #myLabel :invalid + span {
    color: #A44;
  }
  #myLabel :valid + span {
    color: #4A4;
  }
*/
</style>

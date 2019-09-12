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
      <br>
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-3">
            <div class="file_header">Existing Files</div>
            <ExistingFiles />
          </div>
          <div class="col-md-3">
            <div class="file_header">Manifest File</div>
            <div class="file_info_border formatted-text">
              {{manifestdata}}
            </div>
          </div>
          <div class="col-md-3">
            <div class="file_header">Manifest File</div>
            <div class="file_info_border">
              {{manifestdata}}
            </div>
          </div>
        </div>
        <br><br>
      </div>
    </div>
  </fragment>
</template>

<script>

  import { mapActions, mapState } from 'vuex'
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
        testmessage: 'Nothing set yet'
      }
    },
    mounted() {
      this.getCurrentFileinfo();
    },

    computed: {
      ...mapState(['videofiles', 'manifestdata']),
      filesCount() {
        if (this.file) { return 1; }
        else { return 0; }
      },
      fileName() {
        if (this.file) { return this.file.name; }
        else { return "No file selected"; }
      },
      lastModified() {
        if (this.file) { return this.file.lastModifiedDate; }
        else { return ""; }
      },
      fileSize() {
        if (this.file) { return numberWithCommas(this.file.size); }
        else { return ""; }
      },
      fileType() {
        if (this.file) { return this.file.type; }
        else { return ""; }
      }
    },
    methods: {
      ...mapActions(['clickUploadFile', 'requestVideoFileInfo']),
      uploadFile() {

        if (this.filesCount == 0) {
          alert("No files to send.  Select something.")
        }
        else {
          this.clickUploadFile(this.file);
        }
      },
      handleFileUpload() {
        this.file = this.$refs.myfile.files[0];
        console.log(this.$refs.myfile.files[0]);
      },
      getCurrentFileinfo() {
        this.requestVideoFileInfo();
        var videoPath = '/static/videos/sbc.mp4'

        this.testmessage = "Function called."
      }

  // var videoPath = '/static/videos/sbc.mp4';
  //     /var/www/html/static/videos


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

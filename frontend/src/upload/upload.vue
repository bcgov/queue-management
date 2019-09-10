<template>
  <div style="position: relative">

    <br>
    <label class="btn-primary mr-1" id="myLabel">
      <!--<input type="file" name="myfile" id="myfile" accept="video/mp4" required><br>-->
      <input type="file" name="myfile" id="myfile" ref="myfile" accept="video/mp4" required multiple
             @change="handleFileUpload($event)"><br>
      <span>Select Digital Video file to upload: </span>
    </label>
    {{fileName}}
    <br>
    <button @click="uploadFile">Upload File</button>
    <br>
    <br>
    <br>
    Some Info:
    <br>
    File count: {{filesCount}}
    <br>
    File name:  {{fileName}}
    <br>
    Last Modified:  {{lastModified}}
    <br>
    File size (bytes):  {{fileSize}}
    <br>
    File type:  {{fileType}}

  </div>
</template>

<script>

  import { mapActions } from 'vuex'

  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  export default {
    name: 'Upload',
    data() {
      return {
        file: ''
      }
    },
    computed: {
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
      ...mapActions(['clickUploadFile']),
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

/*
  #myLabel {
    border: 2px solid #AAA;
    border-radius: 4px;
    padding: 2px 5px;
    margin: 2px;
    background: #DDD;
    display: inline-block;
  }
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

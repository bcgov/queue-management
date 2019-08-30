<template>
  <div style="position: relative">

    <br>
    <label class="btn-primary mr-1" id="myLabel">
      <!--<input type="file" name="myfile" id="myfile" accept="video/mp4" required><br>-->
      <input type="file" name="myfile" id="myfile" ref="myfile" accept="video/mp4" required
             @change="handleFileUpload($event)"><br>
      <span>Select Digital Video file to upload: </span>
    </label>
    {{fileName}}
    <br>
    <button @click="clickSend">Send</button>
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

  import axios from 'axios'
  // import express from 'express'

  const Axios = axios.create({
    baseURL: process.env.API_URL,
    withCredentials: true,
    headers: {
      'Accept': 'application/json'
    }
  });

  // var express = require('express');
  // let app = express();

  // app.post('/upload', (req, res) => {
  //   console.log("==> In the receive post part of the code")
  // }

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
      clickSend() {

        if (this.filesCount == 0) {
          alert("No files to send.  Select something.")
        }
        else {
          // alert("Trying to send files");
          let formData = new FormData();
          formData.append("file", this.file);
          var contenttype = {
            headers: {
              "content-type" : "multipart/form-data"
            }
          };

          // Post the data to the back end.
          axios.post("http://localhost:5000/api/v1/upload/", formData, contenttype)
            .then(function() {
              console.log("Success!");
            })
            .catch(function() {
              console.log("Failure");
            });

          // Post the data to the front end.
          // axios.post("http://localhost:3000/uploadfile", formData, contenttype)
          //   .then(function() {
          //     console.log("Success!");
          //   })
          //   .catch(function() {
          //     console.log("Failure");
          //   });

          // // Get the data to the front end.
          // axios.get("/uploadfile/", formData, contenttype)
          //   .then(function() {
          //     console.log("Success!");
          //   })
          //   .catch(function() {
          //     console.log("Failure");
          //   });
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

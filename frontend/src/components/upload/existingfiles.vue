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
      :items="singleVideoFile()"
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

      <!--  This is the actions button -->
      <template #cell(actions)="row">
        <div>
          <b-dropdown variant="outline-primary" class="pl-0 ml-0 mr-3" right>
            <span slot="button-content"> Actions</span>
            <b-dropdown-item
              @click="clickAddOffice(row.item.name, null)"
              variant="link"
              >Add Office
            </b-dropdown-item>
            <b-dropdown-item
              v-if="checkAdmin()"
              size="sm"
              @click="clickAddOffice(row.item.name, 'default')"
              variant="link"
              >Set Default Video
            </b-dropdown-item>
            <b-dropdown-divider />
            <b-dropdown-item @click="clickDelete(row.item.name)" variant="link"
              ><span style="color: red">Delete</span>
            </b-dropdown-item>
          </b-dropdown>
        </div>
      </template>
      <template #cell(inuse)="row">
        <div>
          {{ checkVideo(row.item.name) }}
        </div>
      </template>
      <template #cell(offices)="row">
        <div>
          <ul>
            <li v-for="item in videodataperOffice(row.item.name)">
              {{ item.videoId }}
            </li>
          </ul>
        </div>
      </template>
    </b-table>
    <div style="font-size: 15px; font-weight: 700">
      Disk Space
      <span style="padding-left: 1em"
        >Total: {{ numberWithCommas(diskspace.total) }}Mb</span
      >
      <span style="padding-left: 1em"
        >Used: {{ numberWithCommas(diskspace.used) }}Mb</span
      >
      <span style="padding-left: 1em"
        >Free: {{ numberWithCommas(diskspace.freespace) }}Mb</span
      >
    </div>
    <div>
      <b-button size="sm" @click="clickRemoveOffice()" variant="link"
        >Play Default Video</b-button
      >
    </div>
  </b-container>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Mutation, State } from "vuex-class";
import { Component, Vue } from "vue-property-decorator";

@Component({})
export default class ExistingFiles extends Vue {
  @State("videofiles") private videofiles!: any;
  @State("manifestdata") private manifestdata!: any;
  @State("diskspace") private diskspace!: any;

  @Action("clickDeleteFile") public clickDeleteFile: any;
  @Action("clickUploadFile") private clickUploadFile!: ( payload: any ) => Promise<void>;
  @Mutation("setMainAlert") public setMainAlert: any;
  @Mutation("setManifestData") public setManifestData: any;

  get fields() {
    return [
      {
        key: "name",
        label: "Name",
        thStyle: "text-align: center"
      },
      {
        key: "date",
        label: "Date",
        thStyle: "text-align: center"
      },
      {
        key: "size",
        label: "Size",
        thStyle: "text-align: center",
        tdClass: "file-size"
      },
      {
        key: "inuse",
        label: "In use",
        thStyle: "text-align: center"
      },
      {
        key: "offices",
        label: "Offices",
        thStyle: "text-align: center"
      },
      {
        key: "actions",
        label: "Actions",
        thStyle: "text-align: center;",
        tdClass: "actions"
      }
    ];
  }

  checkAdmin() {
    if (
      this.$store.state.user &&
      this.$store.state.user.role &&
      this.$store.state.user.role.role_code
    ) {
      if (this.$store.state.user.role.role_code == "SUPPORT") {
        return true;
      }
    }
    return false;
  }

  numberWithCommas(x) {
    if (x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    } else {
      return "";
    }
  }

  checkVideo(name) {
    if (this.manifestdata.includes(name)) {
      return "Yes";
    }
    return "No";
  }

  videodataperOffice(name) {
    const videoData = JSON.parse(this.manifestdata);
    const finaldata: {
      videoId: string;
    }[] = [];
    Object.keys(videoData).forEach((videoId) => {
      const videoInfo = videoData[videoId];
      if (videoInfo.url === `/static/videos/${name}`) {
        finaldata.push({
          videoId
        });
      }
    });

    return finaldata;
  }

  videoNameFromOffice(office) {
    const filteredFiles = this.videofiles.filter((file) => {
      const videoData = this.videodataperOffice(file.name);
      return videoData.some((data) => data.videoId == office);
    });

    return filteredFiles.map((file) => file.name);
  }

  singleVideoFile() {
    return this.videofiles.filter((file) => {
      const videoData = this.videodataperOffice(file.name);
      const useCheck = this.checkVideo(file.name);
      const officeNumber = this.$store.state.user.office.office_number;
      return (
        videoData.some(
          (data) => data.videoId == officeNumber || data.videoId == "default"
        ) || useCheck == "No"
      );
    });
  }

  clickDelete(name) {
    if (this.manifestdata.includes(name)) {
      this.setMainAlert(
        "You may not delete file " + name + ".  It is used in manifest.json."
      );
    } else {
      this.clickDeleteFile({
        name: name
      });
    }
  }

  async clickAddOffice(name: string, flag: string): Promise<void> {
    try {
      const videoData: any = JSON.parse(this.manifestdata);
      var officeNumber = this.$store.state.user.office.office_number;
      const currentTimestamp = new Date().toISOString();
      if (flag == "default") {
        officeNumber = "default";
        videoData[officeNumber] = {
          url: `/static/videos/${name}`,
          updated: currentTimestamp
        };
      } else {
        videoData[officeNumber] = {
          url: `/static/videos/${name}`,
          updated: currentTimestamp
        };
      }

      const updatedManifestdata = JSON.stringify(videoData, null, 2);

      const payload = {
        data: updatedManifestdata,
        newname: name
      };

      await this.$store.dispatch("clickUploadFile", payload);
      await this.setManifestData(updatedManifestdata);
      this.setMainAlert(
        `Video ${name} added to : ${this.$store.state.user.office.office_name}`
      );
    } catch (error) {
      console.error("Error uploading manifest", error);
    }
  }

  async clickRemoveOffice(): Promise<void> {
    try {
      const videoData: any = JSON.parse(this.manifestdata);
      const officeNumber = this.$store.state.user.office.office_number;
      const currentTimestamp = new Date().toISOString();
      const name = this.videoNameFromOffice("default")[0];
      videoData[officeNumber] = {
        url: `/static/videos/${name}`,
        updated: currentTimestamp
      };

      const updatedManifestdata = JSON.stringify(videoData, null, 2);

      const payload = {
        data: updatedManifestdata,
        newname: name
      };

      await this.$store.dispatch("clickUploadFile", payload);
      await this.setManifestData(updatedManifestdata);
      this.setMainAlert(
        `Current Default Video ${name} added to : ${this.$store.state.user.office.office_name}`
      );
    } catch (error) {
      console.error("Error uploading manifest", error);
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
  text-align: center;
}

table .actions {
  text-align: center;
}
</style>

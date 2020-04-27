<template>
  <!-- Service Model Popup -->
  <v-dialog
    v-model="locationServicesModal"
    max-width="600"
  >
    <v-card>
      <v-toolbar dark flat color="primary">
        <v-toolbar-title>Location Services for {{selectedLocationName}}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon dark @click="locationServicesModal = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <v-row>
          <v-col>
            <v-select
              :items="categoryList"
              label="Categories"
              outlined
              color="primary"
              class="text-left"
              v-model="selectedCategory"
              name="categories-select"
              :item-text="'service_name'"
              :item-value="'service_name'"
              hide-details
              dense
              clearable
              @change="filterUsingCategory"
            >
            </v-select>
          </v-col>
          <v-col>
            <v-text-field
              prepend-inner-icon="mdi-magnify"
              type="text"
              name="search-service"
              label="Search Service"
              outlined
              hide-details
              dense
            ></v-text-field>
          </v-col>
        </v-row>
        <v-simple-table
          fixed-header
          height="300"
        >
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Service</th>
                <th class="text-left">Service Information</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredServiceList" :key="item.service_id">
                <td>{{ item.service_name }}</td>
                <td>
                  <span v-if="!item.online_availability">{{item.service_desc}}</span>
                  <span v-else class="service-unavailable">Unavailable</span>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import { mapState } from 'vuex'

@Component({
  computed: {
    ...mapState('office', [
      'categoryList'
    ])
  }
})
export default class ServiceListPopup extends Vue {
  private selectedCategory:string = ''
  private filteredServiceList: Service[] = []
  private readonly categoryList!: Service[]
  private isFiltered = false

  @Prop({ default: false })
  private locationServicesModal!: boolean

  @Prop({ default: [] })
  private serviceList!: Service[]

  @Prop({ default: '' })
  private selectedLocationName!: string

  private async beforeUpdate () {
    this.filteredServiceList = (!this.isFiltered) ? { ...this.serviceList } : this.filteredServiceList
  }

  private filterUsingCategory () {
    if (this.selectedCategory) {
      this.filteredServiceList = this.serviceList.filter((service) => {
        return (service?.parent?.service_name === this.selectedCategory)
      })
      this.isFiltered = true
    } else {
      this.isFiltered = false
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.service-unavailable {
  color: $BCgovInputError;
  font-weight: 600;
}
</style>

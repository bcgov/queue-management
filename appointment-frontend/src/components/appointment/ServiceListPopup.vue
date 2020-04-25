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
              :items="categoriesList"
              label="Radius"
              outlined
              color="primary"
              class="text-left"
              v-model="selectedCategory"
              name="categories-select"
              hide-details
              dense
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
              <tr v-for="item in serviceList" :key="item.service_id">
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
import { Service } from '@/models/service'

@Component
export default class ServiceListPopup extends Vue {
  private selectedCategory = null
  private categoriesList = ['Category 1', 'Category 2']

  @Prop({ default: false })
  private locationServicesModal!: boolean

  @Prop({ default: [] })
  private serviceList!: Service[]

  @Prop({ default: '' })
  private selectedLocationName!: string
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.service-unavailable {
  color: $BCgovInputError;
  font-weight: 600;
}
</style>

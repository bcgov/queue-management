<template>
  <!-- Service Model Popup -->
  <v-dialog
    v-model="isModelOpen"
    max-width="570"
  >
    <v-card data-cy="step-1-dialog-service-list">
      <v-toolbar dark flat color="primary">
        <v-toolbar-title>Location Services for {{selectedLocationName}}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon dark @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <v-row>
          <v-col>
            <!-- TODO: change snake_case in item-text and item-value, below? Aug3/22 -->
            <v-select
              :items="categoryList"
              label="Categories"
              outlined
              color="primary"
              class="text-left"
              v-model="selectedCategory"
              name="categories-select"
              :item-text="'externalServiceName'"
              :item-value="'serviceName'"
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
              v-model="categorySearchInput"
              clearable
              @input="categorySearch"
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
                <th id="txtservice" class="text-left">Service</th>
                <th id="txtserviceblank"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredServiceList" :key="item.serviceId">
                <td>
                  <div
                    v-bind:class="{'unavailable-service': item.onlineAvailability === ServiceAvailability.DISABLE}"
                  >
                    {{ item.externalServiceName }}
                  </div>
                </td>
                <td>
                  <div v-if="item.onlineLink" class="service-link" @click="goToServiceLink(item.externalServiceName, item.onlineLink)">
                    Online Option <v-icon small>mdi-open-in-new</v-icon>
                  </div>
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
import { mapActions, mapGetters, mapState } from 'vuex'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import { ServiceAvailability } from '@/utils/constants'
import { User } from '@/models/user'

@Component({
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'categoryList'
    ]),
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapActions('office', [
      'callSnowplowClick'
    ])
  }
})
export default class ServiceListPopup extends Vue {
  private selectedCategory:string = ''
  private categorySearchInput:string = ''
  private filteredServiceList: Service[] = []
  private readonly categoryList!: Service[]
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly currentUserProfile!: User
  private readonly isAuthenticated!: boolean
  private isFiltered: boolean = false
  private isModelOpen: boolean = false
  private ServiceAvailability = ServiceAvailability
  private readonly callSnowplowClick!: (mySP: any) => any

  @Prop({ default: false })
  private locationServicesModal!: boolean

  @Prop({ default: [] })
  private serviceList!: Service[]

  @Prop({ default: '' })
  private selectedLocationName!: string

  public open () {
    this.isModelOpen = true
  }

  public close () {
    this.isFiltered = false
    this.selectedCategory = ''
    this.categorySearchInput = ''
    this.isModelOpen = false
  }

  private async beforeUpdate () {
    this.filteredServiceList = (!this.isFiltered) ? { ...this.serviceList } : this.filteredServiceList
  }

  private filterUsingCategory () {
    this.categorySearchInput = ''
    if (this.selectedCategory) {
      this.filteredServiceList = this.serviceList.filter((service) => {
        return (service?.parent?.serviceName === this.selectedCategory)
      })
      this.isFiltered = true
    } else {
      this.isFiltered = false
    }
  }

  private categorySearch (value: string) {
    this.selectedCategory = ''
    if (value) {
      this.filteredServiceList = this.serviceList.filter((service) => {
        return `${service?.externalServiceName || ''} ${service?.serviceDesc || ''}`.toLowerCase().includes(value.toLowerCase())
      })
      this.isFiltered = true
    } else {
      this.isFiltered = false
    }
  }

  private goToServiceLink (sn, url) {
    const mySP = { label: 'Online Option', step: 'Location Selection', loggedIn: this.isAuthenticated, apptID: null, clientID: this.currentUserProfile?.userId, loc: this.selectedLocationName, serv: sn, url: url }
    this.callSnowplowClick(mySP)
    window.open(url, '_blank')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.service-unavailable {
  color: $BCgovInputError;
  font-weight: 600;
}
.unavailable-service {
  color: $gray6;
}
.service-link {
  font-weight: 600;
  font-size: .85rem;
  color: $BCgovBlue8;
  cursor: pointer;
  text-align: end;
}
</style>

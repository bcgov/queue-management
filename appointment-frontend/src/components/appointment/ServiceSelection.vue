<template>
  <v-card>
    <v-card-title class="justify-center">
      <h3>Service Selection</h3>
    </v-card-title>
    <v-divider class="mx-4"></v-divider>
    <v-card-text>
      <p class="subtitle-1 text-center">Please select the service you'd like to receive</p>
      <v-row justify="center">
        <v-col cols="12" sm="6">
          <v-select
            :items="serviceList"
            :item-disabled="'isUnavailable'"
            label="Select Service"
            outlined
            color="primary"
            class="text-left"
            v-model="selectedService"
            name="service-select"
            @change="changed"
          >
            <template v-slot:selection="data">
              {{ data.item.serviceName }}
            </template>
            <template v-slot:item="data">
              <div class="d-flex align-center">
                <div>{{ data.item.serviceName }}</div>
                <div class="align-self-end service-message">{{ data.item.message }}</div>
              </div>
            </template>
          </v-select>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="12" sm="6">
          <v-textarea
            outlined
            name="additional-options"
            label="Is there any additional info you'd like to add? (Optional)"
            v-model="additionalOptions"
        ></v-textarea>
        </v-col>
      </v-row>
      <template v-if="selectedService">
        <p class="text-center mb-6">Do you want to book an appointment with a Service BC Center for the selected service?</p>
        <div class="d-flex justify-center mb-6">
          <v-btn large outlined color="primary" class="mr-3">No, Book With Another Option</v-btn>
          <v-btn large color="primary">Yes, Book With The Service BC Centre</v-btn>
        </div>
      </template>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class ServiceSelection extends Vue {
  @Prop({ default: '' })
  private name!: string

  @Prop({ default: '' })
  private message!: string

  private selectedService = null
  private additionalOptions = ''

  private serviceList = [
    {
      id: 1,
      serviceName: 'BC Online Searches',
      isUnavailable: true,
      message: 'Unavailable due to COVID-19'
    },
    {
      id: 2,
      serviceName: 'Manufactured Homes',
      isUnavailable: false,
      message: ''
    },
    {
      id: 3,
      serviceName: 'Roadtest Booking Online',
      isUnavailable: false,
      message: 'Online Options Available'
    },
    {
      id: 3,
      serviceName: 'Notary',
      isUnavailable: false,
      message: ''
    }
  ]

  private mounted () {
    // eslint-disable-next-line no-console
    console.log(this.selectedService)
  }

  private changed (value) {
    // eslint-disable-next-line no-console
    console.log(value)
  }
}
</script>

<style lang="scss" scoped>
.service-message {
  font-size: 10px;
  margin-left: 12px;
  font-style: italic;
  margin-bottom: 1px;
}
</style>

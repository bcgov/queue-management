<template>
  <v-card>
    <v-divider class="mx-4"></v-divider>
    <v-card-text>
      <p class="subtitle-1 text-center">To book an appointment, please find your nearest BC Service Location</p>
      <v-row justify="center">
        <v-col cols="6" sm="4">
          <v-text-field
            append-icon="mdi-map-marker-radius"
            type="text"
            name="postal-code"
            label="Postal Code"
            outlined
            hide-details
            @click:append="fetchLocation"
          ></v-text-field>
        </v-col>
        <v-col cols="6" sm="4" offset-sm="1">
          <v-select
            :items="radiusList"
            label="Radius"
            outlined
            color="primary"
            class="text-left"
            v-model="selectedRadius"
            name="radius-select"
            hide-details
          >
            <template v-slot:selection="data">
              {{ data.item }} Km
            </template>
          </v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <p class="text-center">Locations sorted by nearest to you</p>
        </v-col>

      </v-row>
      <template>
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

  private selectedRadius = null

  private radiusList = [2, 4, 6, 10]

  private mounted () {
    // eslint-disable-next-line no-console
    console.log(this.selectedRadius)
  }

  private fetchLocation () {
    // eslint-disable-next-line no-console
    console.log('fetchLocation')
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

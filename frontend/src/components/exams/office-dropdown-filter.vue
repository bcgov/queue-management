<template>
  <b-form inline class="mt-otto">
    <b-row no-gutters class="mt-otto">
      <b-col class="dropdown mt-otto">
        <div style="height: 100%" class="mt-otto">
          <b-input
            :value="search"
            @input="handleInput"
            class="ml-3 w-100 mt-otto"
            size="sm"
          />
          <div :class="menuClass" boundary="viewport">
            <template v-for="office in officeList">
              <b-dd-item
                @click="handleClick"
                v-if="officeList.length > 0"
                :name="office.office_name"
                :id="office.office_id"
                :key="office.office_id"
                >{{ office.office_name }}</b-dd-item
              >
              <!-- JSTOTS added key -->
              <b-dd-item v-if="officeList.length === 0" :key="office.office_id"
                >No matching offices</b-dd-item
              >
            </template>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-form>
</template>

<script lang="ts">

import { Action, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class OfficeDropDownFilter extends Vue {
  @State('offices') private offices!: any
  @State('selectedOffice') private selectedOffice!: any

  @Action('getOffices') public getOffices: any

  @Mutation('setSelectedOffice') public setSelectedOffice: any

  public clicked: any = false
  public menuClass: any = 'dropdown-menu'
  public search: any = ''
  public searching: any = false

  get officeList () {
    if (this.searching === true) {
      if (this.offices && this.offices.length > 0) {
        if (this.search) {
          return this.offices.filter(o => o.office_name.toLowerCase().includes(this.search.toLowerCase()))
        }
      }
    }
    return []
  }

  handleInput (e) {
    if (this.searching === false) {
      this.search = ''
      this.searching = true
    }
    this.search = e
    if (this.search.length > 1 && this.searching === true) {
      this.menuClass = 'dropdown-menu show py-0 my-0 w-100'
      this.setSelectedOffice(this.search)
    }
    if (this.search.length <= 1) {
      this.searching = false
      this.menuClass = 'dropdown-menu'
    }
  }

  handleClick (e) {
    this.search = e.target.innerText
    this.searching = false
    this.menuClass = 'dropdown-menu'
  }

  created () {
    this.getOffices()
  }
}
</script>

<style scoped>
.mt-otto {
  margin-top: auto;
}
</style>

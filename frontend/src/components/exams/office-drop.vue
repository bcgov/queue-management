<template>
  <b-row>
    <b-col :cols="columnW">
      <b-form autocomplete="off">
        <b-form-group>
          <label for="office_name" class="my-0"
            >Office
            <span v-if="!error"> {{ msg }} </span>
            <span v-if="error" style="color: red"> {{ msg }} </span>
          </label>
          <div>
            <b-form-input
              id="office_name"
              type="text"
              autocomplete="off"
              class="less-10-mb"
              :value="officeSearch"
              @focus.native="officeSearchOnFocus"
              @blur.native="officeSearchOnBlur"
              @input.native="handleOfficeInput"
            />
          </div>
          <div :class="officeDropClass" style="border: 1px solid grey">
            <template v-for="office in officeChoices">
              <b-dropdown-item-button
                v-on:click.prevent="handleOfficeDropClick"
                :name="office.office_name"
                :value="office.office_number"
                :id="office.office_number"
                :key="office.office_number"
                >{{ office.office_name }}</b-dropdown-item-button
              >
            </template>
          </div>
        </b-form-group>
      </b-form>
    </b-col>
    <b-col :cols="columnW == 8 ? 4 : 2">
      <b-form>
        <b-form-group>
          <label for="office_number" class="my-0">Office #</label>
          <b-form-input
            id="office_number"
            type="text"
            class="less-10-mb"
            :value="numberSearch"
            @focus.native="handleOfficeNumberFocus"
            @blur.native="handleOfficeNumberBlur"
            @input.native="handleOfficeNumberInput"
          />
        </b-form-group>
      </b-form>
    </b-col>
  </b-row>
</template>

<script lang="ts">
/* eslint-disable camelcase */
import { Action, Getter, State } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class OfficeDrop extends Vue {
  @Prop()
  private columnW!: any

  @Prop()
  private office_number!: any

  @Prop()
  private setOffice!: any

  @Prop()
  private msg!: any

  @Prop()
  private error!: any

  @State('offices') private offices!: any
  @State('capturedExam') private capturedExam!: any

  @Getter('role_code') private role_code!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;
  @Getter('is_ita2_designate') private is_ita2_designate!: any;

  @Action('getOffices') public getOffices: any

  public clickedMenu: any = false
  public message: any = ''
  public officeChoices: any = []
  public showMessage: any = false
  public showSearch: any = false
  public searching: any = false
  public search: any = ''
  public searchingNumber: any = false
  public searchNumber: any = ''
  public timer: any = null

  get office_id () {
    if (this.capturedExam && this.capturedExam.office_id) {
      return this.capturedExam.office_id
    }
  }

  get officeDropClass () {
    if (!this.showSearch) {
      return 'dropdown-menu'
    }
    if (this.showSearch) {
      return 'dropdown-menu show py-0 my-0 w-100'
    }
  }

  get numberSearch () {
    if (!this.searchingNumber) {
      return this.office_number
    }
  }

  get officeSearch () {
    if (!this.searching && this.office_number && this.offices.length > 0) {
      // eslint-disable-next-line eqeqeq
      return this.offices.find(office => office.office_number == this.office_number).office_name
    }
    return this.search
  }

  handleOfficeDropClick (e) {
    this.showSearch = false
    this.search = e.target.name
    this.setOffice(e.target.value)
    this.searching = false
  }

  handleOfficeNumberFocus () {
    this.searchingNumber = true
    this.searchNumber = ''
  }

  handleOfficeNumberBlur () {
    this.searchingNumber = false
  }

  handleOfficeInput (e) {
    this.searching = true
    this.search = e.target.value
    if (this.search.length > 1 && this.searching === true) {
      this.showSearch = true

      this.officeChoices = this.offices.filter(item => {
        const office_name = item.office_name === undefined || item.office_name === null ? '' : item.office_name

        if (office_name.toLowerCase().indexOf(this.search.toLowerCase()) > -1) {
          return true
        }
      })

      if (this.officeChoices.length === 0) {
        this.officeChoices = [{ office_number: null, office_name: 'No Offices found' }]
      } else {
        this.officeChoices = this.officeChoices.length >= 4 ? this.officeChoices.slice(0, 4) : this.officeChoices
      }
    }
    this.checkMinSearchLength()
  }

  checkMinSearchLength () {
    if (this.search.length <= 1) {
      this.showSearch = false
    }
  }

  handleOfficeNumberInput (e) {
    this.searchingNumber = true
    this.searchNumber = e.target.value
    // eslint-disable-next-line eqeqeq
    if (this.offices.find(office => office.office_number == e.target.value)) {
      this.setOffice(e.target.value)
      this.searchingNumber = false
    }
  }

  officeSearchOnBlur () {
    this.searching = false
  }

  officeSearchOnFocus () {
    this.searching = true
    this.search = ''
  }
}
</script>

<style scoped>
.less-10-mb {
  margin-bottom: -10px !important;
}
</style>

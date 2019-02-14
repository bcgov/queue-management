<template>
  <div v-if="role_code === 'LIAISON'">
    <b-table v-show="false"
             :items="offices"
             :fields="{key: 'office_name'}"
             :filter="search"
             @filtered="getFilteredOffices" />
    <b-form>
      <b-form-row>
        <b-col>
          <b-form-group>
            <label class="my-0">Office (Start typing below to search or enter Office Number )</label>
            <div><b-form-input id="office_name"
                               type="text"
                               class="less-10-mb"
                               :value="officeSearch"
                               @focus.native="officeSearchOnFocus"
                               @blur.native="officeSearchOnBlur"
                               @input.native="handleOfficeInput" /></div>
            <div :class="officeDropClass" style="border: 1px solid grey">
              <template v-for="office in officeChoices">
                <b-dropdown-item-button v-on:click.prevent="handleOfficeDropClick"
                                        :name="office.office_name"
                                        :value="office.office_number"
                                        :id="office.office_id">{{ office.office_name }}
                </b-dropdown-item-button>
              </template>
            </div>
          </b-form-group>
        </b-col>
      </b-form-row>
    </b-form>
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: "OfficeDrop",
    data () {
      return {
        clickedMenu: false,
        office_number: null,
        office_id: null,
        officeChoices: [],
        showMessage: false,
        showSearch: false,
        searching: false,
        search: '',
      }
    },
    computed: {
      ...mapGetters(['role_code']),
      ...mapState(['offices', 'officeDropDown',]),
      officeDropClass() {
        if (!this.showSearch) {
          return 'dropdown-menu'
        }
        if (this.showSearch) {
          return 'dropdown-menu show py-0 my-0 w-100'
        }
      },
      officeSearch() {
        if (!this.searching && this.officeDropDown) {
          return this.offices.find(office=>office.office_number == this.office_number).office_name
        }
        return this.search
      },
    },
    methods: {
      ...mapActions(['getOffices',]),
      ...mapMutations(['setOfficeDropDown']),
      getFilteredOffices(offices) {
        if (offices.length === 0) {
          this.officeChoices = [{office_id: null, office_name: 'No offices found with those letters'}]
          return
        }
        this.officeChoices = offices.length >= 4 ? offices.slice(0,4) : offices
      },
      handleOfficeDropClick(e) {
        this.showSearch = false
        this.office_id = e.target.id
        this.search = e.target.name
        this.office_number = e.target.value
        this.searching = false
      },
      handleOfficeInput(e) {
        this.searching = true
        this.search = e.target.value
        if (this.search.length > 1 && this.searching === true) {
          this.showSearch = true
        }
        if (this.search.length <= 1) {
          this.showSearch = false
        }
      },
      handleOfficeNumberInput(e) {
        let { value } = e.target
        if (value.length <= 2) {
          this.office_number = value
        } else {
          this.office_number = value.slice(value.length-2, value.length)
        }
        if (this.offices.find(office=>office.office_number == this.office_number)) {
          let office = this.offices.find(office=>office.office_number == this.office_number)
          this.search = office.office_name
          this.office_id = office.office_id
        } else {
          this.search = 'Invalid office number entered.'
          this.office_id = null
        }
      },
      officeSearchOnBlur() {
        this.searching = false
      },
      officeSearchOnFocus() {
        this.searching = true
        this.search = ''
      },
    },
  }
</script>

<style scoped>
  .less-10-mb {
    margin-bottom: -10px !important;
  }
  .less-15-mb {
    margin-bottom: -15px !important;
  }
  .id-grid-1st-col {
    margin-left: auto;
    margin-right: 20px;
  }
  .id-grid-1st-col {
    grid-column: 1 / span 2;
    margin-right: 20px;
  }
</style>
<template>
  <fragment>
    <b-col :cols="columnW">
      <b-table v-show="false"
               v-if="role_code==='LIAISON'"
               :items="offices"
               :fields="{key: 'office_name'}"
               :filter="search"
               @filtered="getFilteredOffices" />
      <b-form-group>
        <label class="my-0">Office
          <span v-if="!error"> {{ msg }} </span>
          <span v-if="error" style="color: red"> {{ msg }} </span>
        </label>
        <div>
          <b-form-input id="office_name"
                        type="text"
                        class="less-10-mb"
                        :value="officeSearch"
                        @focus.native="officeSearchOnFocus"
                        @blur.native="officeSearchOnBlur"
                        @input.native="handleOfficeInput" />
        </div>
        <div :class="officeDropClass"
             style="border: 1px solid grey">
          <template v-for="office in officeChoices">
            <b-dropdown-item-button v-on:click.prevent="handleOfficeDropClick"
                                    :name="office.office_name"
                                    :value="office.office_number"
                                    :id="office.office_number">{{ office.office_name }}</b-dropdown-item-button>
          </template>
        </div>
      </b-form-group>
    </b-col>
    <b-col :cols="columnW == 8 ? 4 : 2">
      <b-form-group>
        <label class="my-0">Office #</label>
        <b-form-input id="office_number"
                      type="number"
                      class="less-10-mb"
                      :value="office_number"
                      @input.native="handleOfficeNumberInput" />
      </b-form-group>
    </b-col>
  </fragment>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: "OfficeDrop",
    props: ['columnW', 'office_number', 'setOffice', 'msg', 'error'],
    data () {
      return {
        clickedMenu: false,
        message: '',
        officeChoices: [],
        showMessage: false,
        showSearch: false,
        searching: false,
        search: '',
      }
    },
    computed: {
      ...mapGetters([ 'role_code' ]),
      ...mapState([ 'offices', 'capturedExam' ]),
      office_id() {
        if (this.capturedExam && this.capturedExam.office_id) {
          return this.capturedExam.office_id
        }
      },
      officeDropClass() {
        if (!this.showSearch) {
          return 'dropdown-menu'
        }
        if (this.showSearch) {
          return 'dropdown-menu show py-0 my-0 w-100'
        }
      },
      officeSearch() {
        let office_number = this.office_number
        if (!this.searching && office_number && this.offices.find(office=>office.office_number == office_number)) {
          return this.offices.find(office => office.office_number == this.office_number).office_name
        }
        return this.search
      },
    },
    methods: {
      ...mapActions(['getOffices',]),
      ...mapMutations([]),
      getFilteredOffices(offices) {
        if (offices.length === 0) {
          this.officeChoices = [{office_number: null, office_name: 'No offices found with those letters'}]
          return
        }
        this.officeChoices = offices.length >= 4 ? offices.slice(0,4) : offices
      },
      handleOfficeDropClick(e) {
        this.showSearch = false
        this.search = e.target.name
        this.setOffice(e.target.value)
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
        this.setOffice(value)
        if (this.offices.find(office=>office.office_number == value)) {
          let office = this.offices.find(office=>office.office_number == value)
          this.search = office.office_name
        } else {
          this.search = 'Invalid office number entered.'
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
</style>

/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/



<template>
<div id="header">
  <b-navbar variant="faded"
            type="light"
            style="box-shadow: 0px 5px 10px 0px rgba(169,169,169,1); padding: 5px 0px 0px 0px; background-color: #003366; border-bottom: 2px solid #fcba19;">
    <b-navbar-brand style="padding-left: 30px; padding-top: 0px; margin-bottom:5px;">
      <a href="#">
        <img style="height:95%; width: 95%" src="https://www2.gov.bc.ca/assets/gov/home/bc_gov_logo_transparent.png" alt="Government of B.C." title="Government of B.C.">
      </a>
    </b-navbar-brand>
    <b-navbar-brand style="padding-left: 30px; padding-top: 0px;">
      <Login />
    </b-navbar-brand>
  </b-navbar>
</div>
</template>

<script>
import Login from './../Login'

export default {
  name: 'Header',
  components: { Login }
}
</script>

<style>
  .modal-main div {
    background-color: blue;
  }
</style>

<template>
<div class="flex h-screen flex-col  justify-center font-bold overflow-hidden">
<AppHeader />
  <div class="flex h-screen flex-col items-center justify-center font-bold border-t border-b ">
    <span class="bg-bcdsBlue-10 text-primaryBlue text-xl">Service BC Queue Management System</span>
    <span class="bg-bcdsGold-10 text-primaryGold text-lg">Under Construction</span>

    <div class="p-sm m-huge rounded-md bg-surface-danger text-danger border-danger border shadow-xs">
      This is a test
    </div>
      <div>
        <button @click="toggleDropdown"> </button>
        <Dropdown :items="dropdownItems" :showDropdown="isDropdownOpen" />
      </div>
  </div>
  
   <div></div>
     <AppFooter />
     </div>

</template>
<script setup>
import { ref } from 'vue';
import Dropdown from '@/components/dropdown.vue';
import AppFooter from '@/components/app_footer/index.vue';
import AppHeader from '@/components/app_header/index.vue';

definePageMeta({
  layout: 'default' 
});
const dropdownItems = ref([
  { text: 'The Q', to: '/queue' },
  { text: 'Room Booking', to: '/booking', condition: true },
  { text: 'Appointments', to: '/appointments', condition: true },
  { text: 'Exam Inventory', to: '/exams', condition: true },
  { text: 'Office Agenda', to: '/agenda', condition: false },
  { text: 'Service Flow', to: '/service-flow', condition: true },
  {
    text: 'Show GA Panel',
    action: () => {
      console.log('GA Panel clicked');
    },
    icon: 'check'
  },
  { divider: true },
  {
    text: 'Refresh',
    action: () => {
      console.log('Refresh clicked');
    }
  },
  { text: 'Upload File', to: '/upload' },
  { divider: true },
  {
    text: 'Feedback',
    action: () => {
      console.log('Feedback clicked');
    }
  },
  { text: 'Logout', to: '/logout', condition: true },
]);

const isDropdownOpen = ref(false);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};
</script>

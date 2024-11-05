import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { defineNuxtPlugin } from 'nuxt/app';
import { faCheck, faBars } from '@fortawesome/free-solid-svg-icons'; 

library.add(faCheck, faBars); 

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('font-awesome-icon', FontAwesomeIcon);
});

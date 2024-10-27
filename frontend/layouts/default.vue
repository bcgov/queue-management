<!-- layouts/default.vue -->
<template>
  <AppHeader />
  <main>
    <nuxt-page />
  </main>
  <AppFooter />
</template>

<script setup>
import AppFooter from '@/components/app_footer/index.vue';
import AppHeader from '@/components/app_header/index.vue';

</script>

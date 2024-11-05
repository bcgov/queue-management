<template>
<footer
    id="app-footer"
    class="grid grid-cols-10 items-center flex min-h-[3.5rem] text-[0.94rem] px-sm xl:px-lg bg-white border-t-2 border-bcdsGray mx-[15rem]"
>
<nav class="col-span-7 flex justify-between justify-content-end">
<ul class="p-0 list-none">
<AppFooterNavLink
          v-for="(link, index) in links"
          :key="index"
          :text="link.text"
          :route="link.route"
          :target="link.target || '_blank'"
          :isLast="index === links.length - 1"
        />
</ul>
</nav>
<aside class="col-span-3 flex justify-self-end justify-content-end">
<span class="text-bcdsGray-50">v3.0.0 df0ab7
<span class="p-sm m-huge rounded-md bg-surface-tertiary text-bcdsGray-80 border-bcdsGray-80 border shadow-xs">Dev</span></span>
</aside>

</footer>
</template>
<script setup lang="ts">
const links = [
  { text: 'About', route: '/' },
  { text: 'Disclaimer', route: 'https://www2.gov.bc.ca/gov/content/home/disclaimer' },
  { text: 'Privacy', route: 'https://www2.gov.bc.ca/gov/content/home/privacy' },
  { text: 'Accessibility', route: 'https://www2.gov.bc.ca/gov/content/home/accessibility' },
  { text: 'Copyright', route: 'https://www2.gov.bc.ca/gov/content/home/copyright' }
]
</script>
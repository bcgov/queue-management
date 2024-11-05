<template>
<li
    :class="{
      'inline-block mr-1 lg:pr-2 xl:mr-2': true,
      'lg:border-r border-solid border-bcdsGray80': true
    }"
>
<nuxt-link
      :to="route"
      class="px-md py-xs text-black font-bold hover:underline"
      :target="target"
>
      {{ text }}
</nuxt-link>
</li>
</template>
<script setup lang="ts">
defineProps<{
  text: string,
  route: string,
  target: string,
  isLast: boolean
}>()
</script>
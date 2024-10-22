<template>
<button
   @click="onClick"
   class="p-sm m-huge  rounded-md bg-surface-primary text-white border-bcdsBlue border shadow-xs"
>
<span class="mr-2 max-w-28">Login</span>
</button>
</template>
<script>
export default {
 methods: {
   onClick() {
     console.log('Button clicked!');
   },
 },
};
</script>

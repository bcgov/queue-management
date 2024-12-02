<template>
<div class="flex items-center space-x-2">
  <div class="relative inline-block text-left">
    <button
      @click="toggleDropdown"
      class="p-sm m-xs inline-flex justify-center w-full px-hair py-xs rounded-md border border-gray-300 shadow-sm bg-white text-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary mr-2"
      :aria-expanded="isOpen.toString()"
    >
      <font-awesome-icon icon="bars" style="font-size: 1.18rem" />
    </button>

    <div v-if="isOpen" class="absolute right-0 z-10 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
      <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="dropdown-button">
        <template v-for="(item, index) in items" :key="index">
          <div v-if="item.condition === undefined || item.condition">
            <button
              v-if="item.action"
              @click.prevent="item.action"
              class="block px-md py-sm text-gray-700 hover:bg-gray-100 text-left w-full"
              role="menuitem"
            >
              <font-awesome-icon
                v-if="item.icon"
                :icon="item.icon"
                class="mr-2"
              />
              {{ item.text }}
            </button>
            <router-link
              v-else-if="item.to"
              :to="item.to"
              class="block px-md py-sm text-gray-700 hover:bg-gray-100 text-left w-full"
              role="menuitem"
            >
              <font-awesome-icon
                v-if="item.icon"
                :icon="item.icon"
                class="mr-2"
              />
              {{ item.text }}
            </router-link>
          </div>
          <div v-if="item.divider" class="border-t border-gray-200"></div>
        </template>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, defineProps, watch } from 'vue';

const props = defineProps({
  showDropdown: {
    type: Boolean,
    required: true
  },
  items: {
    type: Array,
    required: true
  }
});

const isOpen = ref(false);

watch(() => props.showDropdown, (newVal) => {
  isOpen.value = newVal;
});

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};
</script>

<style scoped>
</style>

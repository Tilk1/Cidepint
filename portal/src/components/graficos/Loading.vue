<template>
  <div>
    <div v-if="loading && !showError">
      <div
        class="px-3 py-1 text-xs font-medium leading-none text-center text-blue-800 bg-blue-200 rounded-full animate-pulse dark:bg-blue-900 dark:text-blue-200 mt-2"
      >
        Cargando datos...
      </div>
    </div>
    <div v-if="showError">
      <div
        class="flex items-center p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800 mt-2"
        role="alert"
      >
        <svg
          class="flex-shrink-0 inline w-4 h-4 me-3"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <span class="sr-only">Error</span>
        <div>
          <span class="font-medium">Se ha producido un error al cargar los datos.</span>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted } from 'vue';

const props = defineProps({
  loading: Boolean
});

const showError = ref(false);

onMounted(() => {
  setTimeout(() => {
    if (props.loading) {
      showError.value = true;
    }
  }, 10000);
});
</script>



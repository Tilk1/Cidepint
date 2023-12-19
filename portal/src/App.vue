<template>
  <div class="max-w-7xl mx-auto">
    <keep-alive>
    <NavBar />
    </keep-alive>
    <RouterView />
  </div>
</template>
<script setup>
import NavBar from './components/NavBar.vue'
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { initFlowbite } from 'flowbite'
onMounted(() => {
  initFlowbite()
})
</script>
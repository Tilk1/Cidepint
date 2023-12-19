<template>
    <div class="flex justify-center">
      <div class="w-full lg:w-2/3">
        <h1 class="flex items-center text-4xl font-extrabold dark:text-white mb-8">Mis solicitudes<span class="bg-blue-100 text-blue-800 text-2xl font-semibold mr-2 px-2.5 py-3 rounded dark:bg-blue-200 dark:text-blue-800 ml-2">Servicios</span></h1>
        <ListaMisSolicitudes></ListaMisSolicitudes>
      </div>
    </div>
    <br>
  </template>  
<script setup>
import ListaMisSolicitudes from '@/components/ListaMisSolicitudes.vue'
</script>
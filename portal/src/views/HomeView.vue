<template>
  <section class="bg-white dark:bg-gray-900">
    <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
      <div class="mr-auto place-self-center lg:col-span-7">
        <h1 class="mb-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-5xl lg:text-5xl">
          <span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">CIDEPINT</span>
            Portal Publico
          </h1>
        <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">
          Desde este sitio podras acceder al mapa con las ubicaciones de los centros, utilizar el
          buscador de servicios y realizar pedidos de servicios
        </p>
        <Suspense>
          <Contacto/>
        </Suspense>
      </div>
      <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
        <Carrusel />
      </div>
    </div>
  </section>
</template>
<script setup>
  import { initFlowbite } from 'flowbite'
  import { onMounted } from 'vue'
  import Carrusel from '../components/Carrusel.vue'
  import Contacto from '../components/Contacto.vue'

  onMounted(() => {
    initFlowbite();
  })

</script>

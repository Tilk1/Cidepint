<template>
  <h1 class="flex items-center text-4xl font-extrabold dark:text-white mb-8">
    Estadisticas<span
      class="bg-blue-100 text-blue-800 text-2xl font-semibold mr-2 px-2.5 py-3 rounded dark:bg-blue-200 dark:text-blue-800 ml-2"
      >Servicios</span
    >
  </h1>

  <div id="accordion-nested-parent" data-accordion="collapse">
    <h2 id="accordion-collapse-heading-1">
      <button
        type="button"
        class="flex items-center justify-between w-full p-5 font-medium text-left text-gray-500 border border-b-0 border-gray-200 rounded-t-xl focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
        data-accordion-target="#accordion-collapse-body-1"
        aria-expanded="true"
        aria-controls="accordion-collapse-body-1"
      >
        <span>¿Que puedo analizar en las estadisticas?</span>
        <svg
          data-accordion-icon
          class="w-3 h-3 rotate-180 shrink-0"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 10 6"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 5 5 1 1 5"
          />
        </svg>
      </button>
    </h2>
    <div
      id="accordion-collapse-body-1"
      class="hidden"
      aria-labelledby="accordion-collapse-heading-1"
    >
      <div class="p-5 border border-b-0 border-gray-200 dark:border-gray-700 dark:bg-gray-900">
        <p class="mb-2 text-gray-500 dark:text-gray-400">
          Esta sección permite visualizar información estadística que pueda ser de utilidad tanto
          para los visitantes, los SuperAdmin como para los dueños de cada institución.
        </p>
        <p class="mb-2 text-gray-500 dark:text-gray-400">
          Actualmente hay 3 tipos de estadisticas:
        </p>
        <div id="accordion-nested-collapse" data-accordion="collapse">
          <h2 id="accordion-nested-collapse-heading-1">
            <button
              type="button"
              class="flex items-center justify-between w-full p-5 rounded-t-xl font-medium text-left text-gray-500 border border-b-0 border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              data-accordion-target="#accordion-nested-collapse-body-1"
              aria-expanded="false"
              aria-controls="accordion-nested-collapse-body-1"
            >
              <span
                >Gráfico de torta con la cantidad de las solicitudes realizadas agrupadas por
                estado.</span
              >
              <svg
                data-accordion-icon
                class="w-3 h-3 rotate-180 shrink-0"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 10 6"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5 5 1 1 5"
                />
              </svg>
            </button>
          </h2>
          <div
            id="accordion-nested-collapse-body-1"
            class="hidden"
            aria-labelledby="accordion-nested-collapse-heading-1"
          >
            <div class="p-5 border border-b-0 border-gray-200 dark:border-gray-700">
              <div class="max-w-xl max-h-xs mx-auto">
                <Torta />
              </div>
            </div>
          </div>
          <h2 id="accordion-nested-collapse-heading-2">
            <button
              type="button"
              class="flex items-center justify-between w-full p-5 font-medium text-left text-gray-500 border border-b-0 border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              data-accordion-target="#accordion-nested-collapse-body-2"
              aria-expanded="false"
              aria-controls="accordion-nested-collapse-body-2"
            >
              <span>Ranking de los servicios más solicitados</span>
              <svg
                data-accordion-icon
                class="w-3 h-3 rotate-180 shrink-0"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 10 6"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5 5 1 1 5"
                />
              </svg>
            </button>
          </h2>
          <div
            id="accordion-nested-collapse-body-2"
            class="hidden"
            aria-labelledby="accordion-nested-collapse-heading-2"
          >
            <div class="p-5 border border-b-0 border-gray-200 dark:border-gray-700">
              <p class="text-gray-500 dark:text-gray-400">
                <div>
                <BarrasVerticales />
                </div>
              </p>
            </div>
          </div>
          <h2 id="accordion-nested-collapse-heading-3">
            <button
              type="button"
              class="flex items-center justify-between w-full p-5 font-medium text-left text-gray-500 border border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              data-accordion-target="#accordion-nested-collapse-body-3"
              aria-expanded="false"
              aria-controls="accordion-nested-collapse-body-3"
            >
              <span>Top 10 de las Instituciones con mejor tiempo de resolución</span>
              <svg
                data-accordion-icon
                class="w-3 h-3 rotate-180 shrink-0"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 10 6"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5 5 1 1 5"
                />
              </svg>
            </button>
          </h2>
          <div
            id="accordion-nested-collapse-body-3"
            class="hidden"
            aria-labelledby="accordion-nested-collapse-heading-3"
          >
            <div class="p-5 border border-gray-200 dark:border-gray-700">
              <p class="mb-2 text-gray-500 dark:text-gray-400">
                            <div>
                <BarrasHorizontales />
              </div>
              </p>
              
            </div>
          </div>
        </div>
        <!-- End: Nested accordion -->
      </div>
    </div>
  

    </div>
    




</template>

<script setup>
import BarrasVerticales from '../components/graficos/BarrasVerticales.vue'
import BarrasHorizontales from '../components/graficos/BarrasHorizontales.vue'
import Torta from '../components/graficos/Torta.vue'
import { initFlowbite } from 'flowbite'
import { onMounted } from 'vue'
onMounted(() => {
  initFlowbite()
})
</script>

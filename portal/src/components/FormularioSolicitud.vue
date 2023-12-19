<template>
  <form @submit.prevent="submitForm" class="mb-6">
    <div v-if="servicio" class="mb-5">
      <h1>Servicio al que se va realizar la solicitud: {{ servicio.nombre }}</h1>
    

    <Alerta v-if="msjExito" mensaje="Solicitud enviada" tipoAlerta="exito"></Alerta>
    <Alerta v-if="msjError" mensaje="Hubo un problema en la solicitud" tipoAlerta="error"></Alerta>

    <label for="titulo" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >Titulo de la solicitud (*)</label
    >
    <input
      type="text"
      v-model="titulo"
      id="titulo"
      class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
      required
    />

    <div
      class="w-full mb-4 mt-2 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600"
    >
      <div class="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
        <label for="comment" class="sr-only">Your comment</label>
        <textarea
          id="comment"
          v-model="comentario"
          rows="4"
          class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400"
          placeholder="Descripcion..."
          required
        ></textarea>
      </div>
      <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
        <div class="flex pl-0 space-x-1 sm:pl-2">
          <!-- <button
            type="button"
            class="inline-flex justify-center items-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600"
          >
            <svg
              class="w-4 h-4"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 12 20"
            >
              <path
                stroke="currentColor"
                stroke-linejoin="round"
                stroke-width="2"
                d="M1 6v8a5 5 0 1 0 10 0V4.5a3.5 3.5 0 1 0-7 0V13a2 2 0 0 0 4 0V6"
              />
            </svg>
            <span class="sr-only">Adjuntar archivo</span>
          </button> -->
        </div>
      </div>
    </div>

    <p class="ml-auto text-xs mb-5 text-gray-500 dark:text-gray-400">
      Recuerde que el tiempo de respuesta de su solicitud puede variar, para mas información
      consulte los tiempos promedio de consulta aqui:
      <a href="/estadisticas" class="text-blue-600 dark:text-blue-500 hover:underline"
        >Top 10 de las Instituciones con mejor tiempo de resolución</a
      >.
    </p>
    <p class="ml-auto text-xs mb-5 text-gray-500 dark:text-gray-400">
      Los campos con (*) son obligatorios
    </p>

    <div
      class="px-3 py-1 text-xs font-medium leading-none text-center text-blue-800 bg-blue-200 rounded-full animate-pulse dark:bg-blue-900 dark:text-blue-200 mb-5"
      v-if="isLoading"
    >
      loading...
    </div>

    <button
      type="submit"
      v-if="!msjExito"
      class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
    >
      Solicitar
    </button>
  </div>
  </form>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ServicioClase from '../services/ServicioService.js'
import Alerta from './Alerta.vue'
import { useRoute } from 'vue-router'
import { usuarioStore } from '../stores/auth'

const store = usuarioStore()
const token = store.token
const isLoading = ref(false)
const msjExito = ref(false)
const msjError = ref(false)
const servicio = ref(null)
const titulo = ref('')
const comentario = ref('')
const route = useRoute()
const id_servicio = route.params.id_servicio

function existe_servicio() {
  if (servicio.value !== null) {
    return true
  }
  return false
}

onMounted(async () => {
  initFlowbite()
  try {
    servicio.value = await new ServicioClase().getServicio(id_servicio)
  } catch (error) {
    console.log(error)
  }
})

async function submitForm() {
  isLoading.value = true

  // Llamada al servicio con los datos del formulario
  try {
    await new ServicioClase().postSolicitudServicio(
      id_servicio,
      titulo.value,
      comentario.value,
      token
    )
    setTimeout(() => {
      isLoading.value = false
      msjError.value = false
      msjExito.value = true
    }, 2000)
  } catch (error) {
    setTimeout(() => {
      isLoading.value = false
      msjExito.value = false
      msjError.value = true
      console.log(error)
    }, 2000)
  }
}
</script>

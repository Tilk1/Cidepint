<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-4 py-3">Solicitud</th>
          <th scope="col" class="px-10 py-3">Ultima actualización</th>
          <th scope="col" class="px-10 py-3">Estado</th>
          <th scope="col" class="px-1 py-4">Ver</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(solicitud, index) in solicitudes.data"
          :key="index"
          class="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
        >
          <th
            scope="row"
            class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
          >
            {{ solicitud.titulo }}
          </th>
          <th
            scope="row"
            class="px-10 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
          >
            {{ formatearFecha(solicitud.actualizado_el) }}
          </th>
          <th
            scope="row"
            class="px-10 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
          >
            {{ solicitud.estado }}
          </th>
          <td class="px-1 py-4">
            <router-link :to="'/solicitud_servicio/' + solicitud.id">
              <button
                type="button"
                class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-4 py-2.5 text-center me-2 mb-2"
              >
                Notas y detalle
              </button>
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-if="solicitudesCargadas && solicitudes.data.length === 0" class="flex justify-center mt-5">
    <p class="text-gray-700 dark:text-gray-400">Usted no posee solicitudes realizadas</p>
  </div>

  <Loading :loading="loading"></Loading>

  <nav
    class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4"
    aria-label="Table navigation"
  >
    <span
      class="text-sm font-normal text-gray-500 dark:text-gray-400 mb-4 md:mb-0 block w-full md:inline md:w-auto"
    >
      Pagina actual:
      <span class="font-semibold text-gray-900 dark:text-white"
        >{{ paginaActual }} - {{ paginas }}</span
      >
      , total de elementos:
      <span class="font-semibold text-gray-900 dark:text-white">{{ solicitudes.total }}</span>
    </span>
    <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8">
      <li v-if="paginaActual > 1">
        <a
          @click.prevent="cambiarPagina(paginaActual - 1)"
          href="#"
          class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
          >Anterior</a
        >
      </li>
      <li v-for="pagina in paginas" :key="pagina">
        <a
          @click.prevent="cambiarPagina(pagina)"
          href="#"
          class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
          :class="{ 'bg-blue-200 text-blue-600': pagina === paginaActual }"
          >{{ pagina }}</a
        >
      </li>
      <li v-if="paginaActual < paginas">
        <a
          @click.prevent="cambiarPagina(paginaActual + 1)"
          href="#"
          class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
          >Siguiente</a
        >
      </li>
    </ul>
  </nav>

  <br />
  <form>
    <label for="campo_busqueda" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Criterio orden</label>
    <select
      v-model="campo_busqueda"
      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    >
      <option value="creado_el">Fecha de creacion</option>
      <option value="actualizado_el">Fecha de actualizacion</option>
      <option value="titulo">Titulo</option>
      <option value="estado">Estado</option>
    </select>

    <br />
    <!-- busqueda avanzada -->
    <select
      v-model="orden"
      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    >
      <option value="asc">Orden ascendente</option>
      <option value="desc">Orden descendente</option>
    </select>
  </form>
</template>

<script setup>
import { onMounted, ref, onBeforeUpdate } from 'vue'
import { usuarioStore } from '../stores/auth'
import ServicioSolicitudClase from '../services/ClaseSolicitudes'
import { watch } from 'vue'
import Loading from './graficos/Loading.vue'

const store = usuarioStore()
const token = store.token
const solicitudes = ref({})
const solicitudesCargadas = ref(false)
const paginas = ref(0)
const paginaActual = ref(1)
const campo_busqueda = ref('actualizado_el')
const orden = ref('asc')
const loading = ref(true)

const cambiarPagina = (nuevaPagina) => {
  paginaActual.value = nuevaPagina
}

const obtenerSolicitudes = async () => {
  try {
    const response = await new ServicioSolicitudClase().getSolicitudes(paginaActual.value, token, orden.value, campo_busqueda.value)
    loading.value = false
    solicitudes.value = response
    solicitudesCargadas.value = true
    paginas.value = Math.ceil(solicitudes.value.total / solicitudes.value.per_page)
  } catch (error) {
    console.error('Error al obtener datos:', error)
  }
}

onMounted(onMounted(obtenerSolicitudes))

watch([paginaActual, orden, campo_busqueda ], () => {
  loading.value = true
  obtenerSolicitudes()
})


const formatearFecha = (fecha) => {
  const fechaObjeto = new Date(fecha)
  const dia = fechaObjeto.getDate()
  const mes = fechaObjeto.toLocaleString('default', { month: 'short' })
  const año = fechaObjeto.getFullYear()
  const horas = fechaObjeto.getHours()
  const minutos = fechaObjeto.getMinutes()
  const fechaFormateada = `${dia} ${mes} ${año} ${horas}:${minutos}`
  return fechaFormateada
}
</script>

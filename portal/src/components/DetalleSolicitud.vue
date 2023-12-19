<template>
  <div v-if=existe_solicitud>
  <div
    class="w-full max-w-md p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-8 dark:bg-gray-800 dark:border-gray-700"
  >
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white">
        {{ solicitud.titulo }}
      </h5>
      <a href="#" class="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500">
        <span
          class="bg-blue-50 text-blue-800 text-2xl font-semibold me-2 px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-2"
        >
          {{ solicitud.estado }}</span
        >
      </a>
    </div>
    <div class="flow-root">
      <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
        <li class="py-3 sm:py-4">
          <div class="flex items-center">
            <div class="flex-1 min-w-0 ms-4">
              <p class="text-sm font-medium text-gray-900 truncate dark:text-white">{{ solicitud.detalle }}</p>
            </div>
          </div>
        </li>
        <li class="pt-3 pb-0 sm:pt-4">
          <div class="flex items-center">
            <div class="flex-1 min-w-0 ms-4">
              <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
                Fecha de creación:
              </p>
            </div>
            <div
              class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
            >
              {{ formatearFecha(solicitud.creado_el) }}
            </div>
          </div>
        </li>
        <li class="pt-3 pb-0 sm:pt-4">
          <div class="flex items-center">
            <div class="flex-1 min-w-0 ms-4">
              <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
                Ultima modificación:
              </p>
            </div>
            <div
              class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
            >
              {{ formatearFecha(solicitud.actualizado_el) }}
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import ServicioClase from '../services/SolicitudServicio'
import { useRoute } from 'vue-router'
import { usuarioStore } from '../stores/auth'

const store = usuarioStore();
const token = store.token
const solicitud = ref({})
const id_solicitud = useRoute().params.id_solicitud
const existe_solicitud = ref(false)

onMounted(async () => {
  try {
    solicitud.value = await new ServicioClase().getDetalleSolicitud(id_solicitud,token)
    existe_solicitud.value = true
  } catch (error) {
    console.error(error)
  }
})

const formatearFecha = (fecha) => {
  const fechaObjeto = new Date(fecha);
  const dia = fechaObjeto.getDate();
  const mes = fechaObjeto.toLocaleString('default', { month: 'short' });
  const año = fechaObjeto.getFullYear();
  const horas = fechaObjeto.getHours();
  const minutos = fechaObjeto.getMinutes();
  const fechaFormateada = `${dia} ${mes} ${año} ${horas}:${minutos}`;
  return fechaFormateada;
};

</script>

<template>
<div v-if=existe_solicitud>
<div>
    <div v-for="(message, index) in notas.data" :key="index">
        <div class="flex">
          <img class="w-8 h-8 rounded-full mr-2" src="https://images.squarespace-cdn.com/content/v1/54b7b93ce4b0a3e130d5d232/1519987020970-8IQ7F6Z61LLBCX85A65S/icon.png?format=500w" alt="User Avatar"/>
          <div class="ms-3 text-sm font-normal">
            <span class="mb-1 text-sm font-semibold">{{ message.usuario.nombre }}</span>
            <div class="mb-2 text-sm font-normal">{{ message.nota.nota }}</div>
          </div>
      </div>
    </div>
  </div>


  <label for="message" class="block mb-2 mt-5 text-sm font-medium text-gray-900 dark:text-white"
    >Mensaje de nota a agregar</label
  >
  <textarea
    id="message"
    rows="4"
    v-model="msj_nota"
    class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    placeholder="Escribe tu nota aqui..."
  ></textarea>
  <button
      type="submit"
      class="inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800 mt-2"
      @click="agregarNota"
    >
      Agregar nota
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ServicioClase from '../services/SolicitudServicio'
import { useRoute } from 'vue-router'
import { usuarioStore } from '../stores/auth'

const store = usuarioStore();
const token = store.token
const route = useRoute()
const notas = ref({})
const id_solicitud = route.params.id_solicitud
const msj_nota = ref('')
const existe_solicitud = ref(false)

onMounted(async () => {
  try {
    const response = await new ServicioClase().getNotas(id_solicitud)
    existe_solicitud.value = true
    notas.value = response
  } catch (error) {
    console.error('Error al obtener datos:', error)
  }
})

const agregarNota = async () => {
  try {
    await new ServicioClase().postNota(msj_nota.value,token, id_solicitud);
    const response = await new ServicioClase().getNotas(id_solicitud)
    notas.value = response
    msj_nota.value = ''
  } catch (error) {
    console.error('Error al agregar nota:', error);
  }
};

</script>
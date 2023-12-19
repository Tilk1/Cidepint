<template>
  <div v-for="mensaje in mensajes" v-if="mostrarAlerta">
        <Alerta :mensaje="mensaje" :tipoAlerta="colorAlerta"></Alerta>    
    </div>
  <form @submit.prevent="handleSubmit">
    <div class="grid gap-6 mb-6 md:grid-cols-2">
      <div class="relative">
        <input v-model="servicio.nombre" type="text" id="nombre" class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " />
        <label for="nombre" class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Nombre del Servicio</label>
      </div>
      <div class="relative">
        <input v-model="servicio.descripcion" type="text" id="descripcion" class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " />
        <label for="descripcion" class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Descripción</label>
      </div>
      <div class="relative">
        <input v-model="servicio.institucion" type="text" id="institucion" class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " />
        <label for="institucion" class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Institucion que brinda el servicio</label>
      </div>
    </div>
    <div class="relative">
        <input v-model="servicio.palabras_claves" type="text" id="palabras_claves" class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " />
        <label for="palabras_claves" class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Palabras claves</label>
      </div>

    <div class="mb-2 mt-5">
      <select v-model="servicio.tipo" id="tipo" class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-auto text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" >
        <option value="" selected hidden>Tipo de Servicio</option>
        <option value="" >Sin tipo</option>
        <option value="Análisis">Análisis</option>
        <option value="Desarrollo">Desarrollo</option>
        <option value="Consultoría">Consultoría</option>
      </select>
    </div>

    <button type="submit" class="mt-5 px-5 py-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-900 dark:focus:ring-blue-800">Buscar</button>
  </form>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import ServicioClase from '../services/ClaseServicio';
import Alerta from '../components/Alerta.vue'

const servicio = ref({
  nombre: '',
  descripcion: '',
  institucion: '',
  palabras_claves: '',
  tipo: '',
});
const servicios = ref({})
const router = useRouter();
let mensajes = ref([]);
let mostrarAlerta = ref(false);
let colorAlerta = ref('')


const handleSubmit = async () => {
  const response = await new ServicioClase().buscarServicios(servicio.value);
  servicios.value = response; 
  if(servicios.value.total == 0){
    colorAlerta.value = "error"
    mensajes.value[0] = 'No se encontraron servicios con los parametros ingresados';
    mostrarAlerta.value = true;
  }
  else{
    //serializo el objeto para poder pasarlo como parametro en la ruta
    const serviciosEncontradosString = JSON.stringify(servicios.value);
    const servicioBuscadoString = JSON.stringify(servicio.value);
    router.push({ name: 'TablaDeServiciosView', params: { serviciosEncontrados: serviciosEncontradosString, servicioBuscado:servicioBuscadoString } })
  }
};

</script>

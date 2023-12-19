<template>
    <div class="relative overflow-x-auto">
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400 ">
                <tr>
                    <th scope="col" class="px-6 py-3 flex items-center justify-center">
                        Detalles
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Nombre
                    </th>
                    <th scope="col" class="px-6 py-3 flex items-center justify-center">
                        Descripcion
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Tipo
                    </th>
                    <th scope="col" class="px-6 py-3 flex items-center justify-center">
                        Etiquetas
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Institucion
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700" v-for="(servicio, index) in servicios['data']" :key="index">
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white flex items-center justify-center">
                        <router-link :to="{ name: 'DetalleServicioView', params: { id: servicio.id } }">
                            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 14">
                            <g stroke="#362F78" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                            <path d="M10 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>
                            <path d="M10 13c4.97 0 9-2.686 9-6s-4.03-6-9-6-9 2.686-9 6 4.03 6 9 6Z"/>
                            </g>
                            </svg>
                        </router-link>
                    </td>
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white ">
                        {{servicio.nombre}}
                    </td>
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white flex items-center justify-center">
                        {{servicio.descripcion}}
                    </td>
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{servicio.tipo}}
                    </td>
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white flex items-center justify-center">
                        {{servicio.palabras_claves}}
                    </td>
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{servicio.institucion}}
                    </td>
                </tr>
            </tbody>
        </table>

                <!-- Paginado -->
        <nav class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4" aria-label="Table navigation">
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mb-4 md:mb-0 block w-full md:inline md:w-auto">
            Página <span class="font-semibold text-gray-900 dark:text-white">{{ servicios['page'] }}-{{ total_paginas }}</span> 
            - Total de elementos <span class="font-semibold text-gray-900 dark:text-white">{{ servicios['total'] }}</span>
            </span>   
            <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8">
            <li v-if="servicios['page'] > 1">
            <a @click="cambiarPagina(servicios['page'] - 1, servicios['per_page'])" class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Atras</a>
            </li>
            <li v-for="i in calcularRangoPaginas()" :key="i">
            <a @click="cambiarPagina(i,servicios['per_page'])" class="flex items-center justify-center px-3 h-8 leading-tight text-black-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">{{ i }}</a>
            </li>
            <li v-if="servicios['page'] < servicios['total'] / servicios['per_page']">
            <a @click="cambiarPagina(servicios['page'] + 1,servicios['per_page'])" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Siguiente</a>
            </li>
            </ul>
        </nav>
    </div>
    <br>
    <!-- Paginado del usuario -->
    <div>
        <label for="states" class="sr-only">Choose a state</label>
        <span class="text-sm font-normal text-gray-500 dark:text-gray-400 mb-4 md:mb-0 block w-full md:inline md:w-auto">
        Cantidad de elementos por página: </span>
        <select v-model="cant_elem" @change="cambiarPaginado(cant_elem)" id="states" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-e-lg border-s-gray-100 dark:border-s-gray-700 border-s-2 focus:ring-blue-500 focus:border-blue-500 block w-auto p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <option selected></option>
        <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
        </select>
    </div>
    <div>
        <router-link :to="{ name: 'BuscadorServiciosView' }">
            <button type="button" class=" mt-7 mr-5 px-5 py-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-900 dark:focus:ring-blue-800">Buscador de Servicios</button>
        </router-link>
    </div> 
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import ServicioClase from '../services/ClaseServicio';

const servicios = ref([])
const servBuscado = ref('')
const route = useRoute();
const total_paginas = ref(0)
const cant_elem = ref(0)

onMounted(async () => { 
    try {
        if(route.params.serviciosEncontrados) {
            servicios.value = JSON.parse(route.params.serviciosEncontrados);
            servBuscado.value = JSON.parse(route.params.servicioBuscado)

        } else {
            const response = await new ServicioClase().listarServicios();
            servicios.value = response;
        }
        cant_elem.value = servicios.value.per_page
        total_paginas.value = Math.floor(servicios.value.total / servicios.value.per_page) + (servicios.value.total % servicios.value.per_page !== 0 ? 1 : 0);
    } catch (error) {
        console.error('Error al obtener datos', error);
    }
})

const cambiarPagina = async (page, per_page) => {
  try {
    if(route.params.serviciosEncontrados) {
        const response = await new ServicioClase().buscarServicios(servBuscado.value, page, per_page);
        servicios.value = response;
    }
    else{
        const response = await new ServicioClase().listarServicios(page, per_page);
        servicios.value = response;
    }
  } catch (error) {
    console.error('Error al obtener datos de la página:', error);
  }
};

const calcularRangoPaginas = () => {
  const inicio = Math.max(1, servicios.value.page - 3);
  const fin = Math.min(servicios.value.total / servicios.value.per_page, inicio + 4);
  return Array.from({ length: fin - inicio + 2 }, (_, i) => inicio + i);
};

const cambiarPaginado = async (seleccion) => {
    try {
        cant_elem.value = seleccion
        if(route.params.serviciosEncontrados) {
        const response = await new ServicioClase().buscarServicios(servBuscado.value, 1, seleccion);
        servicios.value = response;
    }
    else{
        const response = await new ServicioClase().listarServicios(1, seleccion);
        servicios.value = response;
    }
    total_paginas.value = Math.floor(servicios.value.total / servicios.value.per_page) + (servicios.value.total % servicios.value.per_page !== 0 ? 1 : 0);
  } catch (error) {
    console.error('Error al obtener datos de la página:', error);
  }  
}
</script>

<template>
  <!-- Contenedor principal -->
  <div class="flex flex-col md:flex-row">
    <!-- Columna 1: Detalle del servicio y detalle de la institución -->
    <div class="max-w-full md:w-1/2 p-4">
      <!-- Detalle del servicio -->
      <div class="max-w-full p-6 bg-white border border-blue-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        <a href="#">
          <h5 class="mb-2 text-2xl md:text-3xl font-bold tracking-tight text-gray-900 dark:text-white">{{ servicio.nombre }}</h5>
        </a>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Descripcion: {{ servicio.descripcion }}
        </p>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Tipo: {{ servicio.tipo }}
        </p>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Etiquetas: {{ servicio.palabras_claves }}
        </p>
      </div>
      <!-- Detalle de la institucion -->
      <div class="max-w-full p-6 bg-white border border-blue-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 mt-4">
        <a href="#">
          <h5 class="mb-2 text-2xl md:text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Institucion {{ servicio.institucion }}</h5>
        </a>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Dias de atencion: {{ institucion.dias_horarios }}
        </p>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Dirección: {{ institucion.direccion }}
        </p>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Contácto: {{ institucion.info_contacto }}
        </p>
        <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
          Web: {{ institucion.web }}
        </p>
      </div>
      <div class="mt-4 md:mt-7">
        <!-- Botones para volver al buscador o al listado  -->
        <div class="flex flex-col md:flex-row">
          <router-link :to="{ name: 'BuscadorServiciosView' }">
            <button type="button" class="mb-2 md:mb-0 md:mr-2 px-4 md:px-5 py-2 md:py-3 text-base md:text-lg font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-900 dark:focus:ring-blue-800">Buscador de Servicios</button>
          </router-link>
          <router-link :to="{ name: 'ServiciosView' }">
            <button type="button" class="px-4 md:px-5 py-2 md:py-3 text-base md:text-lg font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-900 dark:focus:ring-blue-800">Todos los Servicios</button>
          </router-link>
        </div>
      </div>
    </div>
    <!-- Columna 2: Mapa-->
    <div id="mapaContenedor" class="w-full md:w-1/2 mt-4 md:mt-0">
      <h5 class="mb-2 text-2xl md:text-3xl font-bold text-center tracking-tight text-gray-900 dark:text-white">Ubicacion</h5>
      <div id="map" class="max-w-full" style="width: 100%; height: 400px;"></div>
      <div v-if="autenticado()">
        <router-link :to="{ name: 'SolicitudView', params: { id_servicio: obtenerId() } }">
          <button type="button" class="mb-5 mt-4 md:mt-7 px-4 md:px-5 py-2 md:py-3 text-base md:text-lg font-medium text-center text-white bg-purple-700 rounded-lg hover:bg-purple-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-900 dark:focus:ring-blue-800">Solicitar servicio</button>
        </router-link>
      </div>
    </div>
  </div>
</template>


<script setup>
import ServicioClase from '../services/ClaseServicio';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { usuarioStore } from '../stores/auth'


const route = useRoute();
const servicio = ref('')
const institucion = ref('')
const coord = ref('') 
const store = usuarioStore();

onMounted(async () => { 
    try {
        servicio.value = await new ServicioClase().buscarServicio(route.params.id);
        institucion.value = await new ServicioClase().buscarInstitucion(servicio.value.institucion);
        coord.value = await new ServicioClase().obtenerCoordenadas(institucion.value.direccion);
      
        // myMap es el mapa que se visualizara en el div con id="map" 
        const myMap = L.map('map').setView([coord.value['latitude'], coord.value['longitude']], 16);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19, attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(myMap);

        //Personalizacion del marcador
        var estiloPopup = {'maxWidth': '300'}
        var iconoBase = L.Icon.extend({
          options: {
            iconSize:     [80, 80],
            popupAnchor:  [0, -40]
            }
        });
        var popupContent = `<h1>${institucion.value.nombre}</h1> <p>${institucion.value.direccion}</p>`;
        var iconoFachero = new iconoBase({iconUrl: 'https://i.postimg.cc/PfSg4Wgk/Dise-o-sin-t-tulo.png'})
        // marker es un marcador que se visualizara en el mapa, segun las coordenadas que se le pasen.
        L.marker([coord.value['latitude'], coord.value['longitude']], {icon: iconoFachero}).bindPopup(popupContent,estiloPopup).addTo(myMap);



    } catch (error) {
        console.error('Error al obtener datos:', error);
    }
})

function autenticado(){
      return store.estaLogeado;
    };

function obtenerId(){
      return route.params.id;
    };

</script>

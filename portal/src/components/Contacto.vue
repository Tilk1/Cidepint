<template>
    <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">
        Podes contactarnos a <b>{{ info.info_contacto }}</b>
    </p>
    <Alerta v-if="mostrarAlerta" mensaje="Informacion de contacto copiada con exito" tipoAlerta="exito"></Alerta>
    <button @click='copiarPortapapeles' class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800">
        Copiar al portapapeles
    </button>
</template>
<script setup>
    import { ref } from 'vue'
    import ConfiguracionServicio from '../services/ConfiguracionServicio'
    import Alerta from '../components/Alerta.vue'

    let mostrarAlerta = ref(false);
    let info = ref('');
    info = await new ConfiguracionServicio().obtenerInfoContacto();

    function copiarPortapapeles(){
        navigator.clipboard.writeText(info.info_contacto);
        mostrarAlerta.value = true;
        setTimeout(()=> {mostrarAlerta.value = false}, 2000);
    }

</script>
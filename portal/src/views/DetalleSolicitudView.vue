<template>
  <div v-if="autenticado()">
    <div class="flex flex-col">
      <h1 class="text-4xl font-extrabold dark:text-white mb-8">Detalle solicitud</h1>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="mb-4 sm:mb-0">
          <DetalleSolicitud />
        </div>
        <div>
          <ChatSolicitud />
        </div>
      </div>
    </div>
  </div>
</template>
  

<script setup>
import ChatSolicitud from '../components/ChatSolicitud.vue'
import DetalleSolicitud from '../components/DetalleSolicitud.vue'
import { usuarioStore } from '../stores/auth'

const store = usuarioStore();
function autenticado(){
      return store.estaLogeado;
    }

</script>

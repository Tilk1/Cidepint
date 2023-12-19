<template>
  <nav class="bg-white border-gray-200 dark:border-gray-600 dark:bg-gray-900 py-4 px-6">
    <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
      <a class="flex items-center">
        <img
          src="https://cidepint.ing.unlp.edu.ar/wp-content/uploads/2023/09/Logo-CIDEPINT-sept-2023.jpg"
          class="h-20 mr-3 hidden md:block"
          alt="Cidepint-Logo"
        />
        <span class="md:hidden text-2xl font-semibold">CIDEPINT</span>
      </a>
      <button
        data-collapse-toggle="mega-menu-full"
        type="button"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
        aria-controls="mega-menu-full"
        aria-expanded="false"
      >
        <span class="sr-only">Abrir menu principal</span>
        <svg
          class="w-5 h-5"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 17 14"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M1 1h15M1 7h15M1 13h15"
          />
        </svg>
      </button>
      <div
        id="mega-menu-full"
        class="items-center justify-between font-medium hidden w-full md:flex md:w-auto md:order-1"
      >
        <ul
          class="flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"
        >
          <li>
            <router-link
              to="/"
              class="block py-2 pl-3 pr-4 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-blue-500 md:dark:hover:bg-transparent dark:border-gray-700"
              aria-current="page"
            >
              Inicio
            </router-link>
          </li>
          <li>
            <button
              id="mega-menu-full-dropdown-button"
              data-collapse-toggle="mega-menu-full-dropdown"
              class="flex items-center justify-between w-full py-2 pl-3 pr-4 text-gray-900 rounded md:w-auto hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-600 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-blue-500 md:dark:hover:bg-transparent dark:border-gray-700"
            >
              Servicios
              <svg
                class="w-2.5 h-2.5 ml-2.5"
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
                  d="m1 1 4 4 4-4"
                />
              </svg>
            </button>
          </li>
          <li v-if="!autenticado()">
            <button
              id="botonDropdownRegistro"
              data-collapse-toggle="dropdownRegistro"
              class="flex items-center justify-between w-full py-2 pl-3 pr-4 text-gray-900 rounded md:w-auto hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-600 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-blue-500 md:dark:hover:bg-transparent dark:border-gray-700"
            >
              Registrarse
              <svg
                class="w-2.5 h-2.5 ml-2.5"
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
                  d="m1 1 4 4 4-4"
                />
              </svg>
            </button>
          </li>
          <li v-if="!autenticado()">
            <router-link
              to="/iniciar_sesion"
              class="block py-2 pl-3 pr-4 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-blue-500 md:dark:hover:bg-transparent dark:border-gray-700"
              aria-current="page"
            >
              Iniciar Sesion
            </router-link>
          </li>
          <li v-if="autenticado()">
            <button @click="cerrarSesion">Cerrar sesion</button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Opciones que se ven al clickear el el boton de Servicio -->
    <div
      id="mega-menu-full-dropdown"
      class="mt-1 border-gray-200 shadow-sm bg-gray-50 md:bg-white border-y dark:bg-gray-800 dark:border-gray-600 hidden"
    >
      <div
        class="grid max-w-screen-xl px-4 py-5 mx-auto text-gray-900 dark:text-white sm:grid-cols-2 md:px-6"
      >
        <ul>
          <li>
            <router-link
              to="/servicios"
              class="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <div class="font-semibold">Ver listado de servicios</div>
              <span class="text-sm text-gray-500 dark:text-gray-400">
                Visualizá los servicios prestados por cada institución
              </span>
            </router-link>
          </li>
          <li>
            <router-link
              to="/buscador_servicios"
              class="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <div class="font-semibold">Buscador de Servicios</div>
              <span class="text-sm text-gray-500 dark:text-gray-400"
                >Encontrá el servicio que estas buscando</span
              >
            </router-link>
          </li>
        </ul>
        <ul>
          <li v-if="autenticado()">
            <router-link to="/mis_solicitudes" class="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
              <div class="font-semibold">Mis solicitudes</div>
              <span class="text-sm text-gray-500 dark:text-gray-400"> Vea las solicitudes realizadas </span>
            </router-link>
          </li>
          <li v-else>
            <div class="block p-3 rounded-lg hover:bg-red-100 dark:hover:bg-red-700">
              <div class="font-semibold text-red-500">Mis solicitudes</div>
              <span class="text-sm text-red-400 dark:text-red-400"> Debes iniciar sesion para acceder a tus solicitudes </span>
            </div>
          </li>
          <li>
            <router-link
              to="/estadisticas"
              class="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <div class="font-semibold">Análisis de datos</div>
              <span class="text-sm text-gray-500 dark:text-gray-400">
                Analizá las últimas tendencias con nuestras estadísticas</span
              >
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <!-- Opciones que se ven al clickear el el boton de registro -->
    <div v-if="!autenticado()" id="dropdownRegistro" class="mt-1 border-gray-200 shadow-sm bg-gray-50 md:bg-white border-y dark:bg-gray-800 dark:border-gray-600 hidden">
      <div class="text-center grid max-w-screen-xl px-4 py-5 mx-auto text-gray-900 dark:text-white sm:grid-cols-1 md:px-6">
        <ul>
          <li>
            <router-link
              to="/registrarse-correo"
              class="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <div class="font-semibold">
                <i class="bi bi-envelope-fill"></i> Registrarse con correo
              </div>
              <span class="text-sm text-gray-500 dark:text-gray-400">
                Registrate en CIDEPINT a traves de tu correo
              </span>
            </router-link>
          </li>
          <li>
            <div class="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
              <div class="font-semibold">Registrarse con google</div>
              <GoogleLogin :callback="callback"/>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div v-for="mensaje in mensajes" v-if="mostrarAlerta">
    <Alerta :mensaje="mensaje" :tipoAlerta="colorAlerta"></Alerta>    
  </div>
</template>
<script setup> 
    import { usuarioStore } from '../stores/auth'
    import { decodeCredential } from 'vue3-google-login';
    import Alerta from '../components/Alerta.vue'
    import { useRouter } from 'vue-router'
    import { ref } from 'vue'

    let mensajes = ref([]);
    let mostrarAlerta = ref(false);
    let colorAlerta = ref('');

    const store = usuarioStore();
    const router = useRouter();

function autenticado() {
  return store.estaLogeado
}

    const cerrarSesion = async() => {
      store.cerrarSesion();
    }

    const callback = async(respuestaGoogle) => {
      const info_usuario = decodeCredential(respuestaGoogle.credential);
      const usuario = {
      correo: info_usuario.email,
        nombre: info_usuario.given_name,
        apellido: info_usuario.family_name
      }
      let respuesta = await store.registroGoogle(usuario)
      if(respuesta.error){
        mostrarAlerta.value = true;
        colorAlerta.value = "error"
        mensajes.value = respuesta.mensajes;
      }else{
        mostrarAlerta.value = true;
        colorAlerta.value = "exito"
        mensajes.value[0] = respuesta.mensajes[0]+`. Se lo redireccionará al inicio de sesion en 4 segundos...`;;
        setTimeout(()=> {
          mostrarAlerta.value = false;
          router.push('/iniciar_sesion')}, 4000);
      }
    }

</script>

<template>
    <Alerta v-if="mostrarError" :mensaje="msg" tipoAlerta="error"></Alerta>
    <form actions class="form" @submit.prevent="iniciarSesion">
        <div class="mb-6">
            <label for="correo" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Correo:</label>
            <input v-model="correo" type="email" name="correo" id="correo" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="tucorreo@correo.com" required>
        </div>
        <div class="mb-6">
            <label for="contrasenia" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Contraseña:</label>
            <input v-model="contrasenia" type="password" name="contrasenia" id="contrasenia" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required>
        </div>
        <div class="flex justify-start">
            <button type="submit" value="iniciarSesion" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Iniciar Sesion</button>
            <div class="w-full sm:w-auto px-2">
                <GoogleLogin :callback="iniciarSesionGoogle"/>
            </div>
        </div>
    </form>
</template>

<script setup> 
    import Alerta from '../components/Alerta.vue'
    import { usuarioStore } from '../stores/auth'
    import { useRouter } from 'vue-router'
    import { decodeCredential } from 'vue3-google-login';
    import { ref } from 'vue'

    let msg = ref('');
    let mostrarError = ref(false);

    const router = useRouter();
    const store = usuarioStore();
    
    const iniciarSesion = async() => {
        const usuario = {        
            user: correo.value,
            password: contrasenia.value
        };
        let statusCode = await store.iniciarSesion(usuario);
        switch(statusCode){
            case 401:
                msg.value = "Correo electronico o contraseña incorrecta";
                mostrarError.value=true;
                break;
            case 403:
                msg.value = "Usted ha sido bloqueado. Hable con el administrador";
                mostrarError.value=true;
                break;
            case 406:
                msg.value = "Debe iniciar sesion con google";
                mostrarError.value=true;
                break;
        default:
            router.push('/');
            break;
        }
    }

    const iniciarSesionGoogle = async(respuestaGoogle) => {

        const info_usuario = decodeCredential(respuestaGoogle.credential);
        const usuario = {
            correo: info_usuario.email,
            nombre: info_usuario.given_name,
            apellido: info_usuario.family_name
        }
      let respuesta = await store.iniciarSesionGoogle(usuario)
      if (respuesta.error){
        msg.value = respuesta.mensaje;
        mostrarError.value=true;
      }else{
        if(respuesta.rellenar_formulario){
            router.push('/completar-datos')
        }else{
            router.push('/');
        }
      }
    }
</script>
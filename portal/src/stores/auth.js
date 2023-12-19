import { defineStore } from 'pinia'
import configApi from '../services/Api';
import { useStorage } from '@vueuse/core'

export const usuarioStore = defineStore({
    id: "usuarioStore",
    state: () => ({
        token: useStorage('token', ''),
        usuario: useStorage('usuario', {}),
        estaLogeado: useStorage('estaLogeado', false)
    }),
    getter: {
        getToken: (state) => state.token,
        getUsuario: (state) => state.usuario,
        getEstaLogeado: (state) => state.estaLogeado
    },
    actions: {
        setData(usuario, token){
            this.usuario = usuario;
            this.token = token;
            this.estaLogeado = true;
        },
        cerrarSesionEstado(){
            this.token = '';
            this.usuario = {};
            this.estaLogeado = false;
        },
        async iniciarSesion(usuario){
            try{
                const respuesta = await configApi.post('/auth', usuario);
                this.setearUsuario(respuesta.data.token);
                return respuesta;
            }catch(error){
                return error.response.status;
            }
        },
        async setearUsuario(token){
            const respuesta = await configApi.get('/me/profile', { headers: {'Authorization': `Bearer ${token}`}});
            this.setData(respuesta.data, token)
        },
        async cerrarSesion(){
            this.cerrarSesionEstado();
        },
        async registroCorreo(usuario){
            try{
                const respuesta = await configApi.post('/registro-correo', usuario);
                return respuesta.data;
            }catch(error){
                return error.response.data;
            }
        },
        async registroGoogle(usuario){
            try{
                const respuesta = await configApi.post('/registro-google', usuario);
                return respuesta.data;
            }catch(error){
                return error.response.data;
            }
        },
        async iniciarSesionGoogle(usuario){
            try{
                const respuesta = await configApi.post('/auth-google', usuario);
                this.setearUsuario(respuesta.data.token);
                return respuesta.data;
            }catch(error){
                return error.response.data;
            }
        },
        async completarDatos(datos_usuario){
            try{
                const respuesta = await configApi.post('/completar-datos', datos_usuario);
                return respuesta.data;
            }catch(error){
                return error.response.data;
            }
        }
    }
});
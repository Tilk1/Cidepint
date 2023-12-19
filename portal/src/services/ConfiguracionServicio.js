import configApi from '../services/Api';

class ConfiguracionServicio{

    async obtenerInfoContacto(){
        try{
            const respuesta = await configApi.get('/info-contacto');
            return respuesta.data;
        }catch(error){
            return error.response;
        }

    }
}

export default ConfiguracionServicio;
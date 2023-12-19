import axios from 'axios';

class ServicioClase {
  constructor() {
    if (import.meta.env.MODE === 'development') {
      this.URI = 'http://127.0.0.1:5000/api/'
    } else {
      this.URI = 'https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/api/'
    }
  }
  
    listarServicios(page=1,per_page=5) {
      return axios.get(this.URI+='services/all_services?page='+page+'&per_page='+per_page)
        .then(response => {
          return response.data;
        })
        .catch(error => {
          console.error('Error al obtener datos de la API:', error);
          throw error; 
        });
    }
    
    buscarServicio(id) {
      return axios.get(this.URI+='services/'+id)
        .then(response => {
          return response.data;
        })
        .catch(error => {
          console.error('Error al obtener datos de la API:', error);
          throw error; 
        });
    }
    buscarInstitucion(nombre) {
      return axios.get(this.URI+='institutions/'+nombre)
        .then(response => {
          return response.data;
        })
        .catch(error => {
          console.error('Error al obtener datos de la API:', error);
          throw error; 
        });
    }
    obtenerCoordenadas(direccion){
      return axios.get(this.URI+='institutions/geocoding/'+direccion)
      .then(response => {
        return response.data;
      })
      .catch(error => {
        console.error('Error al obtener datos de la API:', error);
        throw error; 
      });
    } 

    
    buscarServicios(param, page = 1, per_page=5) {
      let servicio = {
        service_name: param['nombre'],
        service_description: param['descripcion'],
        institution_name: param['institucion'],
        tag: param['palabras_claves'],
        type: param['tipo'],
      };
    
      // Convierte el objeto servicio en una cadena de parámetros de consulta
      let params = new URLSearchParams(servicio);
      params.append('page', page);
      params.append('per_page', per_page);
    
      return axios.get(this.URI + 'services/searcher?' + params)
        .then(response => {
          return response.data;
        })
        .catch(error => {
          console.error('Error al obtener datos de la API:', error);
          throw error;
        });
    }
    
}
  export default ServicioClase;

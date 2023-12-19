import axios from 'axios'

class ServicioClase {
  constructor() {
    if (import.meta.env.MODE === 'development') {
      this.URI = 'http://127.0.0.1:5000/api/'
    } else {
      this.URI = 'https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/api/'
    }
  }

  getServicio(id) {
    return axios
      .get(`${this.URI}services/${id}`)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        console.error('Error al obtener datos de la API:', error)
        throw error
      })
  }

  postSolicitudServicio(id_servicio, titulo, detalle, token) {
    return axios
      .post(
        `${this.URI}me/requests`,
        {
          titulo: titulo,
          descripcion: detalle,
          servicio: id_servicio
        },
        {
          headers: {'Authorization': `Bearer ${token}`}
        }
      )
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        console.error('Error al obtener datos de la API:', error)
        throw error
      })
  }
}

export default ServicioClase

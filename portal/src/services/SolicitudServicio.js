import axios from 'axios'

class ClaseSolicitud {
  constructor() {
    if (import.meta.env.MODE === 'development') {
      this.URI = 'http://127.0.0.1:5000/api/'
    } else {
      this.URI = 'https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/api/'
    }
  }

  getDetalleSolicitud(id_solicitud, token) {
    return axios
      .get((this.URI += `me/requests/${id_solicitud}`), {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        console.error('Error al obtener datos de la API:', error)
        throw error
      })
  }

  getNotas(id_solicitud) {
    return axios
      .get((this.URI += `requests/${id_solicitud}/get_notes`))
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        console.error('Error al obtener datos de la API:', error)
        throw error
      })
  }

  postNota(nota, token, id_solicitud) {
    return axios
      .post(
        (this.URI += `me/requests/${id_solicitud}/notes`),
        {
          nota: nota
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
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

export default ClaseSolicitud

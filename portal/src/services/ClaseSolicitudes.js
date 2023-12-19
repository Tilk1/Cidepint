import axios from 'axios';

class ServicioSolicitudClase {
  constructor() {
    if (import.meta.env.MODE === 'development') {
      this.URI = 'http://127.0.0.1:5000/api/';
    } else {
      this.URI = 'https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/api/';
    }
  }

  async getSolicitudes(paginaActual, token, orden, filtro) {
    const maxRetries = 2;

    for (let retry = 0; retry <= maxRetries; retry++) {
      try {
        const response = await axios.get(`${this.URI}me/requests`, {
          params: {
            page: paginaActual,
            order: orden,
            sort: filtro
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        return response.data;
      } catch (error) {
        console.error(`Error al obtener datos de la API (Intento ${retry + 1}):`, error);

        if (retry < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, 2000));
        } else {
          throw error;
        }
      }
    }
  }
}

export default ServicioSolicitudClase;

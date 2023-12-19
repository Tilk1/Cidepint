import axios from 'axios';

class ServicioEstadisticasClase {
  constructor() {
    if (import.meta.env.MODE === 'development') {
      this.URI = 'http://127.0.0.1:5000/api/';
    } else {
      this.URI = 'https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/api/';
    }
  }

  async requestWithRetry(endpoint) {
    const maxRetries = 2;

    for (let retry = 0; retry <= maxRetries; retry++) {
      try {
        const response = await axios.get(`${this.URI}${endpoint}`);
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

  getSolicitudesPorEstado() {
    return this.requestWithRetry('/statistics/requests/by_state');
  }

  getServiciosMasSolicitados() {
    return this.requestWithRetry('/statistics/services/most_requested');
  }

  getInstitucionesMejorTiempoResolucion() {
    return this.requestWithRetry('/statistics/institutions/best_resolution_time');
  }
}

export default ServicioEstadisticasClase;

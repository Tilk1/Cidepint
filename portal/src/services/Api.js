import axios from 'axios';

class ServicioApi {
    constructor() {
        if (import.meta.env.MODE === "development")
            this.UrlBase = 'http://127.0.0.1:5000/api/';
        else
            this.UrlBase = 'https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/api/';

        this.configApi = axios.create({
            baseURL: this.UrlBase,
            withCredentials: true,
            xsrfCookieName: 'csrf_access_token',
        });
    }
}

export default new ServicioApi().configApi;

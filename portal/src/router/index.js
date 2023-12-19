import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ServiciosView from '../views/ServiciosView.vue'
import EstadisticasView from '../views/EstadisticasView.vue'
import SolicitudView from '../views/SolicitudView.vue'
import BuscadorServiciosView from '../views/BuscadorServiciosView.vue'
import DetalleSolicitudView from '../views/DetalleSolicitudView.vue'
import IniciarSesionView from '../views/IniciarSesionView.vue'
import RegistrarseCorreoView from '../views/RegistrarseCorreoView.vue'
import { usuarioStore } from '../stores/auth'
import DetalleServicioView from '../views/DetalleServicioView.vue'
import TablaDeServiciosView from '../views/TablaDeServiciosView.vue'
import MisSolicitudesView from '../views/MisSolicitudesView.vue'
import CompletarDatosView from '../views/CompletarDatosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/servicios',
      name: 'ServiciosView',
      component: ServiciosView,
    },
    {
      path: '/estadisticas',
      name: 'EstadisticasView',
      component: EstadisticasView,
    },
    {
      path: '/nueva_solicitud/:id_servicio',
      name: 'SolicitudView',
      component: SolicitudView,
      beforeEnter: ()=>{
        const store = usuarioStore();
        return store.estaLogeado;
      }
    },
    {
      path: '/iniciar_sesion',
      name: 'IniciarSesionView',
      component: IniciarSesionView
    },
    {
      path: '/registrarse-correo',
      name: 'RegistrarseCorreoView',
      component: RegistrarseCorreoView
    },
    {
      path: '/buscador_servicios',
      name: 'BuscadorServiciosView',
      component: BuscadorServiciosView,
    },
    {
      path: '/solicitud_servicio/:id_solicitud',
      name: 'DetalleSolicitudView',
      component: DetalleSolicitudView,
    },
    {
      path: '/detalle_servicio/:id',
      name: 'DetalleServicioView',
      component: DetalleServicioView,
    },
    {
      path: '/tabla_servicios/:serviciosEncontrados,/:servicioBuscado',
      name: 'TablaDeServiciosView',
      component: TablaDeServiciosView,
    },
    {
      path: '/mis_solicitudes',
      name: 'MisSolicitudesView',
      component: MisSolicitudesView,
      beforeEnter: ()=>{
        const store = usuarioStore();
        return store.estaLogeado;
      }
    },
    {
      path: '/completar-datos',
      name: 'CompletarDatosView',
      component: CompletarDatosView,
    },
  ]
})

export default router


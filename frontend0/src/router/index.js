import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Electores from '../views/Electores.vue'
import Candidatos from '../views/Candidatos.vue'
import Cedulas from '../views/Cedulas.vue'
import Partidos from '../views/Partidos.vue'
import Elecciones from '../views/Elecciones.vue'
import Ubigeo from '../views/Ubigeo.vue'
import Voto from '../views/Voto.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/electores',
    name: 'Electores',
    component: Electores
 },
  {
    path: '/candidatos',
    name: 'Candidatos',
    component: Candidatos
  },
  {
    path: '/cedulas',
    name: 'Cedulas',
    component: Cedulas
  },
  {
    path: '/partidos',
    name: 'Partidos',
    component: Partidos
  },
  {
    path: '/elecciones',
    name: 'Elecciones',
    component: Elecciones
  },
  {
    path: '/ubigeo',
    name: 'Ubigeo',
    component: Ubigeo
  },
  {
    path: '/voto',
    name: 'Voto',
    component: Voto
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

import { createRouter, createWebHistory } from 'vue-router'

import TravelView from '../views/TravelView.vue'
import GraphView from '../views/GraphView.vue'
import RecentsView from '../views/RecentsView.vue'
import SavedView from '../views/SavedView.vue'

const routes = [
  { path: '/', redirect: '/travel' },
  { path: '/travel', component: TravelView },
  { path: '/graph', component: GraphView },
  { path: '/recents', component: RecentsView },
  { path: '/saved', component: SavedView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
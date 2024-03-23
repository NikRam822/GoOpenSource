import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from "@/pages/WelcomePage.vue"
import SearchPage from "@/pages/SearchPage.vue"

const routes = [
    { path: '/', component: WelcomePage },
    { path: '/search', component: SearchPage }
]

const router = createRouter({
  routes,
  history: createWebHistory('/'), 
})

export default router
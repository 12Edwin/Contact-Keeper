import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';
import Login from '@/modules/login/views/Login.vue';
import Dashboard from "@/modules/events/views/admin/Dashboard.vue"
import UserPanel from "@/modules/events/views/user/UserPanel.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/user-panel',
    name: 'userPanel',
    component: UserPanel
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }

]

const router = new VueRouter({
  routes
})

export default router

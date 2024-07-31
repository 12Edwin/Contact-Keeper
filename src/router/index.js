import Vue from 'vue';
import VueRouter from 'vue-router';
import privateRoutes from "@/router/private-routes";
import publicRoutes from "@/router/public-routes";
Vue.use(VueRouter);

const routes = [
    {
        path:'',
        redirect:'/'
    },
    {
        path:'/',
        component: {
            render(c) { return c('router-view') }
        },
        children: [
            ...privateRoutes.map(route => {
                route.meta.requiresAuth = false;
                return {...route};
            }),
            ...publicRoutes.map(route => {
                route.meta.requiresAuth = false;
                return {...route};
            })

        ]
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
import adminRoutes from "@/router/admin-routes";
export default [
    {
        path: '',
        component: () => import('@/layouts/MainLayout.vue'),
        meta:{
            requireAuth: false
        },
        children: [
            ...adminRoutes.map(route => {
                route.meta.requireAuth = false
                return {...route}
            }),
        ]
    }
]
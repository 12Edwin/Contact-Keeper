import adminRoutes from "@/router/admin-routes";
export default [
    {
        path: '',
        component: () => import('@/layouts/MainLayout.vue'),
        meta:{
            requireAuth: true
        },
        children: [
            ...adminRoutes.map(route => {
                route.meta.requireAuth = true
                return {...route}
            }),
        ]
    }
]
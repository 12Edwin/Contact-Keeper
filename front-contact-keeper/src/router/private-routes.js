import adminRoutes from "@/router/admin-routes";
import Profile from '@/modules/users/views/Profile.vue'
export default [
    {
        path: '',
        component: () => import('@/layouts/MainLayout.vue'),
        meta:{},
        children: [
            ...adminRoutes.map(route => {
                route.meta.requireAuth = false
                return {...route}
            }),
            {
                path: '/profile',
                name: 'perfil',
                component: Profile,
                meta:{
                    title: 'Perfil'
                }
            }
        ]
    }
]
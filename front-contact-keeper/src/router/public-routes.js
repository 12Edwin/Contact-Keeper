import Login from "@/modules/login/views/Login.vue";
export default [
    {
        path: '',
        component: () => import ("@/layouts/PublicLayout.vue"),
        meta:{
        },
        children:[
            {
                path: '',
                name: 'login',
                component: Login,
                meta: {
                    title: 'Login'
                }
            }
        ]
    }
]
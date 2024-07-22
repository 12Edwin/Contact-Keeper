import Users from "@/modules/events/views/admin/Users.vue";
import Events from "@/modules/events/views/user/Events.vue";

export default [
    {
        path: 'users',
        name: 'users',
        meta: {

        },
        component: {
            render(c){
                return c("router-view")
            }
        },
        children: [
            {
                path: '',
                name: 'users',
                component: Users,
                meta: {
                    title: 'Usuarios',
                    role: 'admin'
                }
            }
        ]
    },
    {
        path: 'events',
        name: 'events',
        component: Events,
        meta: {
            title: 'Eventos'
        }
    }

]
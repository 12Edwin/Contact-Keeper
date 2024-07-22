import Users from "@/modules/events/views/Users.vue";
import Events from "@/modules/events/views/Events.vue";
import Calendar from "@/modules/events/views/Calendar.vue"
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
        path: 'calendar',
        name: 'calendar',
        component: Calendar,
        meta: {
            title: 'Calendario',
        }
    }
]
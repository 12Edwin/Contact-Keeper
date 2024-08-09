import Users from "@/modules/users/views/Users.vue";
import Events from "@/modules/events/views/Events.vue";
import Calendar from "@/modules/events/views/Calendar.vue"
export default [
    {
        path: '',
        name: 'users',
        meta: {
            role: "administrators"
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
                    role: 'administrators'
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
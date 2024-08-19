import router from "@/router";
import axios from "axios";
import { onToast } from "@/kernel/alerts";
import utils from "@/kernel/utils";
const SERVER_URL = process.env.VUE_APP_BASE_URL;
const SERVER_URL_EVENT = process.env.VUE_APP_EVENTS_URL;
const VUE_APP_GROUPS_URL = process.env.VUE_APP_GROUPS_URL;
const SERVER_URL_EVENT_MANAGEMENT = process.env.VUE_APP_EVENTS_MANAGEMENT

const AxiosClient = axios.create({
    baseURL: SERVER_URL,
    timeout: 20000,
})

const EventAxiosClient = axios.create({
    baseURL: SERVER_URL_EVENT,
    timeout: 20000,
})


const EventManagementClient = axios.create({
    baseURL: SERVER_URL_EVENT_MANAGEMENT,
    timeout: 20000,
})

const GroupsAxiosClient = axios.create({
    baseURL: VUE_APP_GROUPS_URL,
    timeout: 20000,
})

export const getServerUrl = () => SERVER_URL;


const setUpInterceptors = (client) => {
    client.interceptors.request.use(
        function(config){
            const auth_token = localStorage.getItem('token')
            if(auth_token !== undefined && auth_token !== null && auth_token !== ""){
                if(!config.url.includes('auth')){
                    config.headers.Authorization = `Bearer ${auth_token}`
                }
            }
            return config
        },
        function(error){
            return Promise.reject(error)
        }
    )

    client.interceptors.response.use(
        (response) => {
            if(response.status === 200 || response.status === 201){
                return Promise.resolve(response)
            }else{
                return Promise.reject(response)
            }
        },
         (error) => {
            if(!error.response){
                onToast('Error de conexión', 'No se ha podido establecer conexión con el servidor', 'error')
                if(error.response.data.message && error.response.data.message === "The incoming token has expired"){
                    onToast('Sesión expirada', "Tiempo de sesión excedido" , 'error')
                    localStorage.removeItem('token')
                    router.push('/login')
                }
                return Promise.reject(error)
            }
            if(error.response.status){
                switch(error.response.status){
                    case 400:
                        onToast('Campo inválido',`${utils.getErrorMessages(error.response.data.message)}` , 'warning')
                        return Promise.resolve()
                    case 401:
                        onToast('No autorizado', 'No tienes permisos para realizar esta acción' , 'warning')
                        return Promise.resolve()
                    case 500:
                         onToast('Error interno','Error interno del servidor' , 'error')
                        break;
                }
                return Promise.reject(error)
            }
            return Promise.reject(error)
        }
    )
}

setUpInterceptors(AxiosClient)
setUpInterceptors(EventAxiosClient)
setUpInterceptors(GroupsAxiosClient)
setUpInterceptors(EventManagementClient)

const axiosClientApi = {
    doGet(url){
        return AxiosClient.get(url)
    },
    doPost(url, data){
        return AxiosClient.post(url, data)
    },
    doPut(url, data){
        return AxiosClient.put(url, data)
    },
    doDelete(url){
        return AxiosClient.delete(url)
    },
}

const axiosClientEvent = {
    doGet(endPoint, config){
        return EventAxiosClient.get(endPoint, config)
    },
    doPost(endPoint, object, config){
        return EventAxiosClient.post(endPoint, object, config || {});
    },
    doPut(endPoint, object, config){
        return EventAxiosClient.put(endPoint, object, config || {})
    },
    doDelete(endPoint, object, config){
        return AxiosClient.put(endPoint, object, config || {});
    },
}

const axiosClientGroups = {
    doGet(endPoint, config){
        return GroupsAxiosClient.get(endPoint, config)
    },
    doPost(endPoint, object, config){
        return GroupsAxiosClient.post(endPoint, object, config || {});
    },
    doPut(endPoint, object, config){
        return GroupsAxiosClient.put(endPoint, object, config || {})
    },
    doDelete(endPoint, object, config){
        return GroupsAxiosClient.delete(endPoint, object, config || {});
    },
}

const axiosClientEventManagement = {
    doGet(endPoint, config){
        return EventManagementClient.get(endPoint, config)
    },
    doPost(endPoint, object, config){
        return EventManagementClient.post(endPoint, object, config || {});
    },
    doPut(endPoint, object, config){
        return EventManagementClient.put(endPoint, object, config || {})
    },
    doDelete(endPoint, object, config){
        return EventManagementClient.delete(endPoint, object, config || {});
    },
}

export default {
    axiosClientApi,
    axiosClientEvent,
    axiosClientGroups,
    axiosClientEventManagement
}
import router from "@/router";
import axios from "axios";
import { onToast } from "@/kernel/alerts";
import utils from "@/kernel/utils";
const SERVER_URL = process.env.VUE_APP_BASE_URL;

const AxiosClient = axios.create({
    baseURL: SERVER_URL,
    timeout: 20000,
})

export const getServerUrl = () => SERVER_URL;

AxiosClient.interceptors.request.use(
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

AxiosClient.interceptors.response.use(
    (response) => {
        if(response.status === 200 || response.status === 201){
            return Promise.resolve(response)
        }else{
            return Promise.reject(response)
        }
    },
     (error) => {
        if(!error.response){
            console.log('Error de conexión', error)
            onToast('Error de conexión', 'No se ha podido establecer conexión con el servidor', 'error')
            return Promise.reject(error)
        }
        if(error.response.status){
            switch(error.response.status){
                case 400:
                    onToast('Campo inválido',`${utils.getErrorMessages(error.response.data.message)}` , 'warning')
                    return Promise.resolve()
                case 401:
                    console.log("Error 401")
                    return Promise.resolve()
                case 500:
                     console.log("Error 500")
                     onToast('Error interno','Error interno del servidor' , 'error')
                    break;
            }
            return Promise.reject(error)
        }
        return Promise.reject(error)
    }
)

export default {
    doGet: function (endPoint, config) {
        return AxiosClient.get(endPoint, config);
    },
    doPost: function (endPoint, object, config) {
        return AxiosClient.post(endPoint, object, config || {});
    },
    doPut: function (endPoint, object, config) {
        return AxiosClient.put(endPoint, object, config || {});
    },
    doDelete: function (endPoint) {
        return AxiosClient.delete(endPoint);
    },
};
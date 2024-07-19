import api from '@/config/http-client.gateway'

const login = async (credentials) => {
    try {
        return await api.doPost('/login', credentials)
    }catch(error){
        return error.response
    }
}

export default {
    login
}
import api from '@/config/http-client.gateway'

const login = async (credentials) => {
  try {
    const response = await api.axiosClientApi.doPost("/login", credentials);
    return response.data;
  } catch (error) {
    return error.response;
  }
};


const signUp = async (person) => {
  try {
    const response = await api.axiosClientApi.doPost("/users", person); 
    return response.data;
  } catch (error) {
    return error.response;
  }
}


const confirmAccount = async (access) => {
  try {
    const response = await api.axiosClientApi.doPost("/confirm", access);
    return response.data;
  } catch (error) {
    return error.response;
  }
}
export default {
  login,
  signUp,
  confirmAccount
}

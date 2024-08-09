import api from '@/config/http-client.gateway'

const login = async (credentials) => {
  try {
    const response = await api.doPost("/login", credentials); 
    return response.data;
  } catch (error) {
    return error.response;
  }
};

export default {
  login
}

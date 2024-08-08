import api from '@/config/http-client.gateway'

const login = async (credentials) => {
  try {
    const response = await api.doPost("https://zy2too7q94.execute-api.us-east-1.amazonaws.com/Prod/login", credentials);
    return response;
  } catch (error) {
    return error.response;
  }
};

export default {
  login
}

import api from "@/config/http-client.gateway";

const get_users = async () => {
  try {
    const response = await api.axiosClientApi.doGet("/users");
    return response.data;
  } catch (error) {
    return error.response;
  }
};

const save_user = async (person) => {
  try {
    const response = await api.axiosClientApi.doPost("/users", person);
    return response.data
  } catch (error) {
    return error.response;
  }
};

export default {
  get_users,
  save_user,
};

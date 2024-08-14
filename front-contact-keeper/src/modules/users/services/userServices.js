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
    const response = await api.doPost("/users", person,{
      headers: {
        "Content-Type": "text/plain"
      }
    });
    return response.data
  } catch (error) {
    return error.response;
  }
};

export default {
  get_users,
  save_user,
};

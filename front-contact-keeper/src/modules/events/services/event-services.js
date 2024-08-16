import api from "@/config/http-client.gateway"

const saveGroupEvent = async (dataEvent) =>{
    try {
        const response = await api.axiosClientEventManagement.doPost("/events", dataEvent);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

const saveMeetingEvent = async (dataEvent) =>{
    try {
        const response = await api.axiosClientEventManagement.doPost("/events_meet", dataEvent);
        return response.data;
    } catch (error) {
        return error.response;
    }
}


const getEvents = async (userLogged) =>{
    try {
        const response = await api.axiosClientEventManagement.doGet(`/events/person/${userLogged}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}
export default {
    saveGroupEvent,
    saveMeetingEvent,
    getEvents
}
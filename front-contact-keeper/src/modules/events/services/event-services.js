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

const deleteEvent = async (id) => {
    try {
        const response = await api.axiosClientEventManagement.doDelete(`/events/${id}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

const updateEvent = async (dataEvent) =>{
    try {
        const response = await api.axiosClientEventManagement.doPut(`events/${dataEvent.id}`,dataEvent);
        return response.data;
    } catch (error) {
        return error.response;
    }
}
export default {
    saveGroupEvent,
    saveMeetingEvent,
    getEvents,
    deleteEvent,
    updateEvent
}
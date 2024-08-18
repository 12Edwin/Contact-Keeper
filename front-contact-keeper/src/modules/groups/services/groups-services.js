import api from "@/config/http-client.gateway"
import utils from "@/kernel/utils";

export const getGroupsByUserId = async () => {
    try {
        const userId = utils.getSubFromToken();
        const response = await api.axiosClientGroups.doGet(`/groups/moderator/${userId}`); 
        console.log("response =>",response.data);
        return response.data;
    } catch (error) {
        console.log("error =>",error);
        
        return error.response;
    }
};

export const saveGroup = async (groupData) => {
    try {
        const userId = utils.getSubFromToken();
        groupData = { ...groupData, moderator: userId };   
        const response = await api.axiosClientGroups.doPost('/groups', groupData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const updateGroup = async (groupId, groupData) => {
    try {
        const response = await api.axiosClientGroups.doPut(`/groups/${groupId}`, groupData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const deleteGroup = async (groupId) => {
    try {
        const response = await api.axiosClientGroups.doDelete(`/groups/${groupId}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const getEventsbyGroup = async (groupId) => {
    try {
        const response = await api.axiosClientEventManagement.doGet(`/events/group/${groupId}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const getUsersByGroup = async (groupId) => {
    try {
        const response = await api.axiosClientGroups.doGet(`/groups/${groupId}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const assignUserToGroup = async (groupData) => {
    try {
        const response = await api.axiosClientGroups.doPost("assign_member_group", groupData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const removeUserFromGroup = async (groupData) => {
    try {
        const response = await api.axiosClientGroups.doPost(`/unassign_member_group/${groupData.member}`, groupData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const createMessage = async (messageData) => {
    try {
        const response = await api.axiosClientGroups.doPost('/message', messageData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const getUsers = async () => {
    try {
        const response = await api.axiosClientApi.doGet('/users/');
        return response.data;
    } catch (error) {
        return error.response;
    }
}



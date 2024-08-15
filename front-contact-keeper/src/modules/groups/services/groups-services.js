import api from "@/config/http-client.gateway"

// Función para decodificar el payload de un JWT
const decodeJwtPayload = (token) => {
    const base64Url = token.split('.')[1]; // Obtener el payload
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Reemplazar caracteres para Base64
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => 
        '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));

    return JSON.parse(jsonPayload);
};


export const getGroupsByUserId = async () => {
    try {
        const token = localStorage.getItem("token");
        const payload = decodeJwtPayload(token);
        const userId = payload.sub;
        const response = await api.axiosClientEvent.doGet(`/groups/moderator/${userId}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
};

export const saveGroup = async (groupData) => {
    try {
        const token = localStorage.getItem("token");
        const payload = decodeJwtPayload(token);
        const userId = payload.sub;
        groupData = { ...groupData, moderator: userId };   
        const response = await api.axiosClientEvent.doPost('/groups', groupData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const updateGroup = async (groupId, groupData) => {
    try {
        const response = await api.axiosClientEvent.doPut(`/groups/${groupId}`, groupData);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const deleteGroup = async (groupId) => {
    try {
        const response = await api.axiosClientEvent.doDelete(`/groups/${groupId}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}

export const getEventsbyGroup = async (groupId) => {
    try {
        const response = await api.axiosClientEvent.doGet(`/events/group/${groupId}`);
        return response.data;
    } catch (error) {
        return error.response;
    }
}




const groupService = {
    
    // getAllGroups() {
    //     return api.doGet('/groups/moderator');
    // },
    // getGroupById(groupId) {
    //     return api.doGet(`/groups/${groupId}`);
    // },
    // createGroup(groupData) {
    //     return api.doPost('/groups', groupData);
    // },
    // updateGroup(groupId, groupData) {
    //     return api.doPut(`/groups/${groupId}`, groupData);
    // },
    // deleteGroup(groupId) {
    //     return api.doDelete(`/groups/${groupId}`);
    // },
    // addMemberToGroup() {
    //     return api.doPost(`/assign_member_group`, groupData);
    // },
    // removeMemberFromGroup(groupId, memberId) {
    //     return api.doDelete(`/unassign_member_group/${memberId}/${groupId}`);
    // }
};

export default groupService;

import api from "@/config/http-client.gateway"
const groupService = {
    async getGroupsByUserId(userId) {
        const response = await api.axiosClientEvent.doGet(`/groups/moderator/${userId}`);
        return response.data;
    },
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
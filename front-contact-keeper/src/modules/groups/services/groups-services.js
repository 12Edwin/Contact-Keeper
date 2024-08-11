import api from "@/config/http-client.gateway";

const groupService = {
    getAllGroups() {
        return api.get('/groups/moderator');
    },
    getGroupById(groupId) {
        return api.get(`/groups/${groupId}`);
    },
    createGroup(groupData) {
        return api.post('/groups', groupData);
    },
    updateGroup(groupId, groupData) {
        return api.put(`/groups/${groupId}`, groupData);
    },
    deleteGroup(groupId) {
        return api.delete(`/groups/${groupId}`);
    },
    addMemberToGroup() {
        return api.post(`/assign_member_group`, groupData);
    },
    removeMemberFromGroup(groupId, memberId) {
        return api.delete(`/unassign_member_group/${memberId}/${groupId}`);
    }
};

export default groupService;
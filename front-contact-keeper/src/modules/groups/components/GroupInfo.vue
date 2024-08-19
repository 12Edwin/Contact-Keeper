<template>
  <Dialog
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{ width: '60vw' }"
    class="custom-dialog"
    :autoZIndex="true"
    @before-show="startLoading"
  >
    <template v-slot:header>
      <h4>{{ selectedGroup.name }}</h4>
    </template>
    
    <div class="dialog-content">
      <b-row>
        <b-col cols="12" class="mb-3">
          <div class="user-list-header">
            <h5>Título</h5>
          </div>
        </b-col>
        <b-col cols="12" class="mb-3">
          <p>{{ selectedGroup.title }}</p>
        </b-col>
        <b-col cols="12" class="mb-3">
          <div class="user-list-header">
            <h5>Descripción</h5>
          </div>
        </b-col>
        <b-col cols="12" class="mb-3">
          <p>{{ selectedGroup.description }}</p>
        </b-col>
        <b-col cols="12" class="mb-3">
          <div class="user-list-header">
            <h5>Notas</h5>
          </div>
        </b-col>
        <b-col cols="12" class="mb-3">
          <p>{{ selectedGroup.notes }}</p>
        </b-col>
      </b-row>

      <b-col cols="12" class="mb-3">
        <div class="user-list-header">
          <h5>Integrantes</h5>
        </div>
      </b-col>

      <b-col v-if="showSkeleton" cols="12" class="mb-3">
        <div class="skeleton-class"></div>
      </b-col>

      <b-col v-if="!showSkeleton && users.length === 0" cols="12" class="mb-3">
        <div class="user-list text-center">
          <img src="@/assets/User_empty.svg" alt="No hay integrantes" class="no-users-image"/>
          <p>No hay integrantes en este grupo</p>
        </div>
      </b-col>

      <b-col v-if="!showSkeleton && users.length > 0" cols="12" class="mb-3">
        <div v-for="user in users" :key="user.id" class="user-list">
          <div class="user-info-container">
            <b-col cols="6">
              <div class="user-zone">
                {{ user.name }} {{ user.surname }} {{ user.last_name }}
              </div>
            </b-col>
            <b-col cols="6" v-if="groupRole === 'moderator'">
              <div class="icon-container d-flex justify-content-end">
                <i
                  v-if="isUserInGroup(user.id)"
                  class="pi pi-trash icon-remove"
                  v-tooltip.top="'Eliminar'"
                  @click="removeUserFromGroup(user.id)"
                  :class="{ 'icon-disabled': loadingUserId === user.id }"
                ></i>
                <i
                  v-else
                  class="pi pi-plus icon-add"
                  v-tooltip.top="'Agregar'"
                  @click="addUserToGroup(user.id)"
                  :class="{ 'icon-disabled': loadingUserId === user.id }"
                ></i>
              </div>
            </b-col>
          </div>
        </div>
      </b-col>
    </div>

    <template #footer>
      <Button v-if="groupRole === 'moderator'" label="Guardar" icon="pi pi-check" iconPos="right" class="button-options" @click="saveModal()"/>
      <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-text p-button-plain" iconPos="right" @click="closeModal()"/>
    </template>
  </Dialog>
</template>

<script>
import Tooltip from 'primevue/tooltip';
import { getUsers, getUsersByGroup, assignUserToGroup, removeUserFromGroup } from '../services/groups-services';
import { onQuestion, onToast } from '@/kernel/alerts';
import utils from '@/kernel/utils';

export default {
  name: 'GroupInfo',
  directives: {
    'tooltip': Tooltip
  },
  props: {
    visible: {
      type: Boolean,
    },
    group: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedGroup: {
        name: '',
        description: '',
        title: '',
        status: '',
        notes: '',
      },
      isLoading: true,
      showSkeleton: true,
      users: [],
      groupUsers: [],
      skeletonTimeout: null,
      loadingUserId: null, 
      userRole: '',
      groupRole: ''
    }
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
      this.showSkeleton = true;
      clearTimeout(this.skeletonTimeout);
    },
    saveModal() {
      this.$emit('update-data');
      this.$emit('update:visible', false);
      this.showSkeleton = true;
      clearTimeout(this.skeletonTimeout);
    },
    async startLoading() {
      this.users = [];
      this.groupUsers = [];
      let user = utils.getRoleStorage();
      this.userRole = user;

      if (this.groupRole === 'moderator') {
        await this.getAllUsers();
      } else {
        await this.getUserGroup();
      }

      this.showSkeleton = false; 
    },
    async getAllUsers() {
      try {
        const response = await getUsers();
        this.users = response.data;
        await this.getUsersGroup();
      } catch (error) {
      }
    },
    async getUserGroup() {
      onToast('info', 'Cargando integrantes del grupo', 'info');
      try {
        const response = await getUsersByGroup(this.selectedGroup.id);
        this.groupUsers = response.data;

        if (this.groupRole !== 'moderator') {
          this.users = this.groupUsers.people;
        }

        this.isLoading = false;
      } catch (error) {
      }
    },
    isUserInGroup(userId) {
      return this.groupUsers.people.some(user => user.id === userId);
    },
    async addUserToGroup(userId) {
      let question = await onQuestion('¿Estás seguro de agregar a este integrante al grupo?');
      if (question === true) {
        onToast('info', 'Agregando integrante al grupo', 'info');
        try {
          this.loadingUserId = userId; 
          let newUserByGroup = {
            title: this.selectedGroup.title,
            notes: "Haz sido agregado al grupo",
            member: userId,
            group_id: this.selectedGroup.id
          }
          let response = await assignUserToGroup(newUserByGroup);
          if (response.status === 200 || response.status === 201 || response.status === "success") {
            onToast('success', 'Integrante agregado correctamente', 'success');
          }
          await this.getUserGroup();
        } catch (error) {
        } finally {
          this.loadingUserId = null; 
        }
      }
    },
    async removeUserFromGroup(userId) {
      let question = await onQuestion('¿Estás seguro de eliminar a este integrante del grupo?');
      if (question === true) {
        onToast('info', 'Eliminando integrante del grupo', 'info');
        try {
          this.loadingUserId = userId; 
          let deleteUserByGroup = {
            title: this.selectedGroup.title,
            notes: "Haz sido eliminado del grupo",
            member: userId,
            group_id: this.selectedGroup.id
          }
          let response = await removeUserFromGroup(deleteUserByGroup);
          if (response.status === 200 || response.status === 201 || response.status === "success") {
            onToast('success', 'Integrante eliminado correctamente', 'success');
          }
          await this.getUserGroup();
        } catch (error) {
        } finally {
          this.loadingUserId = null; 
        }
      }
    }
  },
  watch: {
    group: {
      handler(val) {
        if (val && Object.keys(val).length > 0) {
          this.groupRole = val.role;
          this.selectedGroup = val;
          this.getUserGroup();
        }
      },
      immediate: true
    },
    visible(newValue) {
      if (newValue) {
        this.startLoading();
      }
    }
  }
}
</script>


<style lang="scss" scoped>
@import '@/styles/colors';

.custom-dialog .p-dialog-content {
  max-height: 60vh;
  overflow-y: auto;
}

.info-group {
  text-align: center;
  padding: 1rem;
}

.user-list-header {
  padding: 0.2rem;
  border-bottom: solid 1px #dddddd;
}

.user-list {
  border-bottom: solid 1px #dddddd;
  display: flex;
  align-items: center;
  padding: 0.2rem;
  width: 100%;
}

.user-info-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.username {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.role {
  margin: 0;
  font-size: 13px;
  color: #555;
}

.icon-container {
  background: transparent;
  margin-right: 15px;
}

.button-add, .button-remove {
  color: $sidebar-items; 
  background-color: $white-color; 
  border-color: $white-color;
  border: 1px solid $white-color; 
}

.button-add:hover, .button-remove:hover {
  background-color: $white-color; 
  border-color: $white-color;
  color: $sidebar-items; 
  box-shadow: none; 
}

.pi-trash, .pi-plus {
  font-size: 16px; 
  color: $sidebar-items; 
}

.button-add:disabled, .button-remove:disabled {
  cursor: not-allowed; 
  opacity: 0.6; 
}

.pi-minus-circle, .pi-plus-circle {
  font-size: 16px;
  cursor: pointer;
}

.skeleton-class {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  height: 20px;
  border-radius: 4px;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
.button-options {
  background: $primary-color;
  color: white;
  border: none;
  border-radius: 5px;
}

.button-options:hover {
  border-radius: 5px;
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
  background: $primary-color !important;
  border: none;
  cursor: pointer;
}
</style>

<template>
  <div class="main-content">
    <div class="content">
      <Panel header="Usuarios" class="shadow-lg">
        <div class="p-1">
          <div>
            <b-row>
              <b-col class="d-flex justify-content-between align-content-between mb-3">
                <span class="p-input-icon-right">
                  <i class="pi pi-search custom" @click="changeSearch()" />
                  <InputText type="text" :placeholder="searchBy()" />
                </span>
                <Button class="button-options" label="Nuevo usuario" iconPos="right" icon="pi pi-user-plus"
                  @click="openSaveModal" />
              </b-col>
            </b-row>
          </div>
          <div>
            <DataTable class="custom-datatable" :value="users" selectionMode="single" @row-select="onUserSelect">
              <Column :headerStyle="config" class="ctm-name" :field="formatName" header="Nombre" />
              <Column :headerStyle="config" field="phone" header="Numero de Telefono" />
              <Column :headerStyle="config" field="email" header="Correo Electronico" />
            </DataTable>
          </div>
          <div class="content">
            <UsersSkeleton v-if="isLoading"/>
          </div>
        </div>
      </Panel>
    </div>
    <ModalUserInfo :user="selectedUser" :visible.sync="displayModal" />
    <ModalSaveUser :visible.sync="displaySaveModal" @getUsers="getUsers" />
  </div>
</template>

<script>
import Panel from 'primevue/panel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ModalUserInfo from "@/modules/users/components/ModalUserInfo.vue";
import ModalSaveUser from "@/modules/users/components/ModalSaveUser.vue";
import services from '../services/userServices';
import UsersSkeleton from '@/components/UsersSkeleton.vue';
export default {
  name: 'Events',
  components: {
    Panel,
    DataTable,
    Column,
    ModalUserInfo,
    UsersSkeleton,
    ModalSaveUser
  },
  data() {
    return {
      sidebarVisible: false,
      users: [],
      selectedUser: null,
      config: {
        background: '#333',
        color: 'white',
        justifyContent: 'center',
        alignItems: 'center'
      },
      displayModal: false,
      displaySaveModal: false,
      searchByName: true,
      optionSelected: null,
      isLoading: false
    }
  },
  methods: {
    onUserSelect(event) {
      this.displayModal = true
      if (event.data) {
        this.selectedUser = event.data
      }
    },
    changeSearch() {
      this.searchByName = !this.searchByName
    },
    searchBy() {
      return this.searchByName ? 'Buscar por nombre...' : 'Buscar por correo..'
    },
    openSaveModal() {
      this.displaySaveModal = true
    },
    async getUsers() {
      this.isLoading = true;
      const { data, status } = await services.get_users()
      if (status === "success") {
        this.users = data;
        
      } else {
        onError('Error', 'Ha ocurrido un error inesperado').then(() => { })
      }
      this.isLoading = false
    },
    formatName(users) {
      return `${users.name} ${users.surname}`;
    }
  },
  mounted() {
    this.getUsers()
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/colors';

.user-management {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 2rem;
  margin-left: 0;
  transition: margin-left 0.3s;
}

.content.sidebar-open {
  margin-left: 250px;
  /* Ajusta este valor al ancho de tu sidebar */
}


.content {
  flex: 1;
  padding: 1rem;
  margin-left: 0;
  transition: margin-left 0.3s;
}


.cd-user-info {
  margin-top: 86px;
}

.ctm-name {
  background-color: $primary-color;
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

.custom:hover {
  cursor: pointer;
}
</style>
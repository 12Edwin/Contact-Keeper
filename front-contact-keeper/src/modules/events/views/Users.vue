<template>
  <div class="main-content">
    <div class="content">
      <Panel header="Usuarios" class="shadow-lg">
        <div class="p-1">
          <div>
            <b-row>
              <b-col class="d-flex justify-content-between align-content-between mb-3">
                <span class="p-input-icon-right">
                  <i class="pi pi-search" />
                  <InputText type="text"  placeholder="Buscar..." />
                </span>
                <Button
                  class="button-options"
                  label="Nuevo usuario"
                  iconPos="right"
                  icon="pi pi-user-plus"
                  @click="openSaveModal"
                />
              </b-col>
            </b-row>
          </div>
          <div>
            <DataTable class="custom-datatable" :value="users" selectionMode="single" @row-select="onUserSelect">
              <Column :headerStyle="config" class="ctm-name" field="name" header="Nombre" />
              <Column :headerStyle="config" field="role" header="Rol" />
              <Column :headerStyle="config" field="email" header="Email" />
            </DataTable>
          </div>
        </div>
      </Panel>
    </div>
    <ModalUserInfo :user="selectedUser" :visible.sync="displayModal"/>
    <ModalSaveUser :visible.sync="displaySaveModal"/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import SidebarAdmin from "@/components/SidebarAdmin.vue"
import Panel from 'primevue/panel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ModalUserInfo from "@/modules/events/components/ModalUserInfo.vue";
import ModalSaveUser from "@/modules/events/components/ModalSaveUser.vue";
export default {
  name: 'Events',
  components: {
    Navbar,
    SidebarAdmin,
    Panel,
    DataTable,
    Column,
    ModalUserInfo,
    ModalSaveUser
  },
  data() {
    return {
      sidebarVisible: false,
      users: [
        { name: 'Raúl Domínguez', role: 'Anfitrión', email: '20213tn103@utez.edu.mx' },
        { name: 'Edwin Barragán', role: 'Invitado', email: '20213tn046@utez.edu.mx' },
        { name: 'Carlos González', role: 'Invitado', email: '20203tn103@utez.edu.mx' },
        { name: 'Noé Mérida', role: 'Invitado', email: '20213tn056@utez.edu.mx' },
        { name: 'Yahir Degante', role: 'Anfitrión', email: '20213tn103@utez.edu.mx' }
      ],
      selectedUser: null,
      config: {
        background: '#333',
        color: 'white',
        justifyContent: 'center',
        alignItems: 'center'
      },
      displayModal: false,
      displaySaveModal: false
    }
  },
  methods: {
    onUserSelect(event) {
      this.displayModal = true
      if(event.data){
        this.selectedUser = event.data
      }
    },
    openSaveModal(){
      this.displaySaveModal = true
    },
    hideUserInfo() {
      this.selectedUser = null
    },
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible
    },
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
  margin-left: 250px; /* Ajusta este valor al ancho de tu sidebar */
}

.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

 .main-content {
   display: flex;
   flex: 2;
 }

.content {
  flex: 1;
  padding: 1rem;
  transition: margin-left 0.3s;
}

.content.sidebar-open {
  margin-left: 200px; 
}

.cd-user-info{
  margin-top: 86px;
}

.ctm-name{
  background-color: $primary-color;
}

 .button-options {
    background: $primary-color;
    color: white;
    border: none;
    border-radius: 5px;
 }

 .button-options:hover{
   border-radius: 5px;
   transform: translateY(-5px);
   box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
   background: $primary-color !important;
   border: none;
   cursor: pointer;
 }

</style>
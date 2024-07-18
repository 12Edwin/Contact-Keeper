<template>
  <div class="main-content">
    <Navbar @toggle-sidebar="toggleSidebar" />
    <SidebarAdmin :visible="sidebarVisible" @update:visible="sidebarVisible = $event" />
    <div class="content">
      <Panel header="Usuarios">
        <DataTable class="custom-datatable" :value="users" selectionMode="single" @row-select="onUserSelect">
          <Column :headerStyle="config" class="ctm-name" field="name" header="Nombre" />
          <Column :headerStyle="config" field="role" header="Rol" />
          <Column :headerStyle="config" field="email" header="Email" />
        </DataTable>
      </Panel>
    </div>
    <ModalUserInfo :user="selectedUser" :visible.sync="displayModal"/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import SidebarAdmin from "@/components/SidebarAdmin.vue"
import Panel from 'primevue/panel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ModalUserInfo from "@/modules/events/components/ModalUserInfo.vue";
export default {
  name: 'Dashboard',
  components: {
    Navbar,
    SidebarAdmin,
    Panel,
    DataTable,
    Column,
    ModalUserInfo
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
      },
      displayModal: false
    }
  },
  methods: {
    onUserSelect(event) {
      this.displayModal = true
      this.selectedUser = event.data
    },
    hideUserInfo() {
      this.selectedUser = null
    },
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible
    },
    openModal(service) {

    }
  }
}
</script>

<style scoped lang="scss">
 @import '@/styles/colors.scss';

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
  margin-top: 70px;
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

</style>
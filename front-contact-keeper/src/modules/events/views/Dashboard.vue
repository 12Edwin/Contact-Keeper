<template>
  <div class="dashboard">
    <Navbar @toggle-sidebar="toggleSidebar" />
    <SidebarAdmin :visible="sidebarVisible" @update:visible="sidebarVisible = $event" />
    <div class="main-content">
      <div class="content">
        <Panel header="Usuarios">
          <DataTable class="custom-datatable":value="users" selectionMode="single" @row-select="onUserSelect">
            <Column class="ctm-name" field="name" header="Nombre" />
            <Column field="role" header="Rol" />
            <Column field="email" header="Email" />
          </DataTable>
        </Panel>
      </div>
      <UserInfo class="cd-user-info" :user="selectedUser" v-if="selectedUser" />
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import SidebarAdmin from "@/components/SidebarAdmin.vue"
import UserInfo from '../components/UserInfo.vue'
import Panel from 'primevue/panel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

export default {
  name: 'Dashboard',
  components: {
    Navbar,
    SidebarAdmin,
    Panel,
    DataTable,
    Column,
    UserInfo
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
      selectedUser: null
    }
  },
  methods: {
    onUserSelect(event) {
      this.selectedUser = event.data
    },
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible
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
  flex: 1;
}

.content {
  flex: 1;
  padding: 1rem;
  transition: margin-left 0.3s;
}

.content.sidebar-open {
  margin-left: 250px; 
}

.cd-user-info{
  margin-top: 86px;
}

.ctm-name{
  background-color: $primary-color;
}

</style>
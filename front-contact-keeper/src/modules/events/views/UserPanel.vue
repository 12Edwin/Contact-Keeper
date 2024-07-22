<template>
  <div class="main-content">
    <Navbar @toggle-sidebar="toggleSidebar" />
    <SidebarUser :visible="sidebarVisible" @update:visible="sidebarVisible = $event" />
    <div class="content">
      <Panel header="Eventos">
        <div class="event-actions">
            <InputText v-model="search" placeholder="Buscar..." />
            <Button label="Agregar evento" icon="pi pi-plus" class="p-ml-2 btn_open_modal" @click="showModal = true" />
          </div>
        <DataTable :value="events">
            <Column :headerStyle="config" field="event" header="Evento" />
        </DataTable>
      </Panel>
    </div>
    <CreateEventModal v-if="showModal" @close="showModal = false" />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import SidebarUser from "@/components/SidebarUser.vue"
import Panel from 'primevue/panel'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import CreateEventModal from '@/modules/events/components/CreateEventModal.vue'
export default {
  name: 'Dashboard',
  components: {
    Navbar,
    SidebarUser,
    Panel,
    DataTable,
    Column,
    CreateEventModal
  },
  data() {
    return {
        sidebarVisible: false,
        search: '',
        showModal: false,
        events: [
          // Aquí puedes agregar eventos de ejemplo
          { event: 'Evento 1' },
          { event: 'Evento 2' }
        ],
        config: {
        background: '#333',
        color: 'white',
      },
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
  margin-left: 250px; 
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
  
  .event-actions {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
  }

  .btn_open_modal{
    background-color: $gray-color;
  }

</style>
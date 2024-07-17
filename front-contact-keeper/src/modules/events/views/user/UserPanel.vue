<template>
    <div id="UserPanel">
      <Navbar @toggle-sidebar="toggleSidebar" />
      <SidebarUser :visible="sidebarVisible" @update:visible="sidebarVisible = $event" />
      <div class="content">
        <Panel header="Eventos">
          <div class="event-actions">
            <InputText v-model="search" placeholder="Buscar..." />
            <Button label="Agregar evento" icon="pi pi-plus" class="p-ml-2" @click="showModal = true" />
          </div>
          <DataTable :value="events">
            <Column field="event" header="Evento" />
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
  import InputText from 'primevue/inputtext'
  import Button from 'primevue/button'
  import DataTable from 'primevue/datatable'
  import Column from 'primevue/column'
  import CreateEventModal from '../../components/CreateEventModal.vue'
  
  export default {
    name: 'UserPanel',
    components: {
      Navbar,
      SidebarUser,
      CreateEventModal,
      Panel,
      InputText,
      Button,
      DataTable,
      Column
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
        ]
      }
    },
    methods: {
      toggleSidebar() {
        this.sidebarVisible = !this.sidebarVisible
      }
    }
  }
  </script>
  
  <style scoped lang="scss">
   @import '@/styles/colors.scss';
  
  .content {
    flex: 1;
    padding: 2rem;
    background-color: $background-color;
    margin-top: 70px;
  }
  
  .event-actions {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
  }
  </style>
  
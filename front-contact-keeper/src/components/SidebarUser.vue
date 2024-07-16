<template>
    <Sidebar :visible="visible" @update:visible="$emit('update:visible', $event)" :baseZIndex="1000" class="custom-sidebar">
      <div class="sidebar-header">
        <Avatar label="RD" class="p-mr-2" />
        <h2>Merri Christmas</h2>
        <p>User</p>
      </div>
      <Menu :model="menuItems" />
    </Sidebar>
  </template>
  
  <script>
  export default {
    name: 'SidebarAdmin',
    props: {
      visible: {
        type: Boolean,
        required: true
      }
    },
    data() {
      return {
        menuItems: [
          { label: 'Eventos', icon: 'pi pi-fw pi-calendar' },
          { label: 'Cerrar sesión', icon: 'pi pi-fw pi-power-off' }
        ]
      }
    }
  }
  </script>
  
  <style scoped lang="scss" >
   @import '@/styles/colors.scss';

  .custom-sidebar {
    width: 250px;
    height: 100vh;
  }
  
  .sidebar-header {
    text-align: center;
    padding: 2rem;
  }
  
  .sidebar-header h2 {
    margin: 0.5rem 0 0.25rem;
  }
  
  .sidebar-header p {
    margin: 0;
    color: $subtitles;
  }
  </style>
<template>
  <Sidebar :visible="visible" @update:visible="$emit('update:visible', $event)" :baseZIndex="1000" class="custom-sidebar">
    <div class="sidebar-header p-2">
      <Avatar label="RD" class="p-mr-2 custom-avatar" />
      <div class="user-info">
        <h2 class="user-sidebar">Raúl Domínguez</h2>
        <p class="role">Administrador</p>
      </div>
    </div>
    <div class="w-100">
      <ul>
        <li class="item" v-for="(item, index) in menuItems" :key="index">
          <i :class="`${item.icon} sidebar-icon`" /> <span class="ms-3 sidebar-text">{{ item.label }}</span>
        </li>
      </ul>
    </div>
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
        {label: 'Usuarios', icon: 'pi pi-fw pi-users'},
        {label: 'Eventos', icon: 'pi pi-fw pi-calendar'},
        {label: 'Anuncios', icon: 'pi pi-fw pi-megaphone'},
        {label: 'Cerrar sesión', icon: 'pi pi-fw pi-power-off'}
      ]
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/colors.scss';

div ul {
  padding: 0;
}
.item {
  display: flex;
  align-items: center;
  text-decoration: none;
  padding-bottom: 18px;
  padding-top: 18px;
  padding-left: 15px;
  width: 100%;
  background-color: transparent;
  border-radius: 9px;
  transform: scale(1);
  transition: transform 0333.3s ease, box-shadow 0.3s ease;
  color: $subtitles;
  margin-bottom: 10px;
}
.custom-sidebar {
  width: 250px;
  height: 100vh;
}

.sidebar-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.user-sidebar {
  font-size: 16px;
  color: $sidebar-items;
  font-weight: 700;
  margin: 0;
}

.role {
  margin: 0;
  color: $subtitles;
  font-size: 13px;
}

.sidebar-icon{
  color: $sidebar-items;
  font-size: 18px;
}


.sidebar-text {
  color: $sidebar-items;
  font-size: 14px;
  font-weight: 500;
}


.item:hover {
  color: $blanco;
  border-radius: 9px;
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
  cursor: pointer;
}

.custom-avatar {
  background-color: $primary-color;
  color: $blanco;
}

</style>

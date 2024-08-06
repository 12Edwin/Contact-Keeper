<template>
  <div :class="['custom-sidebar', { closed: visible }]">
    <div class="sidebar-header">
      <div class="avatar">IP</div>
      <div class="user-info">
        <h2 class="user-sidebar">Isa Palacios</h2>
        <p class="role">Administrador</p>
      </div>
    </div>
    <div class="w-100">
      <ul>
        <li class="item" v-for="(item, index) in menuItems"
            :key="index" @click="() => $router.push({ name: item.route })"
        >
          <i :class="`${item.icon} sidebar-icon`" /> <span class="sidebar-text">{{ item.label }}</span>
        </li>
      </ul>
    </div>
  </div>
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
        {label: 'Usuarios', icon: 'pi pi-fw pi-users', route: 'users'},
        {label: 'Eventos', icon: 'pi pi-fw pi-calendar', route: 'calendar'},
        {label: 'Anuncios', icon: 'pi pi-fw pi-megaphone'},
        {label: 'Grupos', icon: 'pi pi-fw pi-sitemap', route: 'groups'},
        {label: 'Cerrar sesión', icon: 'pi pi-fw pi-power-off'},
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
  transition: width 0.3s;
  background-color: $white-color;
  color: #333;
  padding: 10px;
  box-sizing: border-box;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  margin-top: 100px;
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.avatar {
  background-color: #333;
  color: #fff;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20%;
  font-weight: bold;
  transition: transform 0.3s, margin-left 0.3s;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.user-sidebar {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
  color: #333; /* Texto oscuro */
}

.role {
  margin: 0;
  font-size: 13px;
  color: #555;
}

.sidebar-icon {
  font-size: 24px;
  transition: transform 0.3s, box-shadow 0.3s;
  color: #333;
}

.sidebar-text {
  font-size: 14px;
  font-weight: 500;
  margin-left: 15px;
  transition: opacity 0.3s;
  color: #333;
}

ul {
  padding: 0;
  list-style-type: none;
}

.item {
  display: flex;
  align-items: center;
  text-decoration: none;
  padding: 18px 15px;
  width: 100%;
  background-color: transparent;
  border-radius: 9px;
  color: #333;
  margin-bottom: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.item:hover {
  border-radius: 9px;
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
  cursor: pointer;
}

.custom-sidebar.closed {
  width: 100px;
}

.custom-sidebar.closed .sidebar-text {
  opacity: 0;
  visibility: hidden;
}

.custom-sidebar.closed .sidebar-icon {
  margin-left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 50px;
  border-radius: 20%;
  background-color: $white-color;
  color: #333;
  font-size: 24px;
  padding: 24px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.custom-sidebar.closed .item:hover .sidebar-icon {
  box-shadow: none;
}

.custom-sidebar.closed .sidebar-header {
  justify-content: center;
}

.custom-sidebar.closed .avatar {
  transform: translateX(0);
  margin-left: 0;
}

.custom-sidebar.closed .user-sidebar,
.custom-sidebar.closed .role {
  display: none;
}

</style>

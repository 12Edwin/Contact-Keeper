<template>
  <div>
    <Navbar @toggle-sidebar="toggleSidebar" />
    <div class="d-flex">
      <Sidebar @update:visible="sidebarVisible = $event" :visible="sidebarVisible"/>
      <div class="content">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  components : {
    Navbar: () => import('@/components/Navbar.vue'),
    Sidebar: () => import('@/components/SidebarAdmin.vue'),
  },
  data(){
    return {
      sidebarVisible: false
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible
    },
  }
}
</script>

<style scoped>
.content{
  padding-left: 20px;
  padding-top: 20px;
  padding-right: 20px;
  width: 100%;
  overflow: auto;
  height: 92vh;
  margin-top: 60px;
}
</style>
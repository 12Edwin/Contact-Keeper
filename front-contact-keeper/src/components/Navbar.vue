<template>
  <div>
    <b-navbar toggleable="lg" type="dark" class="custom-navbar" fixed="top">
      <b-navbar-toggle 
        target="nav-collapse" 
        @click="toggleSidebar" 
        class="icon-container">
        <i class="pi pi-bars"></i>
      </b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="#" @click="$emit('toggle-sidebar')" class="icon-container">
            <i class="pi pi-bars"></i>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: 'Navbar',
  methods: {
    toggleSidebar() {
      this.$emit('toggle-sidebar');
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/colors.scss';

.custom-navbar {
  height: 8vh;
  width: 100vw;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem; 
  color: $secondary-color; 
}
</style>

<template>
    <b-navbar toggleable="lg" type="dark" class="custom-navbar" fixed="top">  
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="#" @click="$emit('toggle-sidebar')">
            <i class="pi pi-bars" :style="config"></i>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </template>
  
  <script>
  export default {
    name: 'Navbar',
    data(){
      return {
        config: {
          'fontSize': '1.1rem',
          'color': '#737373',
          'margin-left': '0.2rem'
        }
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
  </style>
  
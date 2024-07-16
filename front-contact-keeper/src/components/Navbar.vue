<template>
    <b-navbar toggleable="lg" type="dark" class="custom-navbar" fixed="top">  
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="#" @click="$emit('toggle-sidebar')">
            <b-icon icon="list"></b-icon>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </template>
  
  <script>
  export default {
    name: 'Navbar'
  }
  </script>
  
  <style scoped lang="scss">
   @import '@/styles/colors.scss';
  .custom-navbar {
    background-color: $primary-color 
  }
  </style>
  
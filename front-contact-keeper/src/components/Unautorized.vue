<template>
    <div class="content-gif" :style="`box-shadow: 0 0 10px 10px ${color} inset;`">
      <div class="body-gif">
        <img alt="Not Found" src="@/assets/rechazado.gif" style="width:100%; object-fit: cover; object-position: center;"/>
        <h4>{{ message }}</h4>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Unauthorized',
    props:{
      message:{
        type: String,
        default: 'No tienes permisos para acceder a esta página'
      },
      color: {
        type: String,
        default: '#f5f5f5'
      }
    }
  }
  </script>
  
  <style scoped>
  .content-gif {
    background-color: white;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    border-radius: 15px
  }
  .body-gif{
    width: 40% !important;
    text-align: center;
  }
  h4{
    font-size: 20px;
    font-weight: bold;
    color: #333;
    margin-top: 10px;
    font-family: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  }
  </style>
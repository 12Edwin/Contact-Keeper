<template>
    <Panel header="Información del usuario">
      <div class="user-info">
        <Avatar :label="user.name.charAt(0)" shape="circle" size="xlarge" />
        <h3>{{ user.name }}</h3>
        <p><strong>Correo electrónico:</strong> {{ user.email }}</p>
        <p><strong>Número de teléfono:</strong> 7775743812</p>
      </div>
    </Panel>
  </template>
  
  <script>
  import Panel from 'primevue/panel'
  import Avatar from 'primevue/avatar'
  
  export default {
    name: 'UserInfo',
    components: {
      Panel,
      Avatar
    },
    props: {
      user: Object
    }
  }
  </script>
  
  <style scoped>
  .user-info {
    text-align: center;
    padding: 2rem;
  }
  
  .user-info h3 {
    margin: 0.5rem 0 1rem;
  }
  
  .user-info p {
    margin: 0.25rem 0;
  }
  </style>
  
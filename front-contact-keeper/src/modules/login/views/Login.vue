<template>
    <div class="login-container">
      <div class="image-zone">
        <img src="../../../assets/logo_sin_fondo.png" alt="Login image" class="login-image">
      </div>
      <div class="form-zone">
        <form @submit.prevent="login" class="login-form">
          <h2>Agenda</h2>
          <div class="input-group">
            <label for="username">Usuario:</label>
            <input type="text" id="username" v-model="username" required>
          </div>
          <div class="input-group">
            <label for="password">Contraseña:</label>
            <input type="password" id="password" v-model="password" required>
          </div>
          <button type="submit" class="login-button">Iniciar sesión</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginComponent',
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      login() {
        console.log('Login attempted with:', this.username, this.password)
        this.username = ''
        this.password = ''
      }
    }
  }
  </script>
  
  <style scoped lang="scss">
  @import '@/styles/colors.scss';

  .login-container {
    display: flex;
    justify-content: center;
    align-items: stretch;
    min-height: 100vh;
    background-color: #f0f0f0;
  }
  
  .image-zone {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    background: rgb(90,185,234);
    background: radial-gradient(circle, rgba(90,185,234,1) 40%, rgba(9,9,121,1) 100%);
  }
  
  .login-image {
    max-width: 100%;
    max-height: 400px;
    object-fit: cover;
  }
  
  .form-zone {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    background-color: white;
  }
  
  .login-form {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
  }
  
  h2 {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
  }
  
  .input-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #666;
  }
  
  input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .login-button {
    width: 104%;
    padding: 0.75rem;
    background-color: $azul-cielo;
    color: white;
    border: none;
    border-radius: 9px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .login-button:hover {
    background-color: $rojo-brillante;
  }
  
  @media (max-width: 768px) {
    .login-container {
      flex-direction: column;
    }
  
    .image-zone, .form-zone {
      flex: none;
      width: 100%;
    }
  
    .image-zone {
      padding: 1rem;
    }
  
    .login-image {
      max-height: 200px;
    }
  
    .form-zone {
      padding: 1rem;
    }
  
    .login-form {
      padding: 1.5rem;
    }
  }
  </style>
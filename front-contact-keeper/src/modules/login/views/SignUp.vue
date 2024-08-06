<template>
  <form @submit.prevent="signup" class="login-form onLoginShowed">
    <h2>Registrate</h2>
    <div class="input-group">
      <label for="username">Usuario:</label>
      <input type="text" id="username" v-model="username" required>
    </div>
    <div class="input-group">
      <label for="password">Contraseña:</label>
      <input type="password" id="password" v-model="password" required>
    </div>
    <button type="submit" class="login-button">Registrarse</button>
    <div class="text-center">
      <Button label="Iniciar sesión" class="p-button-text p-button-text mt-2 p-button-plain text" @click="showLoginForm()"/>
    </div>
  </form>
</template>

<script>
export default {
  data(){
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    showLoginForm(){
      this.$emit('showLoginForm')
    },
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/colors.scss';
h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.login-form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
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
  width: 100%;
  padding: 0.75rem;
  background-color: $primary-color;
  color: white;
  border: none;
  border-radius: 9px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.onLoginShowed {
  animation: fadeIn 0.5s;
}
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
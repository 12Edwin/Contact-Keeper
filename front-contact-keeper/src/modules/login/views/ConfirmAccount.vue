<template>
    <div class="form-zone">
      <form @submit.prevent="signup" class="login-form onLoginShowed">
        <h3 class="text-center">¡Confirma tu cuenta!</h3>
        <template>
          <Divider/>
            <div class="inf-text text-center">
                <p>¡Estas a un paso de completar el registro, solo ingresa el código que te hemos enviado por correo!</p>
            </div>
          <div class="input-group">
              <label for="code" class="form-label-required">Código:</label>
              <input type="text" id="code" required>
            </div>
        </template>
        <template>
          <b-row>
            <b-col class="d-flex justify-content-center mt-2">
                <Button type="submit" :disabled="isLoading" @click="confirm()" class="login-button">{{ isLoading ?
            'Confirmando cuenta...' :
            'Confirmar cuenta' }}</Button>
            </b-col>
          </b-row>
        </template>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ConfirmAccount',
    data() {
      return {
        code: '',
        isLoading: false
      }
    },
    methods: {
      confirm(){
        console.log('confirm')
        this.isLoading = true
        setTimeout(() => {
            this.$emit('showLoginForm')
            this.isLoading = false
        }, 5000)
        
      }
    }
  }
  </script>
  
  <style scoped lang="scss" scoped>
  @import '@/styles/colors.scss';
  
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
  
  .show-password {
    display: flex;
    flex-direction: column;
  }
  
  h2 {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
  }
  
  .input-group {
    margin-bottom: 2rem;
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
    justify-content: center;
  }
  
  .login-button:hover {
    background-color: $gray-color !important;
  }
  
  @media (max-width: 768px) {
    .login-container {
      flex-direction: column;
    }
  
    .form-zone {
      padding: 1rem;
    }
  
    .login-form {
      padding: 1.5rem;
    }
  }
  
  .form-label-required::after {
    content: " *";
    color: $red-color;
  }
  
  .invalid-field-custom {
    border-color: $red-color !important;
    box-shadow: 0 0 3px $shadows !important;
  }
  
  .error-messages {
    margin-bottom: 0;
    font-weight: 350;
    font-size: 15px;
  }
  
  .error-messages::before {
    content: "* ";
    color: $red-color;
  }
  
  /*animation*/
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
  
  .p-inline-message {
    width: 80%;
    font-weight: 350;
  }
  
  .form-label-required::after {
    content: " *";
    color: $red-color;
  }
  
  .invalid-field-custom {
    border-color: $red-color !important;
    box-shadow: 0 0 3px $shadows !important;
  }
  
  .error-messages {
    margin-bottom: 0;
    font-weight: 350;
    font-size: 15px;
  }
  
  .error-messages::before {
    content: "* ";
    color: $red-color;
  }

  .inf-text {
    font-size: 0.8rem;
    color: #666;
  }
  </style>
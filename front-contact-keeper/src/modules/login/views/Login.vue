<template>
    <div class="login-container">
      <div class="image-zone">
        <img src="../../../assets/logo_sope.png" alt="Login image" class="login-image">
      </div>
      <div class="form-zone">
        <template v-if="isLoggingIn">
          <form @submit.prevent="login" class="login-form onLoginShowed">
            <h2>SOPE</h2>
            <div class="input-group">
              <label for="username" class="form-label-required">Correo electrónico:</label>
              <input :class="{ 'invalid-field-custom': v$.email.$error }" type="text" id="username" required v-model="v$.email.$model">
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.email.$dirty && v$.email.required.$invalid">
                  {{ v$.email.required.$message }}
                </p>
                <p class="error-messages"
                   v-if="v$.email.$dirty && v$.email.validEmail.$invalid">
                  {{ v$.email.validEmail.$message }}
                </p>
              </div>
            </div>
            <div class="input-group">
              <label for="password" class="form-label-required">Contraseña:</label>
              <input :type="getInputType()" id="password" :class="{ 'invalid-field-custom': v$.password.$error }" v-model="v$.password.$model" required>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.password.$dirty && v$.password.required.$invalid">
                  {{ v$.password.required.$message }}
                </p>
              </div>
            </div>
            <b-row>
              <b-col cols="12" class="d-flex justify-content-start align-items-center mb-3">
                <Checkbox id="binary" :binary="true" v-model="showPassword"/>
                <label for="binary" style="margin-left: 5px; margin-top: 5px">Mostrar contraseña</label>
              </b-col>
            </b-row>
            <Button type="submit" :disabled="isLoading" class="login-button">{{isLoading ? 'Iniciando sesión...' : 'Iniciar sesión'}}</Button>
            <div class="text-center">
              <Button label="Registrate" class="p-button-text p-button-text mt-1 p-button-plain text" @click="showSignForm()"/>
            </div>
          </form>
        </template>
        <template v-else>
          <SignUp @showLoginForm="showLoginForm"/>
        </template>
      </div>
    </div>
  </template>
  
  <script>
  import SignUp from "@/modules/login/views/SignUp.vue";
  import { reactive } from '@vue/composition-api'
  import {useVuelidate} from "@vuelidate/core";
  import {required, helpers, email} from '@vuelidate/validators'
  export default {
    name: 'LoginComponent',
    components: {
      SignUp
    },
    setup(){
      const credentials = reactive({
        email: '',
        password: ''
      })

      const rules = {
        email : {
          required: helpers.withMessage('El correo es requerido', required),
          validEmail: helpers.withMessage('Correo electrónico inválido', email),
        },
        password: {
          required: helpers.withMessage('La contraseña es requerida', required),
        },
      }
      const v$ = useVuelidate(rules, credentials)
      return { credentials, v$ }
    },
    data() {
      return {
        isLoggingIn: true,
        showPassword: false,
        isLoading: false
      }
    },
    methods: {
      login() {
        this.isLoading = true
        setTimeout(() => {
          this.isLoading = false
        }, 2000)
      },
      showSignForm() {
        this.isLoggingIn = false
      },
      showLoginForm(){
        this.isLoggingIn = true
      },
      getInputType() {
        return this.showPassword ? 'text' : 'password'
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
    background: rgb(0,0,0);
    background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(255,255,255,1) 100%);
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
  .show-password{
    display: flex;
    flex-direction: column;
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
  </style>
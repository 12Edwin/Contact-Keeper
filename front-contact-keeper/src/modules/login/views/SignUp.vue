<template>
  <div class="form-zone">
    <template v-if="!onConfirmAccount">
      <form @submit.prevent="signup" class="login-form onLoginShowed">
        <h3 class="text-center">Registrate</h3>
        <template v-if="formPart === 1">
          <h6 class="mt-2">Identificación</h6>
          <Divider align="right">
            <div class="inline-flex align-items-center">
              <small>Paso {{ formPart }} de 3</small>
            </div>
          </Divider>
          <div class="input-group-row">
            <div class="input-group-cols-6">
              <label for="username" class="form-label-required">Usuario:</label>
              <input type="text" id="username" required />
            </div>
            <div class="input-group-cols-6">
              <label for="name" class="form-label-required">Nombre:</label>
              <input type="text" id="name" required />
            </div>
          </div>
          <div class="input-group-row">
            <div class="input-group-cols-6">
              <label for="lastname" class="form-label-required"
                >Apellido paterno:</label
              >
              <input type="text" id="lastname" required />
            </div>
            <div class="input-group-cols-6">
              <label for="surname" class="form-label-required"
                >Apellido materno:</label
              >
              <input type="text" id="surname" required />
            </div>
          </div>
        </template>
        <template v-if="formPart === 2">
          <h6 class="mt-2">Sobre ti</h6>
          <Divider align="right">
            <div class="inline-flex align-items-center">
              <small>Paso {{ formPart }} de 3</small>
            </div>
          </Divider>
          <div class="input-group-row">
            <div class="input-group-cols-6">
              <label for="birthdate" class="form-label-required"
                >Nacimiento:</label
              >
              <input type="date" id="birthdate" required />
            </div>
            <div class="input-group-cols-6">
              <label for="phone" class="form-label-required">Teléfono:</label>
              <input type="tel" id="phone" required />
            </div>
          </div>
          <div class="input-group">
            <label for="email" class="form-label-required"
              >Correo electrónico:</label
            >
            <input type="email" id="email" v-model="username" required />
          </div>
        </template>
        <template v-if="formPart === 3">
          <h6 class="mt-2">Acceso</h6>
          <Divider align="right">
            <div class="inline-flex align-items-center">
              <small>Paso {{ formPart }} de 3</small>
            </div>
          </Divider>
          <div class="input-group">
            <label for="password" class="form-label-required"
              >Contraseña:</label
            >
            <input type="password" id="password" required />
          </div>
          <div class="input-group">
            <label for="confirmPasswors" class="form-label-required"
              >Confirmar contraseña:</label
            >
            <input type="password" id="confirmPasswors" required />
          </div>
        </template>
        <template>
          <b-row>
            <b-col class="d-flex justify-content-between">
              <Button
                :label="formPart === 1 ? 'Regresar' : 'Anterior'"
                class="p-button-text p-button-text p-button-plain"
                @click="formPart === 1 ? showLoginForm() : lastStep()"
              />
              <Button
                :label="formPart <= 2 ? 'Siguiente' : 'Registrate'"
                class="login-button"
                @click="formPart <= 2 ? nextStep() : signUp()"
              />
            </b-col>
          </b-row>
        </template>
      </form>
    </template>
    <template v-else>
      <ConfirmAccount @showLoginForm="showLoginForm" />
    </template>
  </div>
</template>

<script>
import Calendar from "primevue/calendar";
import ConfirmAccount from "./ConfirmAccount.vue";
export default {
  data() {
    return {
      username: "",
      password: "",
      formPart: 1,
      onConfirmAccount: false,
    };
  },
  components: {
    Calendar,
    ConfirmAccount,
  },
  methods: {
    showLoginForm() {
      this.$emit("showLoginForm");
    },
    nextStep() {
      if (this.formPart < 3) {
        this.formPart++;
      }
    },
    lastStep() {
      if (this.formPart > 1) {
        this.formPart--;
      }
    },
    signUp() {
      console.log("signing up");
      this.onReady();
    },
    onReady() {
      setTimeout(() => {
        this.onConfirmAccount = true;
        this.formPart = 1;
      }, 3000);
    },
  },
};
</script>

<style scoped lang="scss" scoped>
@import "@/styles/colors.scss";

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

.input-group-cols-6 {
  width: 48%;
  display: inline-block;
  margin-bottom: 1rem;
}

.input-group-row {
  display: flex;
  justify-content: space-between;
}
.login-button {
  background: $primary-color;
  color: white;
  border: none;
  border-radius: 5px;
}

.login-button:hover {
  background-color: $gray-color !important;
}

@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }

  .image-zone,
  .form-zone {
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
</style>

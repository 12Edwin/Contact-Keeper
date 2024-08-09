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
              <input type="text" id="username"  v-model="v$.username.$model" :class="{ 'invalid-field-custom': v$.username.$error }"/>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.username.$dirty && v$.username.required.$invalid">
                  {{ v$.username.required.$message }}
                </p>
                <p class="error-messages"
                  v-if="v$.username.$dirty && v$.username.onlyLetters.$invalid">
                  {{ v$.username.onlyLetters.$message }}
                </p>
                <p class="error-messages" v-if="v$.username.$dirty && v$.username.minLength.$invalid">
                  {{ v$.username.minLength.$message }}
                </p>
                <p class="error-messages" v-if="v$.username.$dirty && v$.username.maxLength.$invalid">
                  {{ v$.username.maxLength.$message }}
                </p>
              </div>
            </div>
            <div class="input-group-cols-6">
              <label for="name" class="form-label-required">Nombre:</label>
              <input type="text" id="name" required v-model="v$.name.$model"
              :class="{ 'invalid-field-custom': v$.name.$error }"/>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.name.$dirty && v$.name.required.$invalid">
                {{ v$.name.required.$message }}
                </p>
                <p class="error-messages"
                  v-if="v$.name.$dirty && v$.name.onlyLetters.$invalid">
                  {{ v$.name.onlyLetters.$message }}
                </p>
                <p class="error-messages" v-if="v$.name.$dirty && v$.name.minLength.$invalid">
                  {{ v$.name.minLength.$message }}
                </p>
                <p class="error-messages" v-if="v$.name.$dirty && v$.name.maxLength.$invalid">
                  {{ v$.name.maxLength.$message }}
                </p>
              </div>
            </div>
          </div>
          <div class="input-group-row">
            <div class="input-group-cols-6">
              <label for="lastname" class="form-label-required"
                >Apellido paterno:</label
              >
              <input type="text" id="lastname" v-model="v$.surname.$model"
              :class="{ 'invalid-field-custom': v$.surname.$error }" required/>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.surname.$dirty && v$.surname.required.$invalid">
                  {{ v$.surname.required.$message }}
                </p>
                <p class="error-messages"
                  v-if="v$.surname.$dirty && v$.surname.onlyLetters.$invalid">
                  {{ v$.surname.onlyLetters.$message }}
                </p>
                <p class="error-messages" v-if="v$.surname.$dirty && v$.surname.minLength.$invalid">
                  {{ v$.surname.minLength.$message }}
                </p>
                <p class="error-messages" v-if="v$.surname.$dirty && v$.surname.maxLength.$invalid">
                  {{ v$.surname.maxLength.$message }}
                </p>
              </div>
            </div>
            <div class="input-group-cols-6">
              <label for="surname" class="form-label-required"
                >Apellido materno:</label
              >
              <input type="text" id="surname" required v-model="v$.lastname.$model"
              :class="{ 'invalid-field-custom': v$.lastname.$error }"/>
              <div class="text-danger text-start pt-2">
                <p class="error-messages"
                  v-if="v$.lastname.$dirty && v$.lastname.onlyLetters.$invalid">
                  {{ v$.lastname.onlyLetters.$message }}
                </p>
              </div>
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
              <input type="date" id="birthdate" required  v-model="v$.birthdate.$model"
              :class="{ 'invalid-field-custom': v$.birthdate.$error }" />
              <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.birthdate.$dirty && v$.birthdate.required.$invalid">
                {{ v$.birthdate.required.$message }}
              </p>
            </div>
            </div>
            <div class="input-group-cols-6">
              <label for="phone" class="form-label-required">Teléfono:</label>
              <input type="tel" id="phone" required v-model="v$.phone.$model"
              :class="{ 'invalid-field-custom': v$.phone.$error }"/>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.phone.$dirty && v$.phone.required.$invalid">
                  {{ v$.phone.required.$message }}
                </p>
                <p class="error-messages"
                  v-if="v$.phone.$dirty && v$.phone.validPhone.$invalid">
                  {{ v$.phone.validPhone.$message }}
                </p>
                <p class="error-messages" v-if="v$.phone.$dirty && v$.phone.minLength.$invalid">
                  {{ v$.phone.minLength.$message }}
                </p>
                <p class="error-messages" v-if="v$.phone.$dirty && v$.phone.maxLength.$invalid">
                  {{ v$.phone.maxLength.$message }}
                </p>
              </div>
            </div>
          </div>
          <div class="input-group">
            <label for="email" class="form-label-required"
              >Correo electrónico:</label
            >
            <input type="email" id="email" v-model="v$.email.$model"
            :class="{ 'invalid-field-custom': v$.email.$error }" required />
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.email.$dirty && v$.email.required.$invalid">
                {{ v$.email.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.email.$dirty && v$.email.email.$invalid">
                {{ v$.email.email.$message }}
              </p>
            </div>
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
            <input type="password" id="password" required v-model="v$.password.$model" :class="{ 'invalid-field-custom': v$.password.$error }"/>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.password.$dirty && v$.password.required.$invalid">
                {{ v$.password.required.$message }}
              </p>
            </div>
          </div>
          <div class="input-group">
            <label for="confirmPasswors" class="form-label-required"
              >Confirmar contraseña:</label
            >
            <input type="password" id="confirmPasswors" required v-model="v$.confirmPassword.$model"/>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.confirmPassword.$dirty && v$.confirmPassword.required.$invalid">
                {{ v$.confirmPassword.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.confirmPassword.$dirty && v$.confirmPassword.match.$invalid">
                {{ v$.confirmPassword.match.$message }}
              </p>
            </div>
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
                :disabled="validFormPart()"
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
import {reactive} from "@vue/composition-api";
import useVuelidate from "@vuelidate/core";
import { required, helpers, maxLength, minLength, email } from '@vuelidate/validators'
import {nameRegex, noRequiredField, phoneRegex} from "@/kernel/patterns.js";
import moment from 'moment'
export default {
  data() {
    return {
      username: "",
      password: "",
      formPart: 1,
      onConfirmAccount: false,
    };
  },
  setup(){
    const newPerson = reactive({
      username: '',
      name: '',
      lastname: '',
      surname: '',
      birthdate: '',
      phone: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const rules = {
      username : {
        required: helpers.withMessage('El nombre de usuario es requerido', required),
        onlyLetters: helpers.withMessage('El nombre de usuario solo puede contener letras y numeros', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El nombre debe tener menos de 10 caracteres", maxLength(10))
      },
      name: {
        required: helpers.withMessage('El nombre es requerido', required),
        onlyLetters: helpers.withMessage('El nombre solo puede contener letras', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El nombre debe tener menos de 50 caracteres", maxLength(60))
      },
      lastname: {
        onlyLetters: helpers.withMessage('El apellido materno solo puede contener letras', (value) => noRequiredField.test(value)),
      },
      surname: {
        required: helpers.withMessage('El apellido paterno es requerido', required),
        onlyLetters: helpers.withMessage('El apellido paterno solo puede contener letras', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El apellido debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El apellido debe tener menos de 50 caracteres", maxLength(60))
      },
      phone: {
        required: helpers.withMessage('El teléfono es requerido', required),
        validPhone: helpers.withMessage('El teléfono no es válido', (value) => phoneRegex.test(value)),
        minLength: helpers.withMessage("El teléfono debe ser de 10 caracteres", minLength(10)),
        maxLength: helpers.withMessage("El teléfono debe tener máximo 10 caracteres", maxLength(10))
      },
      password: {
        required: helpers.withMessage('La contraseña es requerida', required),
      },
      email: {
        required: helpers.withMessage('El correo electrónico es requerido', required),
        email: helpers.withMessage('El correo electrónico no es válido', email),
      },
      confirmPassword: {
        required: helpers.withMessage('La confirmación de la contraseña es requerida', required),
        match: helpers.withMessage('Las contraseñas no coinciden', (value) => value === newPerson.password)
      },
      birthdate: {
        required: helpers.withMessage('La fecha de nacimiento es requerida', required),
      }
    }

    const v$ = useVuelidate(rules, newPerson)
    return { newPerson, v$ }
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
      if(this.v$.$invalid) return;
      console.log("user creado =>",this.prepareObject())
    },
    onReady() {
      setTimeout(() => {
        this.onConfirmAccount = true;
        this.formPart = 1;
      }, 3000);
    },
    validFormPart(){
      if(this.formPart === 1){
        return this.v$.username.$invalid || this.v$.name.$invalid || this.v$.surname.$invalid || this.v$.lastname.$invalid;
      }else if(this.formPart === 2){
        return this.v$.phone.$invalid || this.v$.email.$invalid || this.v$.birthdate.$invalid;
      }else if(this.formPart === 3){
        return this.v$.password.$invalid || this.v$.confirmPassword.$invalid;
      }
    },
    formmatDate(date){
      return moment(date).format('YYYY-MM-DD')
    },
    prepareObject(){
      return {
        username: this.newPerson.username,
        name: this.newPerson.name,
        last_name: this.newPerson.lastname,
        surname: this.newPerson.surname,
        birthdate: this.formmatDate(this.newPerson.birthdate),
        phone: this.newPerson.phone,
        email: this.newPerson.email,
        password: this.newPerson.password,
        user_type: 'normal'
      }
    }
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
  font-size: 12px;
}

.error-messages::before {
  content: "* ";
  color: $red-color;
}
</style>

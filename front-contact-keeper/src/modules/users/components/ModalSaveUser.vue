<template>
  <Dialog
      header="Crear nuevo usuario"
      :modal="true"
      :closeOnEscape="false"
      :closable="false"
      position="center"
      :contentStyle="{overflow: 'visible', width: '50vw'}"
      :visible.sync="visible"
  >
    <div class="p-fluid grid">
      <b-row>
        <b-col cols="12">
          <h2 class="form-part">Identificación</h2>
        </b-col>
        <b-col class="mt-3 mb-2" lg="4">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-user" />
              <InputText id="field-name" v-model="v$.name.$model"
                         :class="{ 'invalid-field-custom': v$.name.$error }"/>
              <label for="field-name" class="form-label-required">Nombre</label>
            </span>
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
        </b-col>
        <b-col class="mt-3 mb-3" lg="4">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-user" />
              <InputText id="field-surname" v-model="v$.surname.$model"
                         :class="{ 'invalid-field-custom': v$.surname.$error }"/>
              <label for="field-surname" class="form-label-required">Apellido paterno</label>
            </span>
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
        </b-col>
        <b-col class="mt-3 mb-3" lg="4">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-user" />
              <InputText id="field-lastname" v-model="v$.lastname.$model"
                         :class="{ 'invalid-field-custom': v$.lastname.$error }"/>
              <label for="field-lastname">Apellido materno</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages"
                 v-if="v$.lastname.$dirty && v$.lastname.onlyLetters.$invalid">
                {{ v$.lastname.onlyLetters.$message }}
              </p>
            </div>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <h2 class="form-part">Contacto</h2>
        </b-col>
        <b-col class="mt-3 mb-3" lg="6">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-envelope" />
              <InputText id="field-email" v-model="v$.email.$model"
                         :class="{ 'invalid-field-custom': v$.email.$error }"/>
              <label for="field-email" class="form-label-required">Correo electrónico</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.email.$dirty && v$.email.required.$invalid">
                {{ v$.email.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.email.$dirty && v$.email.email.$invalid">
                {{ v$.email.email.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col class="mt-3 mb-2" lg="6">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-phone" />
              <InputText id="field-phone" v-model="v$.phone.$model"
                         :class="{ 'invalid-field-custom': v$.phone.$error }"/>
              <label for="field-phone" class="form-label-required">Teléfono</label>
            </span>
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
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <h2 class="form-part" >Acceso</h2>
        </b-col>
        <b-col class="mt-3 mb-2" cols="12" lg="12">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-at" />
              <Dropdown v-model="v$.user_type.$model" :options="userTypes" optionLabel="name"  optionValue="code"/>
              <label for="field-lastname" class="form-label-required">Tipo:</label>
            </span>
          </div>
        </b-col>
        <b-col class="mt-3 mb-2" lg="6">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-at" />
              <InputText id="field-username" type="text" v-model="v$.username.$model" :class="{ 'invalid-field-custom': v$.username.$error }"/>
              <label for="field-username" class="form-label-required">Usuario</label>
            </span>
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
        </b-col>
        <b-col class="mt-3 mb-2" lg="6">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <Password v-model="v$.password.$model" :class="{ 'invalid-field-custom': v$.password.$error }"  toggleMask promptLabel="Elige una contraseña segura" weakLabel="Débil" mediumLabel="Medianamente segura" strongLabel="Muy segura" >
                <template #header>
                  <h6>Escribe una contraseña</h6>
                </template>
                <template #footer>
                  <Divider />
                  <p class="mt-2">Sugerencias</p>
                  <ul class="pl-2 ml-2 mt-0" style="line-height: 1.5">
                      <li>Al menos una minúscula</li>
                      <li>Al menos una mayúscula</li>
                      <li>Al menos un número</li>
                      <li>Mínimo 8 caracteres</li>
                  </ul>
                </template>
              </Password>
              <label for="field-password" class="form-label-required">Contraseña</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.password.$dirty && v$.password.required.$invalid">
                {{ v$.password.required.$message }}
              </p>
            </div>
          </div>
        </b-col>
      </b-row>
    </div>
    <template #footer>
      <Button @click="saveUser()" label="Guardar" icon="pi pi-check"  iconPos="right" class="button-options"/>
      <Button  label="Cancelar" icon="pi pi-times" class="p-button-text p-button-text p-button-plain" iconPos="right" @click="closeModal()"/>
    </template>
  </Dialog>
</template>

<script>
import {reactive} from "@vue/composition-api";
import useVuelidate from "@vuelidate/core";
import { required, helpers, maxLength, minLength, email } from '@vuelidate/validators'
import {nameRegex, noRequiredField, phoneRegex} from "@/kernel/patterns.js";
export default {
  name: 'ModalSaveUser',
  props: {
    visible: Boolean,
    required: true
  },
  data(){
    return {
      show: false,
      userTypes: [
        {name: 'Administrador', code: 'admin'},
        {name: 'Usuario', code: 'normal'}
      ],
      selectedUser: null
    }
  },
  setup(){
    const person = reactive({
      name: '',
      surname: '',
      lastname: '',
      email: '',
      phone: '',
      password: '',
      user_type: '',
      username: ''
    })

    const rules = {
      name: {
        required: helpers.withMessage('El nombre es requerido', required),
        onlyLetters: helpers.withMessage('El nombre solo puede contener letras', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El nombre debe tener menos de 50 caracteres", maxLength(60))
      },
      surname: {
        required: helpers.withMessage('El apellido paterno es requerido', required),
        onlyLetters: helpers.withMessage('El apellido paterno solo puede contener letras', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El apellido debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El apellido debe tener menos de 50 caracteres", maxLength(60))
      },
      lastname: {
        onlyLetters: helpers.withMessage('El apellido materno solo puede contener letras', (value) => noRequiredField.test(value)),
      },
      email: {
        required: helpers.withMessage('El correo electrónico es requerido', required),
        email: helpers.withMessage('El correo electrónico no es válido', email),
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
      user_type: {
        required: helpers.withMessage('El tipo de usuario es requerido', required),
      },
      username : {
        required: helpers.withMessage('El nombre de usuario es requerido', required),
        onlyLetters: helpers.withMessage('El nombre de usuario solo puede contener letras y numeros', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El nombre debe tener menos de 10 caracteres", maxLength(10))
      }

    }
    const v$ = useVuelidate(rules, person)
    return {person, v$}
  },
  methods: {
    closeModal(){
      this.$emit('update:visible', false);
    },
    saveUser(){
      console.log('Guardando usuario')
      console.log(this.person)
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/colors';
.button-options {
  background: $primary-color;
  color: white;
  border: none;
  border-radius: 5px;
}

.form-part {
  font-size: 16px;
  color: $sidebar-items;
  font-weight: 600;
  margin-bottom: 10px;
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
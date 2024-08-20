<template>
  <Dialog header="Crear nuevo usuario" :modal="true" :closeOnEscape="false" :closable="false" position="center"
    :contentStyle="{ overflow: 'visible', width: '50vw' }" :visible.sync="visible">
    <div class="p-fluid grid">
      <b-row>
        <b-col cols="12">
          <h2 class="form-part">Identificación</h2>
        </b-col>
        <b-col class="mt-3 mb-2" lg="4">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-user" />
              <InputText id="field-name" v-model="v$.name.$model" :class="{ 'invalid-field-custom': v$.name.$error }" />
              <label for="field-name" class="form-label-required">Nombre</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.required.$invalid">
                {{ v$.name.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.onlyLetters.$invalid">
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
                :class="{ 'invalid-field-custom': v$.surname.$error }" />
              <label for="field-surname" class="form-label-required">Apellido paterno</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.surname.$dirty && v$.surname.required.$invalid">
                {{ v$.surname.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.surname.$dirty && v$.surname.onlyLetters.$invalid">
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
              <InputText id="field-last_name" v-model="v$.last_name.$model"
                :class="{ 'invalid-field-custom': v$.last_name.$error }" />
              <label for="field-last_name">Apellido materno</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.last_name.$dirty && v$.last_name.onlyLetters.$invalid">
                {{ v$.last_name.onlyLetters.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col class="mt-3 mb-3" lg="4">
          <div class="field">
            <div class="input-group-row">
              <div class="input-group-cols-6">
                <label for="birthday" class="form-label-required">Fecha de Nacimiento:</label>
                <input type="date" id="birthday" required v-model="v$.birthday.$model"
                  :class="{ 'invalid-field-custom': v$.birthday.$error }" />
                <div class="text-danger text-start pt-2">
                  <p class="error-messages" v-if="v$.birthday.$dirty && v$.birthday.required.$invalid">
                    {{ v$.birthday.required.$message }}
                  </p>
                  <p class="error-messages" v-if="serverError && serverError.field === 'birthday'">
                    {{ serverError.translate }}
                  </p>
                </div>
              </div>
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
                :class="{ 'invalid-field-custom': v$.email.$error }" />
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
                :class="{ 'invalid-field-custom': v$.phone.$error }" />
              <label for="field-phone" class="form-label-required">Teléfono</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.phone.$dirty && v$.phone.required.$invalid">
                {{ v$.phone.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.phone.$dirty && v$.phone.validPhone.$invalid">
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
          <h2 class="form-part">Acceso</h2>
        </b-col>
        <b-col class="mt-3 mb-2" cols="12" lg="12">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-at" />
              <Dropdown v-model="v$.user_type.$model" :options="userTypes" optionLabel="name" optionValue="code" />
              <label for="field-lastname" class="form-label-required">Tipo:</label>
            </span>
          </div>
        </b-col>
        <b-col class="mt-3 mb-2" lg="6">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-at" />
              <InputText id="field-username" type="text" v-model="v$.username.$model"
                :class="{ 'invalid-field-custom': v$.username.$error }" />
              <label for="field-username" class="form-label-required">Usuario</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.username.$dirty && v$.username.required.$invalid">
                {{ v$.username.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.username.$dirty && v$.username.onlyLetters.$invalid">
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
      </b-row>
    </div>
    <template #footer>
      <Button @click="saveUser()" label="Guardar" icon="pi pi-check" iconPos="right" class="button-options" />
      <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-text p-button-plain" iconPos="right"
        @click="closeModal()" />
    </template>
  </Dialog>
</template>

<script>
import { reactive } from "@vue/composition-api";
import useVuelidate from "@vuelidate/core";
import { required, helpers, maxLength, minLength, email } from '@vuelidate/validators'
import { nameRegex, noRequiredField, phoneRegex } from "@/kernel/patterns.js";
import service from '../services/userServices'
import { onError, onSuccess, onToast } from "@/kernel/alerts";
export default {
  name: 'ModalSaveUser',
  props: {
    visible: Boolean,
    required: true
  },
  data() {
    return {
      show: false,
      userTypes: [
        { name: 'Administrador', code: 'admin' },
        { name: 'Usuario', code: 'normal' }
      ],
      selectedUser: null
    }
  },
  setup() {
    const person = reactive({
      name: '',
      surname: '',
      last_name: '',
      email: '',
      phone: '',
      user_type: '',
      username: '',
      birthday: ''
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
      last_name: {
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
      user_type: {
        required: helpers.withMessage('El tipo de usuario es requerido', required),
      },
      username: {
        required: helpers.withMessage('El nombre de usuario es requerido', required),
        onlyLetters: helpers.withMessage('El nombre de usuario solo puede contener letras y numeros', (value) => nameRegex.test(value)),
        minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El nombre debe tener menos de 10 caracteres", maxLength(10))
      },
      birthday: {
        required: helpers.withMessage('La fecha de nacimiento es requerida', required),
      }

    }
    const v$ = useVuelidate(rules, person)
    return { person, v$ }
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
      this.v$.name.$model = '',
      this.v$.surname.$model = '',
      this.v$.last_name.$model = '',
      this.v$.email.$model = '',
      this.v$.phone.$model = '',
      this.v$.user_type.$model = '',
      this.v$.username.$model = '',
      this.v$.birthday.$model = '',
      this.v$.$reset()
    },
    async saveUser() {
      if (!this.v$.$invalid) {
        this.isLoading = true

        try {
          const { status, message } = await service.save_user(this.person);
          if (status === "success") {
            onToast("¡Éxito!", "¡Usuario guardado correctamente!");
            this.closeModal()
            this.$emit("getUsers")
          } else {
            onToast("¡Error!", "¡No se pudo guardar al usuario!");
          }
        } catch (error) {

          return error
        }
      } else {
        onError("¡Error!", "¡Debes completar los campos correctamente!");
      }
      this.isLoading = false
    },
    formmatDate(date) {
      return moment(date).format('YYYY-MM-DD')
    },
    prepareObject() {
      return {
        username: this.person.username,
        name: this.person.name,
        last_name: this.person.last_name,
        surname: this.person.surname,
        phone: this.person.phone,
        birthday: this.formmatDate(this.person.birthday),
        email: this.person.email,
        user_type: this.person.user_type
      }
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

input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
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

.input-group-cols-6 {
  width: 48%;
  display: inline-block;
  margin-bottom: 1rem;
}

.input-group-row {
  display: flex;
  justify-content: space-between;
}
</style>
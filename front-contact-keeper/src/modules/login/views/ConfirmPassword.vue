<template>
    <div class="form-zone">
        <form @submit.prevent="onConfirmPassword" class="login-form onLoginShowed">
            <h3 class="text-center">¡Confirma tu cuenta!</h3>
            <Divider />
            <div class="inf-text text-center">
                <p>Por tu seguridad, es necesario cambiar la contraseña que te enviamos a tu correo electrónico</p>
            </div>
            <div class="input-group">
                <label for="username" class="form-label-required">Correo electrónico:</label>
                <input :class="{ 'invalid-field-custom': v$.email.$error }" type="text" id="username" required
                    v-model="v$.email.$model">
                <div class="text-danger text-start pt-2">
                    <p class="error-messages" v-if="v$.email.$dirty && v$.email.required.$invalid">
                        {{ v$.email.required.$message }}
                    </p>
                    <p class="error-messages" v-if="v$.email.$dirty && v$.email.validEmail.$invalid">
                        {{ v$.email.validEmail.$message }}
                    </p>
                </div>
            </div>
            <div class="input-group-row">
                <div class="input-group-cols-6">
                    <label for="oldPassword" class="form-label-required">Contraseña:</label>
                    <input :type="getInputType()" id="oldPassword" v-model="v$.password.$model"
                        :class="{ 'invalid-field-custom': v$.password.$error }" required>
                    <div class="text-danger text-start pt-2">
                        <p class="error-messages" v-if="v$.password.$dirty && v$.password.required.$invalid">
                            {{ v$.password.required.$message }}
                        </p>
                    </div>
                </div>
                <div class="input-group-cols-6">
                    <label for="newPassword" class="form-label-required">Nueva contraseña:</label>
                    <input :type="getInputType()" id="newPassword" v-model="v$.new_password.$model"
                        :class="{ 'invalid-field-custom': v$.new_password.$error }" required>
                    <div class="text-danger text-start pt-2">
                        <p class="error-messages" v-if="v$.new_password.$dirty && v$.new_password.required.$invalid">
                            {{ v$.new_password.required.$message }}
                        </p>
                        <p class="error-messages" v-if="v$.new_password.$dirty && v$.new_password.validPass.$invalid">
                            {{ v$.new_password.validPass.$message }}
                        </p>
                    </div>
                </div>

            </div>
            <b-row>
                <b-col cols="12" class="d-flex justify-content-start align-items-center mb-3">
                    <Checkbox id="binary" :binary="true" v-model="showPassword" />
                    <label for="binary" style="margin-left: 5px; margin-top: 5px">Mostrar contraseña</label>
                </b-col>
            </b-row>
            <template>
                <b-row>
                    <b-col class="d-flex justify-content-center mt-2">
                        <Button type="submit" :disabled="isLoading" @click="onConfirmPassword()" class="login-button">{{
                            isLoading ?
                                'Confirmando cuenta...' :
                                'Confirmar cuenta' }}</Button>
                    </b-col>
                </b-row>
            </template>
            <template>
                <div class="text-center">
            <Button label="Regresar al inicio de sesión" class="p-button-text p-button-text mt-1 p-button-plain text"
              @click="goBackLogin()" />
          </div>
            </template>
        </form>
    </div>
</template>



<script>
import {
    reactive
} from "@vue/composition-api";
import useVuelidate from "@vuelidate/core";
import {
    required,
    helpers,
    maxLength,
    minLength,
    email
} from '@vuelidate/validators'
import services from '../services/Access'
import {
    onToast
} from "@/kernel/alerts";
import utils from "@/kernel/utils";
import { validPassword } from "@/kernel/patterns";
export default {
    name: 'ConfirmAccount',
    data() {
        return {
            isLoading: false,
            showPassword: false
        }
    },
    setup() {
        const confirmInfo = reactive({
            email: '',
            password: '',
            new_password: ''
        })

        const rules = {
            email: {
                required: helpers.withMessage('El email es requerido', required),
                validEmail: helpers.withMessage('Debes ingresar un email válido', email)
            },
            password: {
                required: helpers.withMessage('La contraseña es requerida', required),
            },
            new_password: {
                required: helpers.withMessage('Debes ingresar una nueva contraseña', required),
                validPass: helpers.withMessage('La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un carácter especial, un número y tener un mínimo de 6 caracteres.', (value) => validPassword.test(value))
            }
        }
        const v$ = useVuelidate(rules, confirmInfo)
        return {
            confirmInfo,
            v$
        }
    },
    methods: {
        goBackLogin() {
            this.$emit('showLoginForm')
        },
        async onConfirmPassword() {
            try {
                if (this.v$.password.$invalid || this.v$.new_password.$invalid || this.v$.email.$invalid) return;
                const response = await services.confirmAccount(this.confirmInfo)
                if (response) {
                    if (response.status === 'success') {
                        onToast('Bienvenido', 'Tu cuenta ha sido confirmada correctamente', 'success')
                        this.$emit('showLoginForm')
                        this.isLoading = false
                    }
                }
            } catch (error) { } finally {
                this.isLoading = false
            }
        },
        getInputType() {
            return this.showPassword ? 'text' : 'password'
        },
    }
}
</script>


<style lang="scss" scoped>
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

.input-group-cols-6 {
    width: 48%;
    display: inline-block;
    margin-bottom: 1rem;
}

.input-group-row {
    display: flex;
    justify-content: space-between;
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
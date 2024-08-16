<template>
    <Dialog
      header="Crear Nuevo Grupo"
      :modal="true"
      :closeOnEscape="false"
      :closable="false"
      position="center"
      :contentStyle="{ overflow: 'visible', width: '50vw' }"
      :visible.sync="visible"
    >
      <div class="p-fluid grid">
        <b-row>
          <b-col cols="12">
            <h2 class="form-part">Información del Grupo</h2>
          </b-col>
          <b-col class="mt-3 mb-2" lg="6">
            <div class="field">
              <span class="p-float-label p-input-icon-right">
                <i class="pi pi-briefcase" />
                <InputText id="field-name" v-model="group.name"
                           :class="{ 'invalid-field-custom': v$.name.$error }"/>
                <label for="field-name" class="form-label-required">Nombre del Grupo</label>
              </span>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.name.$dirty && v$.name.required.$invalid">
                  {{ v$.name.required.$message }}
                </p>
                <p class="error-messages" v-if="v$.name.$dirty && v$.name.maxLength.$invalid">
                  {{ v$.name.maxLength.$message }}
                </p>
              </div>
            </div>
          </b-col>
          <b-col class="mt-3 mb-2" lg="6">
            <div class="field">
              <span class="p-float-label p-input-icon-right">
                <i class="pi pi-align-left" />
                <InputText id="field-title" v-model="group.title"
                           :class="{ 'invalid-field-custom': v$.title.$error }"/>
                <label for="field-title">Título</label>
              </span>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.title.$dirty && v$.title.maxLength.$invalid">
                  {{ v$.title.maxLength.$message }}
                </p>
              </div>
            </div>
          </b-col>
          <b-col class="mt-3 mb-2" cols="12">
            <div class="field">
              <span class="p-float-label p-input-icon-right">
                <i class="pi pi-pencil" />
                <InputText id="field-description" v-model="group.description" rows="5"
                               :class="{ 'invalid-field-custom': v$.description.$error }"/>
                <label for="field-description">Descripción</label>
              </span>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.description.$dirty && v$.description.maxLength.$invalid">
                  {{ v$.description.maxLength.$message }}
                </p>
              </div>
            </div>
          </b-col>
          <b-col class="mt-3 mb-2" cols="12">
            <div class="field">
              <span class="p-float-label p-input-icon-right">
                <i class="pi pi-note" />
                <b-form-textarea id="field-notes" v-model="group.notes" rows="5"
                               :class="{ 'invalid-field-custom': v$.notes.$error }"/>
                <label for="field-notes">Notas</label>
              </span>
              <div class="text-danger text-start pt-2">
                <p class="error-messages" v-if="v$.notes.$dirty && v$.notes.maxLength.$invalid">
                  {{ v$.notes.maxLength.$message }}
                </p>
              </div>
            </div>
          </b-col>
        </b-row>
      </div>
      <template #footer>
        <Button @click="saveGroupForMember" label="Guardar" icon="pi pi-check" iconPos="right" class="button-options" :disabled="isLoading" />
        <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-plain" iconPos="right" @click="closeModal"/>
      </template>
    </Dialog>
  </template>
  
  <script>
  import { defineComponent, reactive } from 'vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, maxLength } from '@vuelidate/validators';
  import { helpers } from '@vuelidate/validators';
  import { saveGroup } from '../services/groups-services';
  import { onToast } from '@/kernel/alerts';
  
  export default defineComponent({
    name: 'ModalCreateGroup',
    props: {
      visible: {
        type: Boolean,
        required: true
      }
    },
    components: {
    },
    data() {
      return {
        isLoading: false
      };
    },
    setup(props, { emit }) {
      // Initial form data
      const group = reactive({
        name: '',
        description: '',
        title: '',
        notes: ''
      });

  
      // Validation rules
      const rules = {
        name: {
          required: helpers.withMessage('El nombre del grupo es requerido', required),
          maxLength: helpers.withMessage("El nombre del grupo debe tener menos de 50 caracteres", maxLength(50))
        },
        title: {
          required: helpers.withMessage('El título es requerido', required),
          maxLength: helpers.withMessage("El título debe tener menos de 20 caracteres", maxLength(50))
        },
        description: {
          required: helpers.withMessage('La descripción es requerida', required),
          maxLength: helpers.withMessage("La descripción debe tener menos de 50 caracteres", maxLength(50))
        },
        notes: {
          maxLength: helpers.withMessage("Las notas deben tener menos de 70 caracteres", maxLength(70))
        }
      };
  
      // Setup Vuelidate
      const v$ = useVuelidate(rules, group);
  
      // Function to close the modal
      const closeModal = () => {
        emit('update:visible', false);
      };
  
      const saveGroupForMember = async () => {
        this.isLoading = true;
        v$.value.$touch(); 
        if (v$.value.$invalid) {
          return;
        }

        try {
          const response = await saveGroup(group);
          if (response.status === 200 || response.status === 201 || response.status === "success") {
            onToast('success', 'Grupo creado correctamente', 'success');  
          }
          this.isLoading = false;
          closeModal();
        } catch (error) {
          this.isLoading = false;
          closeModal();
        }
      };
  
      return {
        group,
        v$,
        closeModal,
        saveGroupForMember,
      };
    }
  });
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
  
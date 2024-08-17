<template>
  <Dialog
    header="Editar Grupo"
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
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.minLength.$invalid">
                {{ v$.name.minLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.format.$invalid">
                {{ v$.name.format.$message }}
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
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.required.$invalid">
                {{ v$.title.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.maxLength.$invalid">
                {{ v$.title.maxLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.minLength.$invalid">
                {{ v$.title.minLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.format.$invalid">
                {{ v$.title.format.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col class="mt-3 mb-2" cols="12">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-pencil" />
              <b-form-textarea id="field-description" v-model="group.description" rows="2"
                             :class="{ 'invalid-field-custom': v$.description.$error }"/>
              <label for="field-description">Descripción</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.required.$invalid">
                {{ v$.description.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.maxLength.$invalid">
                {{ v$.description.maxLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.minLength.$invalid">
                {{ v$.description.minLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.format.$invalid">
                {{ v$.description.format.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col class="mt-3 mb-2" cols="12">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-note" />
              <b-form-textarea id="field-notes" v-model="group.notes" rows="3"
                             :class="{ 'invalid-field-custom': v$.notes.$error }"/>
              <label for="field-notes">Notas</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.notes.$dirty && v$.notes.maxLength.$invalid">
                {{ v$.notes.maxLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.notes.$dirty && v$.notes.format.$invalid">
                {{ v$.notes.format.$message }}
              </p>
            </div>
          </div>
        </b-col>
      </b-row>
    </div>
    <template #footer>
      <Button 
        @click="updateGroupFunction" 
        label="Guardar" 
        icon="pi pi-check" 
        iconPos="right" 
        class="button-options" 
        :disabled="isLoading || !isFormValid"
      />
      <Button 
        label="Cancelar" 
        icon="pi pi-times" 
        class="p-button-text p-button-plain" 
        iconPos="right" 
        @click="closeModal"
      />
    </template>
  </Dialog>
</template>

<script>
import { defineComponent, reactive, computed, ref, watch } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, maxLength, minLength } from '@vuelidate/validators';
import { helpers } from '@vuelidate/validators';
import { onQuestion } from '@/kernel/alerts';
import { updateGroup } from '../services/groups-services';
import { nameRegex, phraseRegex } from '@/kernel/patterns';

export default defineComponent({
  name: 'ModalPutGroup',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    groupData: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    const group = reactive({
      name: props.groupData?.name || '',
      description: props.groupData?.description || '',
      title: props.groupData?.title || '',
      notes: props.groupData?.notes || ''
    });

    watch(() => props.groupData, (newValue) => {
      group.name = newValue?.name || '';
      group.description = newValue?.description || '';
      group.title = newValue?.title || '';
      group.notes = newValue?.notes || '';
    }, { deep: true });

    const rules = {
      name: {
        required: helpers.withMessage('El nombre del grupo es requerido', required),
        maxLength: helpers.withMessage("El nombre del grupo debe tener menos de 50 caracteres", maxLength(50)),
        minLength: helpers.withMessage("El nombre del grupo debe tener al menos 3 caracteres", minLength(3)),
        format: helpers.withMessage("El nombre del grupo solo puede contener letras, números y espacios", helpers.regex(nameRegex))
      },
      title: {
        required: helpers.withMessage('El título es requerido', required),
        maxLength: helpers.withMessage("El título debe tener menos de 50 caracteres", maxLength(50)),
        minLength: helpers.withMessage("El título debe tener al menos 3 caracteres", minLength(3)),
        format: helpers.withMessage("El título solo puede contener letras, números y espacios", helpers.regex(nameRegex))
      },
      description: {
        required: helpers.withMessage('La descripción es requerida', required),
        maxLength: helpers.withMessage("La descripción debe tener menos de 50 caracteres", maxLength(50)),
        minLength: helpers.withMessage("La descripción debe tener al menos 3 caracteres", minLength(3)),
        format: helpers.withMessage("La descripción puede contener letras, números, espacios, puntos y comas", helpers.regex(phraseRegex))
      },
      notes: {
        maxLength: helpers.withMessage("Las notas deben tener menos de 70 caracteres", maxLength(70)),
        format: helpers.withMessage("Las notas pueden contener letras, números, espacios, puntos y comas", helpers.regex(phraseRegex))
      }
    };

    const v$ = useVuelidate(rules, group);
    const isLoading = ref(false);
    const isFormValid = computed(() => !v$.value.$pending && !v$.value.$invalid);

    const closeModal = () => {
      emit('update:visible', false);
    };

    const updateGroupFunction = async () => {  
      isLoading.value = true;
      v$.value.$touch();
      if (v$.value.$invalid) {
        isLoading.value = false;
        return;
      }

      await onQuestion('¿Estás seguro de que deseas actualizar este grupo?');
      try {
        const response = await updateGroup(props.groupData.id, {
          id: props.groupData.id,
          name: group.name,
          description: group.description,
          title: group.title,
          notes: group.notes
        });
        if (response.status === 200 || response.status === 201 || response.status === "success") {
          emit('update-data');
          closeModal();
        }
      } catch (error) {
        console.error('Error al actualizar el grupo:', error);
      } finally {
        isLoading.value = false;
      }
    };

    return {
      group,
      v$,
      closeModal,
      updateGroupFunction,
      isLoading,
      isFormValid
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

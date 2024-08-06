<template>
  <Dialog
    header="Agregar Nuevo Evento"
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{ overflow: 'visible', width: '35vw' }"
    class="custom-dialog"
    :autoZIndex="true"
  >
    <div class="event-form">
      <b-row>
        <b-col cols="12">
          <div class="form-group">
            <label for="title">Título</label>
            <InputText v-model="v$.title.$model" type="text" class="form-control" id="title" placeholder="Título del Evento" @input="v$.title.$touch"/>
            <small class="p-error" v-if="v$.title.$error">{{ v$.title.$errors[0].$message }}</small>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <div class="form-group">
            <label for="description">Descripción</label>
            <textarea v-model="v$.description.$model" class="form-control" id="description" placeholder="Descripción del Evento" @input="v$.description.$touch"></textarea>
            <small class="p-error" v-if="v$.description.$error">{{ v$.description.$errors[0].$message }}</small>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6">
          <div class="form-group">
            <span class="p-float-label">
              <Dropdown id="type" :options="types" v-model="v$.type.$model" optionLabel="label" class="full-width-dropdown" @change="v$.type.$touch"/>
              <label for="type">Tipo</label>
            </span>
            <small class="p-error" v-if="v$.type.$error">{{ v$.type.$errors[0].$message }}</small>
          </div>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="form-group">
            <span class="p-float-label">
              <Dropdown id="participants" :options="invites" v-model="v$.participants.$model" optionLabel="label" class="full-width-dropdown" @change="v$.participants.$touch"/>
              <label for="participants">Participantes</label>
            </span>
            <small class="p-error" v-if="v$.participants.$error">{{ v$.participants.$errors[0].$message }}</small>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6">
          <div class="form-group">
            <label for="start">Fecha de Inicio</label>
            <input v-model="v$.startDate.$model" type="date" class="form-control" id="start" :min="today" @input="v$.startDate.$touch">
            <small class="p-error" v-if="v$.startDate.$error">{{ v$.startDate.$errors[0].$message }}</small>
          </div>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="form-group">
            <label for="end">Fecha de Fin</label>
            <input v-model="v$.endDate.$model" type="date" class="form-control" id="end" :min="v$.startDate.$model" @input="v$.endDate.$touch">
            <small class="p-error" v-if="v$.endDate.$error">{{ v$.endDate.$errors[0].$message }}</small>
          </div>
        </b-col>
      </b-row>
    </div>
    <template #footer>
      <Button label="Guardar" icon="pi pi-check" style="background-color: black; color: white;" class="p-button-text" @click="saveEvent" />
      <Button label="Cancelar" icon="pi pi-times" style="color: gray;" class="p-button-text" @click="closeModal" />
    </template>
  </Dialog>
</template>

<script>
import { ref, reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, helpers, maxLength, minLength } from '@vuelidate/validators';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import {phraseRegex} from "@/kernel/patterns.js";

export default {
  name: 'ModalAddEvent',
  components: {
    Dialog,
    Button,
    Dropdown,
    InputText
  },
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      types: [
        { label: 'Cumpleaños', value: 'tipo1' },
        { label: 'Tipo 2', value: 'tipo2' }
      ],
      invites: [
        { label: 'Merri Chrismas', value: 'invitado1' },
        { label: 'Isa Palacios', value: 'invitado2' },
        { label: 'Typescrips', value: 'invitado3' }
      ],
      today: new Date().toISOString().split('T')[0]
    };
  },
  setup() {
    const eventData = reactive({
      title: '',
      description: '',
      startDate: '',
      endDate: '',
      type: null,
      participants: null
    });

    const rules = {
      title: {
        required: helpers.withMessage('El título del evento es requerido', required),
        onlyLetters: helpers.withMessage('El título solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("El título debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El título debe tener máximo de 30 caracteres", maxLength(30))
      },
      description: {
        required: helpers.withMessage('La descripción es requerida', required),
        onlyLetters: helpers.withMessage('La descripción solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("La descripción debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("La descripción debe tener máximo 70 caracteres", maxLength(70))
      },
      startDate: {
        required: helpers.withMessage('La fecha de inicio del evento es requerida', required),
      },
      endDate: {
        required: helpers.withMessage('La fecha de fin del evento es requerida', required),
      },
      type: {
        required: helpers.withMessage('El tipo de evento es requerido', required),
      },
      participants: {
        required: helpers.withMessage('El tipo de evento es requerido', required),
      }
    };

    const v$ = useVuelidate(rules, eventData);
    return {eventData, v$}
  },
  methods:{
    closeModal(){
      this.$emit('update:visible', false);
    },

    saveEvent() {
      console.log(this.eventData);
      this.closeModal(); 
    }
  }
};
</script>


<style scoped lang="scss">
 @import '@/styles/colors';
 .field {
    margin-bottom: 1rem;
  }
  .full-width-dropdown {
    width: 100%;
  }
  .event-form {
    margin: 1rem;
  }
  .form-group {
    margin-bottom: 1rem;
  }
  .invalid-field-custom {
    border-color: $red-color;
  }
  .p-error {
    color: $red-color;
  }
</style>
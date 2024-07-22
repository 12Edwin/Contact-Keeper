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
            <input v-model="eventData.title" type="text" class="form-control" id="title" placeholder="Título del Evento">
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <div class="form-group">
            <label for="description">Descripción</label>
            <textarea v-model="eventData.description" class="form-control" id="description" placeholder="Descripción del Evento"></textarea>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6">
          <div class="form-group">
                <span class="p-float-label">
            <Dropdown id="type" :options="types" v-model="eventData.type" optionLabel="label" />
            <label for="type">Tipo</label>
          </span>
          </div>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="form-group">
                <span class="p-float-label">
            <Dropdown id="participants" :options="invites" v-model="eventData.participants" optionLabel="label" />
            <label for="participants">Participantes</label>
          </span>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6">
          <div class="form-group">
            <label for="start">Fecha de Inicio</label>
            <input v-model="eventData.startDate" type="date" class="form-control" id="start">
          </div>
        </b-col>
        <b-col cols="12" lg="6">
          <div class="form-group">
            <label for="end">Fecha de Fin</label>
            <input v-model="eventData.endDate" type="date" class="form-control" id="end">
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
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

export default {
  name: 'ModalAddEvent',
  components: {
    Dialog,
    Button,
  },
  data() {
    return {
      eventData: {
        title: '',
        description: '',
        startDate: '',
        endDate: '',
        type: '',
        participants: ''
      },
      types: [
        { label: 'Cumpleaños', value: 'tipo1' },
        { label: 'Tipo 2', value: 'tipo2' }
      ],
      invites: [
        { label: 'Merri Chrismas', value: 'invitado1' },
        { label: 'Isa Palacios', value: 'invitado2' },
        { label: 'Typescrips', value: 'invitado3' }
      ],
      users: [
        { name: 'Usuario 1' },
        { name: 'Usuario 2' }
      ],
      selectedUsers: [],
      selectedGuests: [],
      sourceHeader: 'Disponibles',
      targetHeader: 'Seleccionados'
    };
  },
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
    saveEvent() {
      this.$emit('add-event', { ...this.eventData });
      this.closeModal();
    },
  },
};
</script>

<style scoped>
.event-form {
  margin: 1rem;
}
.form-group {
  margin-bottom: 1rem;
}
</style>

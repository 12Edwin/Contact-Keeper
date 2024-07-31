<template>
    <Dialog
      header="Crear nuevo evento"
      :visible="true"
      modal
      :style="{ width: '70vw' }"
      :closable="false"
      @hide="$emit('close')"
    >
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-6">
          <span class="p-float-label">
            <InputText id="name" v-model="event.name" />
            <label for="name">Nombre</label>
          </span>
        </div>
        <div class="p-col-12 p-md-6">
          <span class="p-float-label">
            <Dropdown id="type" :options="types" v-model="event.type" optionLabel="label" />
            <label for="type">Tipo</label>
          </span>
        </div>
        <div class="p-col-12">
          <span class="p-float-label">
            <Dropdown id="invites" :options="invites" v-model="event.invites" optionLabel="label" />
            <label for="invites">Invitados</label>
          </span>
        </div>
        <div class="p-col-12 p-md-6">
          <h3>Usuarios</h3>
          <PickList
            :source="users"
            :target="selectedUsers"
            :sourceHeader="sourceHeader"
            :targetHeader="targetHeader"
            responsive
            @moveToTarget="onMoveToTarget"
            @moveToSource="onMoveToSource"
          >
            <template v-slot:item="slotProps">
              <div>{{ slotProps.item.name }}</div>
            </template>
          </PickList>
        </div>
        <div class="p-col-12 p-md-6">
          <h3>Invitados</h3>
          <PickList
            :source="guests"
            :target="selectedGuests"
            :sourceHeader="sourceHeader"
            :targetHeader="targetHeader"
            responsive
            @moveToTarget="onMoveToTarget"
            @moveToSource="onMoveToSource"
          >
            <template v-slot:item="slotProps">
              <div>{{ slotProps.item.name }}</div>
            </template>
          </PickList>
        </div>
      </div>
      <div class="p-d-flex p-jc-end p-mt-3">
        <Button label="Crear" icon="pi pi-check" class="p-mr-2" @click="createEvent" />
        <Button label="Cancelar" icon="pi pi-times" class="p-button-secondary" @click="$emit('close')" />
      </div>
    </Dialog>
  </template>
  
  <script>
  import Dialog from 'primevue/dialog'
  import InputText from 'primevue/inputtext'
  import Dropdown from 'primevue/dropdown'
  import Button from 'primevue/button'
  import PickList from 'primevue/picklist'
  
  export default {
    name: 'CreateEventModal',
    components: {
      Dialog,
      InputText,
      Dropdown,
      Button,
      PickList
    },
    data() {
      return {
        event: {
          name: '',
          type: null,
          invites: null
        },
        types: [
          { label: 'Tipo 1', value: 'tipo1' },
          { label: 'Tipo 2', value: 'tipo2' }
        ],
        invites: [
          { label: 'Invitado 1', value: 'invitado1' },
          { label: 'Invitado 2', value: 'invitado2' }
        ],
        users: [
          { name: 'Usuario 1' },
          { name: 'Usuario 2' }
        ],
        selectedUsers: [],
        guests: [
          { name: 'Invitado 1' },
          { name: 'Invitado 2' }
        ],
        selectedGuests: [],
        sourceHeader: 'Disponibles',
        targetHeader: 'Seleccionados'
      }
    },
    methods: {
      createEvent() {
        // Implementa la lógica para crear el evento
        console.log('Evento creado:', this.event, this.selectedUsers, this.selectedGuests)
        this.$emit('close')
      },
      onMoveToTarget(event) {
        console.log('Moved to target:', event.items)
      },
      onMoveToSource(event) {
        console.log('Moved to source:', event.items)
      }
    }
  }
  </script>
  
  <style scoped>
  .p-float-label {
    margin-bottom: 1rem;
  }
  </style>
  
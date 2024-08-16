<template>
  <Dialog
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{overflow: 'auto', width: '35vw'}"
    class="custom-dialog"
    :autoZIndex="true"
  >
    <template v-slot:header>
      <h4>Eventos</h4>
    </template>
    
    <template v-if="events.length === 0">
      <div class="skeleton-container">
        <div class="skeleton-item" v-for="index in 6" :key="index"></div>
      </div>
    </template>
    
    <template v-else>
      <b-row>
        <b-col v-for="event in events" :key="event.id" cols="12" class="mb-3">
          <div class="event-container">
            <div class="event-header">
              <h5>Título</h5>
            </div>
            <p>{{ event.name }}</p>
          </div>
          <div class="event-container">
            <div class="event-header">
              <h5>Localización</h5>
            </div>
            <p>{{ event.location }}</p>
          </div>
          <div class="event-container">
            <div class="event-header">
              <h5>Tipo</h5>
            </div>
            <p>{{ event.type }}</p>
          </div>
          <div class="event-container">
            <div class="event-header">
              <h5>Fechas</h5>
            </div>
            <p>{{ event.start_date }} - {{ event.end_date }}</p>
          </div>
        </b-col>
      </b-row>
    </template>

    <template #footer>
      <Button label="Guardar" icon="pi pi-check" iconPos="right" class="button-options"/>
      <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-plain" iconPos="right" @click="closeModal()"/>
    </template>
  </Dialog>
</template>


  
<script>
import Tooltip from 'primevue/tooltip';
import { getEventsbyGroup } from '../services/groups-services';

export default {
  name: 'Announcements',
  directives: {
    'tooltip': Tooltip
  },
  props: {
    visible: {
      type: Boolean,
    },
    group: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      events: [],
    };
  },
  mounted() {
    this.getEvents();
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
    async getEvents() {
      try {
        const response = await getEventsbyGroup(this.group.id);
        this.events = response.data;
        console.log(this.events);
      } catch (error) {
        console.error(error);
      }
    }
  },
  watch: {
    group: {
      handler(val) {
        if (val && Object.keys(val).length > 0) {
          this.selectedGroup = val;
        }
      },
      immediate: true
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/styles/colors';

.custom-dialog {
  .p-dialog {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  
  .p-dialog-enter-active,
  .p-dialog-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  
  .p-dialog-enter, .p-dialog-leave-to {
    opacity: 0;
    transform: scale(0.9);
  }

  .skeleton-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .skeleton-item {
    height: 1.5rem;
    background-color: #e0e0e0;
    border-radius: 4px;
    animation: pulse 1.5s infinite ease-in-out;
  }
  
  @keyframes pulse {
    0% {
      background-color: #e0e0e0;
    }
    50% {
      background-color: #c0c0c0;
    }
    100% {
      background-color: #e0e0e0;
    }
  }

  .event-container {
    margin-bottom: 1rem;
    border-bottom: solid 1px #dddddd;
    padding-bottom: 0.5rem;
  }
  
  .event-header {
    padding: 0.2rem;
    border-bottom: solid 1px #dddddd;
  }

  .button-options {
    background: $primary-color;
    color: white;
    border: none;
    border-radius: 5px;
  }
  
  .button-options:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
    background: $primary-color !important;
    cursor: pointer;
  }
}
</style>


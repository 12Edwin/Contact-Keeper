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

    <!-- Mostrar skeleton mientras se cargan los eventos -->
    <template v-if="loading">
      <div class="skeleton-container">
        <div class="skeleton-item" v-for="index in 6" :key="index"></div>
      </div>
    </template>

    <!-- Mensaje cuando no hay eventos -->
    <template v-if="!loading && localEvents.length === 0">
      <div class="text-center">
        <img src="@/assets/no_events.svg" alt="No hay eventos" class="no-events-img"/>
        <p>No hay eventos en este grupo.</p>
      </div>
    </template>

    <!-- Mostrar eventos si hay alguno -->
    <template v-else>
      <b-row>
        <b-col v-for="(event, index) in localEvents" :key="event.id" cols="12" class="mb-2">
          <div class="event-container" :class="{ 'event-container--small': index > 0 }">
            <div class="event-header">
              <h5>Título</h5>
            </div>
            <p>{{ event.name }}</p>
          </div>
          <div class="event-container" :class="{ 'event-container--small': index > 0 }">
            <div class="event-header">
              <h5>Localización</h5>
            </div>
            <p>{{ event.location }}</p>
          </div>
          <div class="event-container" :class="{ 'event-container--small': index > 0 }">
            <div class="event-header">
              <h5>Tipo</h5>
            </div>
            <p>{{ event.type }}</p>
          </div>
          <div class="event-container" :class="{ 'event-container--small': index > 0 }">
            <div class="event-header">
              <h5>Fechas</h5>
            </div>
            <p>{{ event.start_date }} - {{ event.end_date }}</p>
          </div>
        </b-col>
      </b-row>
    </template>

    <!-- Botones de acción en el footer del modal -->
    <template #footer>
      <Button label="Guardar" icon="pi pi-check" iconPos="right" class="button-options"/>
      <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-plain" iconPos="right" @click="closeModal()"/>
    </template>
  </Dialog>
</template>

<script>
import Tooltip from 'primevue/tooltip';

export default {
  name: 'EventsForGroups',
  directives: {
    'tooltip': Tooltip
  },
  props: {
    visible: {
      type: Boolean,
    },
    events: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      loading: false, 
      timer: null,
      localEvents: [] 
    };
  },
  watch: {
    visible: {
      handler(val) {
        if (val) {
          this.resetModal();
        }
      },
      immediate: true
    },
    events: {
      handler(val) {
        if (val.length > 0) {
          this.localEvents = val;
          clearTimeout(this.timer);
          this.loading = false;
        }
      },
      immediate: true
    }
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
    startTimer() {
      this.timer = setTimeout(() => {
        if (this.localEvents.length === 0) {
          this.localEvents = [];
          this.loading = false;
        }
      }, 5000); 
    },
    resetModal() {
      this.loading = true; 
      this.localEvents = []; 
      clearTimeout(this.timer); 
      this.startTimer(); 
    }
  },
  mounted() {},
  beforeDestroy() {
    clearTimeout(this.timer);
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
    margin-bottom: 0.5rem; /* Mayor margen inferior para diferenciar entre iteraciones */
    border-bottom: solid 1px #dddddd;
    padding-bottom: 0.3rem;
    transition: all 0.3s ease;
  }

  .event-container--small {
    margin-bottom: 0.9rem; /* Ajuste del margen inferior para iteraciones posteriores */
  }

  .event-header {
    padding: 0.2rem;
    margin-bottom: 0.3rem;
    font-size: 1rem;
    border-bottom: solid 1px #dddddd;
  }

  p {
    margin: 0.2rem 0; /* Ajuste del margen entre los párrafos */
    font-size: 1rem; /* Tamaño de fuente un poco más grande */
    line-height: 1.5; /* Ajustar la altura de la línea */
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



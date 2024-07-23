<template>
  <Dialog
    header="Información del Evento"
    :modal="true"
    :visible.sync="visible"
    position="center"
    :contentStyle="{ overflow: 'auto', maxWidth: '60vw' }"
    class="custom-dialog"
    :autoZIndex="true"
    :baseZIndex="1000"
  >
    <div class="event-info">
      <div class="event-header text-center">
        <Avatar :label="getInitials(eventData.event)" shape="circle" size="xlarge" class="mb-2 mx-auto" />
        <h2 class="event-title">{{ eventData.event }}</h2>
      </div>
      <div class="event-details">
        <b-row>
          <b-col cols="12" lg="6">
            <div class="event-detail">
              <i class="pi pi-calendar"></i>
              <div class="detail-text">
                <label>Fechas</label>
                <p>{{ formatDates(eventData.startDate, eventData.endDate) }}</p>
              </div>
            </div>
          </b-col>
          <b-col cols="12" lg="6">
            <div class="event-detail">
              <i class="pi pi-tag"></i>
              <div class="detail-text">
                <label>Tipo de evento</label>
                <p>{{ eventData.type }}</p>
              </div>
            </div>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" lg="6">
            <div class="event-detail">
              <i class="pi pi-users"></i>
              <div class="detail-text">
                <label>Participantes</label>
                <p>{{ eventData.participants }}</p>
              </div>
            </div>
          </b-col>
          <b-col cols="12" lg="6">
            <div class="event-detail">
              <i class="pi pi-info-circle"></i>
              <div class="detail-text">
                <label>Descripción</label>
                <p>{{ eventData.description }}</p>
              </div>
            </div>
          </b-col>
        </b-row>
      </div>
    </div>
    <template #footer>
      <Button label="Cerrar" icon="pi pi-times" style="color: gray;" class="p-button-text" @click="closeModal()" />
    </template>
  </Dialog>
</template>

<script>
import Avatar from 'primevue/avatar';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import 'primeicons/primeicons.css';

export default {
  name: 'ModalEventInfo',
  components: {
    Avatar,
    Dialog,
    Button,
  },
  props: {
    event: {
      type: Object,
      required: true,
    },
    visible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      eventData: {
        event: '',
        description: '',
        startDate: '',
        endDate: '',
        type: '',
        participants: '',
      },
    };
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
    getInitials(text) {
      if (!text) return '';
      return text.split(' ').map(word => word.charAt(0)).join('').toUpperCase();
    },
    formatDates(start, end) {
      return `${this.formatCalendarDate(start)} - ${this.formatCalendarDate(end)}`;
    },
    formatCalendarDate(date) {
      return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    },
  },
  watch: {
    event: {
      handler(val) {
        if (val && Object.keys(val).length > 0) {
          this.eventData = {
            event: val.title || '',
            description: val.description || '',
            startDate: val.start || '',
            endDate: val.end || '',
            type: val.type || '',
            participants: val.participants || '',
          };
        } else {
          this.eventData = {
            event: '',
            description: '',
            startDate: '',
            endDate: '',
            type: '',
            participants: '',
          };
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.event-info {
  padding: 1rem;
}

.event-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.event-title {
  margin-top: 0.5rem;
}

.event-details {
  margin-top: 1rem;
}

.event-detail {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.event-detail i {
  font-size: 2rem;
  margin-right: 1rem;
}

.detail-text {
  flex: 1;
}

.detail-text label {
  font-weight: bold;
}

.detail-text p {
  margin: 0.5rem 0;
}

.text-center {
  text-align: center;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.p-button-text{
  color: #333;
}
</style>

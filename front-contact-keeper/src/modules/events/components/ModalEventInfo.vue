<template>
  <Dialog
    header="Información del Evento"
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{ overflow: 'auto', maxWidth: '35vw' }"
    class="custom-dialog"
    :autoZIndex="true"
    :baseZIndex="1000"
  >
    <template v-slot:header>
      <h4>{{event.name}}</h4>
    </template>
    <template>
            <b-row>
              <b-col cols="12" class="mb-3">
                <div class="event-header">
                  <h5>Título</h5>
                </div>
              </b-col>
              <b-col cols="12" class="mb-3">
                <p>{{event.title ? event.title : 'Sin título'}}</p>
              </b-col>
              <b-col cols="12" class="mb-3">
                <div class="event-header">
                  <h5>Información</h5>
                </div>
              </b-col>
              <b-col cols="12" class="mb-2">
                <p>{{event.description}}</p>
              </b-col>
              <b-col cols="12" class="mb-3">
                <p>{{splitDate(event.start_date).date}} - {{ splitDate(event.end_date).date }}</p>
                <p>{{ splitDate(event.start_date).time }} - {{ splitDate(event.end_date).time }}</p>
                <p>{{eventType(event.type)}}</p>
              </b-col>
              <b-col cols="12" class="mb-3">
                <div class="event-header">
                  <h5>Ubicación</h5>
                </div>
              </b-col>
              <b-col cols="12" class="mb-3">
                <p>{{event.location}}</p>
              </b-col>
            </b-row>
          </template>
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
import utils from '@/kernel/utils';
import TabView from 'primevue/tabview/TabView';
import TabPanel from 'primevue/tabpanel/TabPanel';
import ScrollPanel from 'primevue/scrollpanel/ScrollPanel';

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
      eventData: {},
    };
  },
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
    splitDate(date){
      return utils.splitDateTime(date);
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
    eventType(type){
      if(type === 'meeting'){
        return 'Reunión'
      } else if(type === "session"){
        return 'Sesión'
      } else if(type === "event"){
        return 'Evento'
      }else{
        return 'Otro'
      }
    }
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
  padding: 0.2rem;
  border-bottom: solid 1px #dddddd;
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

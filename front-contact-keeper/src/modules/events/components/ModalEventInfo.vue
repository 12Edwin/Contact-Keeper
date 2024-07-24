<template>
  <Dialog
      header="Información del Evento"
      :modal="true"
      :closeOnEscape="false"
      :closable="false"
      :visible.sync="visible"
      position="center"
      :contentStyle="{ overflow: 'visible', width: '35vw' }"
      class="custom-dialog"
      :autoZIndex="true"
  >
    <div class="user-info">
      <Avatar :label="eventData.event.charAt(0)" shape="circle" size="xlarge" class="mb-2" />
      <h3>{{ eventData.event }}</h3>
    </div>
    <div class="user-data">
      <b-row>
        <b-col cols="12" lg="6" md="4" sm="12" class="ml-2">
          <div class="info-item">
            <i class="pi pi-envelope"></i>
            <div class="info-text">
              <label>Fechas</label>
              <p>{{ eventData.startDate }} - {{ eventData.endDate }}</p>
            </div>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6" md="4" sm="12" class="ml-2">
          <div class="info-item">
            <i class="pi pi-envelope"></i>
            <div class="info-text">
              <label>Tipo de evento</label>
              <p>{{ eventData.type }}</p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" lg="6" md="4" sm="12">
          <div class="info-item">
            <i class="pi pi-phone"></i>
            <div class="info-text">
              <label>Participantes</label>
              <p>{{ eventData.participants }}</p>
            </div>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" lg="6" md="4" sm="12" class="ml-2">
          <div class="info-item">
            <i class="pi pi-envelope"></i>
            <div class="info-text">
              <label>Descripción</label>
              <p>{{ eventData.description }}</p>
            </div>
          </div>
        </b-col>
      </b-row>
    </div>
    <template #footer>
      <Button
          label="Cerrar"
          icon="pi pi-times"
          class="p-button-text"
          @click="closeModal()"
      />
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
  methods: {
    closeModal() {
      this.$emit('update:visible', false);
    },
  },
  watch: {
    event: {
      handler(val) {
        if (val && Object.keys(val).length > 0) {
          this.eventData = val;
        }
      },
      immediate: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/styles/colors.scss';

.user-info {
  text-align: center;
  padding: 1rem;
}

.user-info h3 {
  margin: 0.2rem 0 1rem;
}

.user-info p {
  margin: 0.25rem 0;
}
.user-data {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 1.3rem;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.info-item i {
  font-size: 20px;
  color: $sidebar-items;
  margin-right: 10px;
}

.info-text {
  display: flex;
  flex-direction: column;
}

.info-text label {
  font-weight: bold;
  margin: 0;
}

.info-text p {
  margin: 0;
}
</style>
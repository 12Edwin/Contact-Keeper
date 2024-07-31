<template>
  <Dialog
      header="Información del usuario"
      :modal="true"
      :closeOnEscape="false"
      :closable="false"
      :visible.sync="visible"
      position="center"
      :contentStyle="{overflow: 'visible', width: '35vw'}"
      class="custom-dialog"
      :autoZIndex="true"
  >
    <div class="user-info">
      <Avatar :label="userData.name.charAt(0)" shape="circle" size="xlarge" class="mb-2"/>
      <h3>{{ userData.name }}</h3>
    </div>
    <div class="user-data">
      <b-row>
        <b-col cols="12" lg="6" md="4" sm="12" class="ml-2">
          <div class="info-item">
            <i class="pi pi-envelope"></i>
            <div class="info-text">
              <label>Correo electrónico</label>
              <p>{{ userData.email }}</p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" lg="6" md="4" sm="12">
          <div class="info-item">
            <i class="pi pi-phone"></i>
            <div class="info-text">
              <label>Número de teléfono</label>
              <p>7775673712</p>
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
import Panel from 'primevue/panel'
import Avatar from 'primevue/avatar'
import Dialog from "primevue/dialog";

export default {
  name: 'UserInfo',
  components: {
    Panel,
    Avatar,
    Dialog
  },
  data(){
    return {
      userData: {
        name: '',
        email: '',
        phone: ''
      }
    }
  },
  props: {
    user: {
      type: Object
    },
    visible: {
      type: Boolean,
      required: true
    },
  },
  methods: {
    closeModal(){
      this.$emit('update:visible', false);
    }
  },
  watch: {
    user: {
      handler: function (val) {
        if(val && Object.keys(val).length > 0){
          this.userData = val;
        }
      },
      immediate: true
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/colors';

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
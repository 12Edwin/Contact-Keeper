<template>
  <div>
    <Dialog
        header="Información del usuario"
        :modal="true"
        :closeOnEscape="false"
        :closable="true"
        :visible.sync="visible"
        position="center"
        :contentStyle="{overflow: 'visible'}"
        class="custom-dialog"
        :autoZIndex="true"
    >
      <div class="user-info">
        <Avatar :label="user.name.charAt(0)" shape="circle" size="xlarge"/>
        <h3>{{ user.name }}</h3>
        <p><strong>Correo electrónico:</strong> {{ user.email }}</p>
        <p><strong>Número de teléfono:</strong> 7775743812</p>
      </div>
    </Dialog>
  </div>
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
  props: {
    user: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      required: true
    },
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
.user-info {
  text-align: center;
  padding: 2rem;
}

.user-info h3 {
  margin: 0.5rem 0 1rem;
}

.user-info p {
  margin: 0.25rem 0;
}
</style>
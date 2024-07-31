<template>
  <Dialog
      :modal="true"
      :closeOnEscape="false"
      :closable="false"
      :visible.sync="visible"
      position="center"
      :contentStyle="{overflow: 'visible', width: '35vw'}"
      class="custom-dialog"
      :autoZIndex="true"
  >
    <template v-slot:header>
      <h4>{{selectedGroup.name}}</h4>
    </template>
    <template>
      <b-row>
        <b-col cols="12" class="mb-3">
          <div class="user-list-header">
            <h5>Integrantes</h5>
          </div>
        </b-col>
        <b-col cols="12" v-for="(member, userIndex) in selectedGroup.members" :key="userIndex" class="mb-2">
          <div class="user-list d-flex justify-content-between align-items-center">
            <div class="user-info-container d-flex align-items-center">
              <Avatar :label="member.name.charAt(0)" shape="circle" size="small"/>
              <div class="user-info">
                <label class="username">{{ member.name }}</label>
                <p class="role">{{ member.role }}</p>
              </div>
            </div>
            <div class="icon-container">
              <i class="pi pi-minus-circle icon-styles" v-tooltip.right="'Expulsar'"></i>
            </div>
          </div>
        </b-col>
      </b-row>
    </template>
    <template #footer>
      <Button  label="Guardar" icon="pi pi-check"  iconPos="right" class="button-options"/>
      <Button  label="Cancelar" icon="pi pi-times" class="p-button-text p-button-text p-button-plain" iconPos="right" @click="closeModal()"/>
    </template>
  </Dialog>
</template>

<script>
import Tooltip from 'primevue/tooltip';
export default {
  name: 'Announcements',
  directives:{
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
  data(){
    return {
      selectedGroup :{
        name: '',
        description: '',
        members: [
          {
            name: '',
            role: ''
          }
        ]
      }
    }
  },
  methods: {
    closeModal(){
      this.$emit('update:visible', false);
    }
  },
  watch: {
    group: {
      handler: function (val) {
        if(val && Object.keys(val).length > 0){
          this.selectedGroup = val;
        }
      },
      immediate: true
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/colors';
.info-group {
  text-align: center;
  padding: 1rem;
}

.user-list-header {
  padding: 0.2rem;
  border-bottom: solid 1px #dddddd;
}

.user-list {
  border-bottom: solid 1px #dddddd;
  display: flex;
  align-items: center;
  padding: 0.2rem;
  width: 100%;
}

.user-info-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.username {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.role {
  margin: 0;
  font-size: 13px;
  color: #555;
}

.icon-container {
  background: transparent;
  margin-right: 15px;
}

.pi-minus-circle {
  font-size: 16px;
  color: #555;
  cursor: pointer;
}

.button-options {
  background: $primary-color;
  color: white;
  border: none;
  border-radius: 5px;
}

.button-options:hover{
  border-radius: 5px;
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
  background: $primary-color !important;
  border: none;
  cursor: pointer;
}

</style>
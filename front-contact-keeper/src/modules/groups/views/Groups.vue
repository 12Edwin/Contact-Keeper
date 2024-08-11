<template>
  <div class="main-content">
    <div class="content">
      <Panel header="Grupos" class="shadow-lg">
        <div class="p-1">
          <template>
            <b-row>
              <b-col class="d-flex justify-content-between align-content-between mb-3">
                <span class="p-input-icon-right">
                  <i class="pi pi-search"/>
                  <InputText type="text" placeholder="Buscar..."/>
                </span>
                <Button
                    class="button-options"
                    label="Nuevo grupo"
                    iconPos="right"
                    icon="pi pi-sitemap"
                />
              </b-col>
            </b-row>
          </template>
          <template>
            <b-row class="mt-2">
              <b-col  cols="12" lg="4" md="6" v-for="(group, index) in groups" :key="index">
                <template>
                  <div class="card mb-4">
                    <div class="card-header">
                      <div class="card-header-text">
                        <h2>{{group.name}}</h2>
                        <p>Mayo-Agosto 2024</p>
                        <p>Miguel Rosemberg</p>
                      </div>
                      <Avatar :label="getInitial(group.name)" shape="circle" size="xlarge" class="card-header-image"/>
                    </div>
                    <div class="card-footer">
                      <i class="pi pi-megaphone icon-camera" v-tooltip.top="'Anuncios'" ></i>
                      <i class="pi pi-info-circle icon-folder" v-tooltip.top="'Información'" @click="openInfoModal(group)"></i>
                    </div>
                  </div>
                </template>
              </b-col>
            </b-row>
          </template>
          <Announcements :group="groupSelected" :visible.sync="showInfo"/>
        </div>
      </Panel>
    </div>
  </div>
</template>

<script>
import BadgeDirective from 'primevue/badgedirective';
import Tooltip from 'primevue/tooltip';
import Announcements from "@/modules/groups/components/GroupInfo.vue";
import groupService from '../services/groups-services';

export default {
  name: 'Groups',
  directives:{
    'badge': BadgeDirective,
    'tooltip': Tooltip
  },
  components: {
    Announcements
  },
  data() {
    return {
      groups: [],
      showInfo: false,
      groupSelected: {}
    }
  },
  mounted() {
    this.getAllGroups();
  },
  methods: {
    getInitial(name){
      const initials = name.split(' ');
      return initials.length > 1 ? initials[0].charAt(0) + initials[1].charAt(0) : initials[0].charAt(0);
    },
    openInfoModal(group){
      this.groupSelected = JSON.parse(JSON.stringify(group));
      this.showInfo = true;
    },
    getAllGroups() {
      groupService.getAllGroups()
        .then(response => {
          this.groups = response.data;
        })
        .catch(error => {
          console.error('Error al obtener grupos:', error);
        });
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/colors';
.content {
  flex: 1;
  padding: 1rem;
  transition: margin-left 0.3s;
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

.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card:hover{
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
  cursor: pointer;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header-text {
  max-width: 70%;
}

.card-header-image {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.card-footer {
  display: flex;
  justify-content: right;
  margin-top: 16px;
}

.icon-camera,
.icon-folder {
  font-size: 20px;
  cursor: pointer;
  margin-top: 5px;
}

.icon-camera {
  margin-right: 16px;
}

</style>
<template>
  <div class="main-content">
    <div class="content">
      <Panel header="Grupos" class="shadow-lg">
        <div class="p-1">
          <!-- Contenido de la barra de búsqueda y botón de nuevo grupo -->
          <b-row>
            <b-col class="d-flex justify-content-between align-content-between mb-3">
              <span class="p-input-icon-right">
                <i class="pi pi-search"/>
                <InputText type="text" placeholder="Buscar..." v-model="searchQuery"/>
              </span>
            </b-col>
            <b-col class="d-flex justify-content-end mb-3">
              <Button
                class="button-options"
                label="Nuevo grupo"
                iconPos="right"
                icon="pi pi-sitemap"
                @click="openSaveModal"
              />
            </b-col>
          </b-row>

          <!-- Skeleton Loader -->
          <template v-if="isLoading">
            <b-row>
              <b-col cols="12" lg="4" md="6" v-for="n in 3" :key="n">
                <div class="card skeleton mb-4">
                  <div class="card-header">
                    <div class="card-header-text">
                      <div class="skeleton-text skeleton-title"></div>
                      <div class="skeleton-text skeleton-subtitle"></div>
                      <div class="skeleton-text skeleton-subtitle"></div>
                    </div>
                    <div class="skeleton-image"></div>
                  </div>
                </div>
              </b-col>
            </b-row>
          </template>

          <!-- Contenido Real -->
          <template v-else>
            <b-row class="mt-2">
              <b-col cols="12" lg="4" md="6" v-for="(group, index) in filteredGroups" :key="index">
                <div class="card mb-4">
                  <div class="card-header">
                    <div class="card-header-text">
                      <h2>{{ group.name }}</h2>
                      <p>{{ group.title }}</p>
                      <p>
                        <span :class="['custom-badge', getBadgeClass(group.status)]">
                          {{ translateStatus(group.status) }}
                        </span>
                      </p>
                    </div>
                    <Avatar :label="getInitial(group.name)" shape="circle" size="xlarge" class="card-header-image"/>
                  </div>
                  <div class="card-footer">
                    <i class="pi pi-trash icon-folder-end" v-tooltip.top="'Eliminar'" @click="deleteGroup(group)"></i>
                    <i class="pi pi-pencil icon-folder" v-tooltip.top="'Editar'" @click="openEditModal(group)"></i>
                    <i class="pi pi-calendar icon-folder" v-tooltip.top="'Eventos'" @click="openModalGetEvents(group)"></i>
                    <i class="pi pi-info-circle icon-folder" v-tooltip.top="'Información'" @click="openInfoModal(group)"></i>
                  </div>
                </div>
              </b-col>
            </b-row>
          </template>

          <!-- Componentes Modales y de Anuncios -->
          <Announcements :group="groupSelected" :visible.sync="showInfo" @update-data="getGroups"/>
          <ModalCreateGroup :visible.sync="showModalSave" @update-data="getGroups"/>
          <ModalEditGroup :visible.sync="showModalEdit" :groupData="groupSelected" @update-data="getGroups"/>
          <EventsForGroups :group="groupSelected" :events="events" :visible.sync="showModalEvents" @addNewMessages="addNewMessages"/>
        </div>
      </Panel>
    </div>
  </div>
</template>


<script>
import BadgeDirective from 'primevue/badgedirective';
import Tooltip from 'primevue/tooltip';
import Announcements from "@/modules/groups/components/GroupInfo.vue";
import ModalCreateGroup from '../components/ModalSaveGroup.vue';
import ModalEditGroup from '../components/ModalEditGroup.vue';
import EventsForGroups from '../components/EventsForGroups.vue';
import {getGroupsByUserId, deleteGroup, getEventsbyGroup } from '../services/groups-services';
import { onQuestion, onToast } from '@/kernel/alerts';

export default {
  name: 'Groups',
  directives:{
    'badge': BadgeDirective,
    'tooltip': Tooltip
  },
  components: {
    Announcements,
    ModalCreateGroup,
    ModalEditGroup,
    EventsForGroups
  },
  data() {
    return {
      groups: [],
      events: [],
      showInfo: false,
      isLoading: true,
      groupSelected: {},
      showModalSave: false,
      showModalEdit: false,
      showModalEvents: false,
      searchQuery: '',
      idGroup: 0
    }
  },
  mounted() {
    this.getGroups();
  },
  methods: {
    getInitial(name){
      if(!name){
        return ''
      }else{
        const initials = name.split(' ');
        return initials.length > 1 ? initials[0].charAt(0) + initials[1].charAt(0) : initials[0].charAt(0);
      };
    },
    getBadgeClass(status) {
      switch (status.toLowerCase()) {
        case 'pending':
          return 'badge-secondary'; 
        case 'approved':
          return 'badge-success'; 
        case 'rejected':
          return 'badge-danger'; 
        default:
          return 'badge-primary';
      }
    },
    translateStatus(status) {
      const translations = {
        pending: 'Pendiente',
        approved: 'Aprobado',
        rejected: 'Rechazado'
      };
      return translations[status.toLowerCase()] || 'Desconocido'; 
    },
    openInfoModal(group){
      this.groupSelected = JSON.parse(JSON.stringify(group));
      this.showInfo = true;
    },
    openSaveModal(){
      this.showModalSave = true;
    },
    openEditModal(group){
      this.groupSelected = JSON.parse(JSON.stringify(group));
      this.showModalEdit = true;
    },
    addNewMessages(group){
      const index = this.groups.findIndex(g => g.id === group.id);
      this.groups[index].messages = group.messages;
    },
    async openModalGetEvents(group){
      this.groupSelected = JSON.parse(JSON.stringify(group));
      
      try {
        onToast('info', 'Cargando eventos', 'info');
        this.showModalEvents = true;
        const response = await getEventsbyGroup(this.groupSelected.id);

        if (response.status === 'success') {
          this.events = response.data;
        } else {
          this.events = [];
        }
      } catch (error) {
        this.events = []; 
      }
    },
    async getGroups() {
      this.isLoading = true;
        try {
          const response = await getGroupsByUserId();
          this.groups = response.data;
          this.isLoading = false;
        } catch (error) {
          this.isLoading = false;
      }
    },
    async deleteGroup(group){
      try {
        let question = await onQuestion('¿Estás seguro de eliminar este grupo?');
        if(question === true){
          onToast('info', 'Eliminando grupo', 'info');
          const response = await deleteGroup(group.id);
          if(response.status === 200 || response.status === 201 || response.status === "success"){
            this.getGroups();
            onToast('success', 'Grupo eliminado correctamente', 'success');
          }
        }
      } catch (error) {
      }
    }
  },
  computed: {
    filteredGroups() {
      const query = this.searchQuery.toLowerCase();
      return this.groups.filter(group => {
        return group.name.toLowerCase().includes(query) ||
              group.title.toLowerCase().includes(query);
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
  justify-content: flex-end;
  margin-top: 16px;
  gap: 5px;
  flex-wrap: wrap;
}

.icon-camera,
.icon-folder {
  font-size: 20px;
  cursor: pointer;
  margin-top: 5px;
}

.icon-folder-end {
  font-size: 20px;
  cursor: pointer;
  margin-top: 5px;
}

.icon-camera {
  margin-right: 16px;
}

.skeleton {
  background-color: #faf9f9;
  border-radius: 4px;
  margin-bottom: 10px;
  position: relative;
  overflow: hidden;
}

.skeleton:after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(245, 245, 245, 0.8) 25%, rgba(220, 220, 220, 0.8) 50%, rgba(245, 245, 245, 0.8) 75%);
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.skeleton-text {
  background-color: #faf9f9;
  border-radius: 4px;
  margin-bottom: 10px;
}

.skeleton-title {
  height: 24px;
  width: 70%;
}

.skeleton-text {
  animation: skeletonAnimation 1s infinite;
}
.skeleton-subtitle {
  height: 16px;
  width: 50%;
}

.skeleton-image {
  background-color: #e0e0e0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.custom-badge {
  display: inline-block;
  padding: 0.25em 0.4em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;
  color: #fff; /* Default text color */
}

.badge-secondary {
  background-color: #6c757d;
}

.badge-success {
  background-color: #28a745;
}

.badge-danger {
  background-color: #dc3545;
}

.badge-primary {
  background-color: #007bff;
}

</style>
<template>
  <Dialog
    header="Nuevo Evento"
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{ overflow: 'visible', width: '70vw' }"
    class="custom-dialog"
    :autoZIndex="true"
  >
    <div class="p-fluid grid">
      <b-row>
        <b-col cols="12" lg="4" md="6" sm="12">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-bookmark"/>
              <InputText id="field-event-title" v-model="v$.title.$model" :class="{ 'invalid-field-custom': v$.title.$error }" />
              <label for="field-event-title" class="form-label-required">Título</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.required.$invalid">
                {{ v$.title.required.$message }}
              </p>
              <p class="error-messages"
                 v-if="v$.title.$dirty && v$.title.onlyLetters.$invalid">
                {{ v$.title.onlyLetters.$message }}
              </p>
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.minLength.$invalid">
                {{ v$.title.minLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.title.$dirty && v$.title.maxLength.$invalid">
                {{ v$.title.maxLength.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" lg="4" md="6" sm="12">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <Dropdown id="field-event-type" v-model="v$.type.$model" :options="types" optionLabel="label"  optionValue="value"/>
              <label for="field-event-type" class="form-label-required">Tipo</label>
            </span>
          </div>
        </b-col>
        <b-col cols="12" lg="4" md="6" sm="12">
          <span class="p-float-label p-input-icon-right">
              <i class="pi pi-map-marker"/>
              <InputText id="field-event-location" v-model="v$.location.$model" :class="{ 'invalid-field-custom': v$.location.$error }" />
              <label for="field-event-location" class="form-label-required">Ubicación</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages"
                 v-if="v$.location.$dirty && v$.location.onlyLetters.$invalid">
                {{ v$.location.onlyLetters.$message }}
              </p>
              <p class="error-messages" v-if="v$.location.$dirty && v$.location.maxLength.$invalid">
                {{ v$.location.maxLength.$message }}
              </p>
            </div>
        </b-col>
        <b-col cols="12" lg="3" md="6" sm="12" class="mt-2">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-info"/>
              <InputText id="field-event-title" v-model="v$.name.$model" :class="{ 'invalid-field-custom': v$.name.$error }" />
              <label for="field-event-title" class="form-label-required">Nombre</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.required.$invalid">
                {{ v$.name.required.$message }}
              </p>
              <p class="error-messages"
                 v-if="v$.name.$dirty && v$.name.onlyLetters.$invalid">
                {{ v$.name.onlyLetters.$message }}
              </p>
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.minLength.$invalid">
                {{ v$.name.minLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.name.$dirty && v$.name.maxLength.$invalid">
                {{ v$.name.maxLength.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" lg="3" md="6" sm="12" class="mt-2">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-calendar"/>
              <Calendar v-model="v$.dates.$model" selectionMode="range" dateFormat="yy/mm/dd"/>
              <label for="field-event-dates" class="form-label-required">Duración</label>
            </span>
          </div>
        </b-col>
        <b-col cols="12" lg="3" md="6" sm="12" class="mt-2">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-clock"></i>
              <Calendar id="field-event-start" v-model="v$.startHour.$model" :class="{ 'invalid-field-custom': v$.startHour.$error }" :timeOnly="true" hourFormat="12"/>
              <label for="field-event-start" class="form-label-required">Hora inicio</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.startHour.$dirty && v$.startHour.required.$invalid">
              {{ v$.startHour.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.startHour.$dirty && v$.startHour.isBeforeEnd.$invalid">
              {{ v$.startHour.isBeforeEnd.$message }}
              </p>
              <p class="error-messages" v-if="v$.startHour.$dirty && v$.startHour.notEqualEnd.$invalid">
              {{ v$.startHour.notEqualEnd.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" lg="3" md="12" sm="12" class="mt-2">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-clock"></i>
              <Calendar id="field-event-end" v-model="v$.endHour.$model" :timeOnly="true" hourFormat="12" :class="{ 'invalid-field-custom': v$.startHour.$error }"/>
              <label for="field-event-end" class="form-label-required">Hora fin</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.endHour.$dirty && v$.endHour.required.$invalid">
              {{ v$.endHour.required.$message }}
              </p>
              <p class="error-messages" v-if="v$.endHour.$dirty && v$.endHour.isAfterStart.$invalid">
              {{ v$.endHour.isAfterStart.$message }}
              </p>
              <p class="error-messages" v-if="v$.endHour.$dirty && v$.endHour.notEqualStart.$invalid">
                {{ v$.endHour.notEqualStart.$message }} 
              </p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" class="mt-2">
          <div class="field">
            <span class="p-float-label p-input-icon-right">
              <Textarea id="field-event-description" rows="2" cols="30" v-model="v$.description.$model" :class="{ 'invalid-field-custom': v$.description.$error }" />
              <label for="field-event-description" class="form-label-required">Descripción</label>
            </span>
            <div class="text-danger text-start pt-2">
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.required.$invalid">
                {{ v$.description.required.$message }}
              </p>
              <p class="error-messages"
                 v-if="v$.description.$dirty && v$.description.onlyLetters.$invalid">
                {{ v$.description.onlyLetters.$message }}
              </p>
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.minLength.$invalid">
                {{ v$.description.minLength.$message }}
              </p>
              <p class="error-messages" v-if="v$.description.$dirty && v$.description.maxLength.$invalid">
                {{ v$.description.maxLength.$message }}
              </p>
            </div>
          </div>
        </b-col>
        <b-col cols="12" class="mt-1">
          <TabView >
            <TabPanel header="Usuarios">
              <ScrollPanel style="width: 100%; height: 160px">
                <template v-if="!isLoading">
                  <template v-if="invites.length > 0">
                    <div class="user-list d-flex justify-content-between align-items-center" v-for="(member, userIndex) in invites" :key="userIndex">
                      <div class="user-info-container d-flex align-items-center mb-2">
                        <Avatar :label="member.name.charAt(0)" shape="circle" size="small"/>
                        <div class="user-info">
                          <label class="username">{{ member.name }} {{ member.surname }} {{ member.last_name }}</label>
                          <p class="role">{{ member.email }}</p>
                        </div>
                      </div>
                      <div class="icon-container">
                        <b-form-checkbox :binary="true" @change="onCheckboxUserChange(member)" :checked="ifUserSelected(member)"/>
                      </div>
                    </div>
                  </template>
                <template v-else>
                  <div class="no-events-img">
                    <img src="@/assets/User_empty.svg" alt="Sin usuarios" style="width: 120px; height: 120px;"/>
                      <p class="no-events-text">Sin usuarios</p>
                  </div>
                </template>
                </template>
                <template v-else>
                  <div class="custom-skeleton">
                    <ul class="m-0 p-0">
                      <li class="mb-3">
                        <div class="flex">
                          <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                          <div style="flex: 1">
                            <Skeleton width="100%" class="mb-2"></Skeleton>
                            <Skeleton width="75%"></Skeleton>
                          </div>
                        </div>
                      </li>
                      <li class="mb-3">
                        <div class="flex">
                          <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                          <div style="flex: 1">
                            <Skeleton width="100%" class="mb-2"></Skeleton>
                            <Skeleton width="75%"></Skeleton>
                          </div>
                        </div>
                      </li>
                      <li class="mb-3">
                        <div class="flex">
                          <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                          <div style="flex: 1">
                            <Skeleton width="100%" class="mb-2"></Skeleton>
                            <Skeleton width="75%"></Skeleton>
                          </div>
                        </div>
					            </li>
                    </ul>
                  </div>
                </template>
              </ScrollPanel>
            </TabPanel>
            <TabPanel header="Grupos">
              <ScrollPanel style="width: 100%; height: 160px;">
                <template v-if="!isLoading">
                  <template v-if="groups.length > 0">
                    <div class="user-list d-flex justify-content-between align-items-center" v-for="(group, userIndex) in groups" :key="userIndex">
                      <div class="user-info-container d-flex align-items-center mb-2">
                        <Avatar :label="group.name.charAt(0)" shape="circle" size="small"/>
                        <div class="user-info">
                          <label class="username">{{ group.name }}</label>
                          <p class="role">{{ eventStatus(group.status) }}</p>
                        </div>
                      </div>
                      <div class="icon-container">
                        <b-form-checkbox :binary="true" @change="onCheckboxGroupChange(group)" :checked="ifGroupSelected(group)"/>
                      </div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="no-events-img">
                      <img src="@/assets/inbox_empty.svg" alt="Sin usuarios" style="width: 120px; height: 120px;"/>
                        <p class="no-events-text">Sin grupos</p>
                    </div>
                  </template>
                </template>
                <template v-else>
                  <div class="custom-skeleton">
                    <ul class="m-0 p-0">
                      <li class="mb-3">
                        <div class="flex">
                          <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                          <div style="flex: 1">
                            <Skeleton width="100%" class="mb-2"></Skeleton>
                            <Skeleton width="75%"></Skeleton>
                          </div>
                        </div>
                      </li>
                      <li class="mb-3">
                        <div class="flex">
                          <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                          <div style="flex: 1">
                            <Skeleton width="100%" class="mb-2"></Skeleton>
                            <Skeleton width="75%"></Skeleton>
                          </div>
                        </div>
                      </li>
                      <li class="mb-3">
                        <div class="flex">
                          <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
                          <div style="flex: 1">
                            <Skeleton width="100%" class="mb-2"></Skeleton>
                            <Skeleton width="75%"></Skeleton>
                          </div>
                        </div>
					            </li>
                    </ul>
                  </div>
                </template>
              </ScrollPanel>
            </TabPanel>
          </TabView>
        </b-col>
      </b-row>
    </div>
    <template #footer>
      <Button label="Guardar" icon="pi pi-check" style="background-color: black; color: white;" class="p-button-text" @click="saveEvent" />
      <Button label="Cancelar" icon="pi pi-times" style="color: gray;" class="p-button-text" @click="closeModal" />
    </template>
  </Dialog>
</template>

<script>
import { ref, reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, helpers, maxLength, minLength } from '@vuelidate/validators';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import {phraseRegex} from "@/kernel/patterns.js";
import Textarea from 'primevue/textarea/Textarea';
import ScrollPanel from 'primevue/scrollpanel/ScrollPanel';
import groupService from '@/modules/groups/services/groups-services';
import userServices from '@/modules/users/services/userServices';
import utils from '@/kernel/utils';
import Calendar from '../views/Calendar.vue';
import eventServices from '../services/event-services';
export default {
  name: 'ModalAddEvent',
  components: {
    Dialog,
    Button,
    Dropdown,
    InputText
  },
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      types: [
        { label: 'Reunión', value: 'meeting' },
        { label: 'Sesión', value: 'session' },
        {label: 'Cumpleaños', value: 'birthday'},
        {label: 'Otro', value: 'other'}
      ],
      invites: [
        // { name: 'Merri Chrismas', email: '20213tn103@utez.edu.mx' },
        // { name: 'Isa Palacios', email: '20213tn103@utez.edu.mx' },
        // { name: 'Typescrips', email: '20203tn103@utez.edu.mx' }

      ],
      groups: [
        // { name: 'Grupo 1', status: 'active' },
        // { name: 'Grupo 2', status: 'pending' },
        // { name: 'Grupo 3', status: 'active' }
      ],
      isLoading: false,
      today: new Date().toISOString().split('T')[0]
    };
  },
  setup() {
    const eventData = reactive({
      title: '',
      description: '',
      dates: null,
      type: null,
      participants: null,
      location: '',
      startHour: '',
      endHour: '',
      name: '',
      id_group_member: ''
    });

    const rules = {
      title: {
        required: helpers.withMessage('El título del evento es requerido', required),
        onlyLetters: helpers.withMessage('El título solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("El título debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El título debe tener máximo de 30 caracteres", maxLength(30)),
      },
      name: {
        required: helpers.withMessage('El nombre del evento es requerido', required),
        onlyLetters: helpers.withMessage('El nombre solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El nombre debe tener máximo de 30 caracteres", maxLength(30)),
      },
      description: {
        required: helpers.withMessage('La descripción es requerida', required),
        onlyLetters: helpers.withMessage('La descripción solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("La descripción debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("La descripción debe tener máximo 70 caracteres", maxLength(100))
      },
      dates: {
        required: helpers.withMessage('La fecha de inicio del evento es requerida', required),
      },
      type: {
        required: helpers.withMessage('El tipo de evento es requerido', required),
      },
      participants: {
        required: helpers.withMessage('Debes seleccionar al menos un ', required),
      },
      dates: {
        required: helpers.withMessage('La fecha de inicio y de fin son requeridos', required),
      },
      location: {
        onlyLetters: helpers.withMessage('El npmbre del lugar solo pueden contener letras y números', (value) => phraseRegex.test(value)),
        maxLength: helpers.withMessage("El nombre del lugar debe tener máximo 70 caracteres", maxLength(70))
      },
      startHour: {
        required: helpers.withMessage('La hora de inicio es requerida', required),
        isBeforeEnd: helpers.withMessage('La hora de inicio debe ser menor a la hora de fin', (value) => utils.startAfterEnd(value, eventData.endHour)),
        notEqualEnd: helpers.withMessage('La hora de inicio no puede ser igual a la hora de fin', (value) => !utils.isSameDate(value, eventData.endHour))
      },
      endHour: {
        required: helpers.withMessage('La hora de fin es requerida', required),
        isAfterStart: helpers.withMessage('La hora de fin debe ser mayor a la hora de inicio', (value) => utils.endBeforeStart(eventData.startHour, value)),
        notEqualStart: helpers.withMessage('La hora de fin no puede ser igual a la hora de inicio', (value) => !utils.isSameDate(eventData.startHour, value))
      }
    };

    const v$ = useVuelidate(rules, eventData);
    return {eventData, v$}
  },
  methods:{
    closeModal(){
      this.$emit('update:visible', false);
    },

    async saveEvent() {
      const event = this.prepareObject()
      console.log("desde el save event", event)
      const {id_group_member} = event
      try {
        if(id_group_member){
          const response = await eventServices.saveGroupEvent(event)
          if(response){
            if(response.status === "success"){
              console.log("Evento guardado")
            }
          }
        }else{
          const response = await eventServices.saveMeetingEvent(event)
          if(response){
            if(response.status === "success"){
              console.log("Evento de tipo reunion guardado")
            }
          }
        }
      } catch (error) {
        console.log(error)
      }
    },
    eventStatus(status){
      return status=== 'pending' ? 'Pendiente' : 'Activo';
    },
    async getUsergroups(){
      const id = utils.getIdUserFromToke()
      const response = await groupService.getGroupsByUserId(id)
      if(response){
        if(response.status === "success"){
          this.groups = response.data
        }
      }
    },
    async getUsers(){
      try {
        this.isLoading = true
        const response = await userServices.get_users()
        if(response){
          if(response.status === "success"){
            this.invites = response.data
          }
        }
      this.isLoading = false
      } catch (error) {
        console.log(error)
      }finally{
        this.isLoading = false
      }
    },
    onCheckboxUserChange(userSelected) {
      if (this.eventData.participants === userSelected.id) {
        this.eventData.participants = null;
      } else {
        this.eventData.participants = userSelected.id;
      }
      this.eventData.id_group_member = null;
    },
    onCheckboxGroupChange(groupSelected) {
      if (this.eventData.id_group_member === groupSelected.id) {
        this.eventData.id_group_member = null;
      } else {
        this.eventData.id_group_member = groupSelected.id;
      }
      this.eventData.participants = null;
    },
    ifUserSelected(userSelected){
      return this.eventData.participants === userSelected.id
    },
    ifGroupSelected(groupSelected){
      return this.eventData.id_group_member === groupSelected.id
    },
    prepareObject(){
      console.log("desde el prepare object start", this.eventData.dates[1])
      const startHour = this.eventData.startHour
      const endHour = this.eventData.endHour
      const {start_date, end_date} = utils.formatDate(this.eventData.dates[0], startHour, this.eventData.dates[1], endHour)
      const event = {
        title: this.eventData.title,
        description: this.eventData.description,
        start_date,
        end_date,
        type: this.eventData.type,
        location: this.eventData.location,
        name: this.eventData.name,
        reminder: "",
        notes: "",
      }
      if (this.eventData.id_group_member) {
        event.id_group_member = this.eventData.id_group_member;
      } else {
        // Si no hay un grupo seleccionado
        if (this.eventData.participants) {
          event.moderator = this.eventData.participants;
        } else {
          // Si no hay un usuario seleccionado, tomar el ID del usuario del localStorage
          const userLogged = utils.getIdUserFromToke();
          event.moderator = userLogged;
        }
      }
      return event
    }
  },
  mounted(){
    this.getUsergroups()
    this.getUsers()
  }
};
</script>


<style scoped lang="scss">
 @import '@/styles/colors';

 .no-events-img{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.no-events-text{
  margin-top: 0.2rem;
  font-size: 1.0rem;
  color: #333;
  
}

 .fields {
    margin-bottom: 1.3rem !important;
 }
  .full-width-dropdown {
    width: 100%;
  }
  .form-label-required::after {
  content: " *";
  color: $red-color;
}

.invalid-field-custom {
  border-color: $red-color !important;
  box-shadow: 0 0 3px $shadows !important;
}

.error-messages {
  margin-bottom: 0;
  font-weight: 350;
  font-size: 15px;
}

.error-messages::before {
  content: "* ";
  color: $red-color;
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

.role {
  margin: 0;
  font-size: 12px;
  color: #808080;
}

.icon-container {
  background: transparent;
  margin-right: 15px;
  font-size: 1rem
}

</style>
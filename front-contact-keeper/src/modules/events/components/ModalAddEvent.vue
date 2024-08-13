<template>
  <Dialog
    header="Nuevo Evento"
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{ overflow: 'visible', width: '50vw' }"
    class="custom-dialog"
    :autoZIndex="true"
  >
    <div class="p-fluid grid">
      <b-row>
        <b-col cols="6">
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
        <b-col cols="6">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <Dropdown id="field-event-type" v-model="v$.type.$model" :options="types" optionLabel="label"  optionValue="value"/>
              <label for="field-event-type" class="form-label-required">Tipo:</label>
            </span>
          </div>
        </b-col>
        <b-col cols="12" class="mt-2">
          <div class="fields">
            <span class="p-float-label p-input-icon-right">
              <Textarea id="field-event-description" rows="3" cols="30" v-model="v$.description.$model" :class="{ 'invalid-field-custom': v$.description.$error }" />
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
        <b-col cols="12">
          <div>
            <span class="p-float-label p-input-icon-right">
              <i class="pi pi-calendar"/>
              <Calendar v-model="v$.dates.$model" selectionMode="range" />
              <label for="field-event-dates" class="form-label-required">Duración</label>
            </span>
          </div>
        </b-col>
        <b-col cols="12" class="mt-3">
          <TabView >
            <TabPanel header="Usuarios">
              <ScrollPanel style="width: 100%; height: 160px">
                <template v-if="invites.length > 0">
                  <div class="user-list d-flex justify-content-between align-items-center" v-for="(member, userIndex) in invites" :key="userIndex">
                    <div class="user-info-container d-flex align-items-center mb-2">
                      <Avatar :label="member.name.charAt(0)" shape="circle" size="small"/>
                      <div class="user-info">
                        <label class="username">{{ member.name }}</label>
                        <p class="role">{{ member.email }}</p>
                      </div>
                    </div>
                    <div class="icon-container">
                      <Checkbox :binary="true" />
                    </div>
                  </div>
                </template>
                <template v-else>
                  <div class="no-events-img">
                    <img src="@/assets/User_empty.svg" alt="Sin usuarios" style="width: 120px; height: 120px;"/>
                      <p class="no-events-text">Sin usuarios</p>
                  </div>
                </template>
              </ScrollPanel>
            </TabPanel>
            <TabPanel header="Grupos">
              <ScrollPanel style="width: 100%; height: 160px;">
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
                      <Checkbox :binary="true" />
                    </div>
                  </div>
                </template>
                <template v-else>
                  <div class="no-events-img">
                    <img src="@/assets/inbox_empty.svg" alt="Sin usuarios" style="width: 120px; height: 120px;"/>
                      <p class="no-events-text">Sin grupos</p>
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
import utils from '@/kernel/utils';
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
      today: new Date().toISOString().split('T')[0]
    };
  },
  setup() {
    const eventData = reactive({
      title: '',
      description: '',
      dates: null,
      type: null,
      participants: null
    });

    const rules = {
      title: {
        required: helpers.withMessage('El título del evento es requerido', required),
        onlyLetters: helpers.withMessage('El título solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("El título debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("El título debe tener máximo de 30 caracteres", maxLength(30))
      },
      description: {
        required: helpers.withMessage('La descripción es requerida', required),
        onlyLetters: helpers.withMessage('La descripción solo puede contener letras y números', (value) => phraseRegex.test(value)),
        minLength: helpers.withMessage("La descripción debe tener al menos 3 caracteres", minLength(3)),
        maxLength: helpers.withMessage("La descripción debe tener máximo 70 caracteres", maxLength(70))
      },
      dates: {
        required: helpers.withMessage('La fecha de inicio del evento es requerida', required),
      },
      type: {
        required: helpers.withMessage('El tipo de evento es requerido', required),
      },
      participants: {
        required: helpers.withMessage('El tipo de evento es requerido', required),
      },
      dates: {
        required: helpers.withMessage('La fecha de inicio y de fin son requeridos', required),
      }
    };

    const v$ = useVuelidate(rules, eventData);
    return {eventData, v$}
  },
  methods:{
    closeModal(){
      this.$emit('update:visible', false);
    },

    saveEvent() {
      console.log(this.eventData);
      this.closeModal(); 
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
    }
  },
  mounted(){
    this.getUsergroups()
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
}

</style>
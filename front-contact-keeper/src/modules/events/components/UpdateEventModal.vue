<template>
    <Dialog header="Modificar evento" :modal="true" :closeOnEscape="false" :closable="false" :visible.sync="visible"
        position="center" :contentStyle="{ overflow: 'visible', width: '70vw' }" class="custom-dialog"
        :autoZIndex="true">
        <div class="p-fluid grid">
            <b-row>
                <b-col cols="12" lg="4" md="6" sm="12">
                    <div class="field">
                        <span class="p-float-label p-input-icon-right">
                            <i class="pi pi-bookmark" />
                            <InputText id="field-event-title" v-model="v$.title.$model"
                                :class="{ 'invalid-field-custom': v$.title.$error && v$.title.$dirty }" />
                            <label for="field-event-title" class="form-label-required">Título</label>
                        </span>
                        <div class="text-danger text-start pt-2">
                            <p class="error-messages" v-if="v$.title.$dirty && v$.title.required.$invalid">
                                {{ v$.title.required.$message }}
                            </p>
                            <p class="error-messages" v-if="v$.title.$dirty && v$.title.onlyLetters.$invalid">
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
                            <Dropdown id="field-event-type" v-model="v$.type.$model" :options="types"
                                optionLabel="label" optionValue="value" />
                            <label for="field-event-type" class="form-label-required">Tipo</label>
                        </span>
                    </div>
                </b-col>
                <b-col cols="12" lg="4" md="6" sm="12">
                    <span class="p-float-label p-input-icon-right">
                        <i class="pi pi-map-marker" />
                        <InputText id="field-event-location" v-model="v$.location.$model"
                            :class="{ 'invalid-field-custom': v$.location.$error && v$.location.$dirty }" />
                        <label for="field-event-location" class="form-label-required">Ubicación</label>
                    </span>
                    <div class="text-danger text-start pt-2">
                        <p class="error-messages" v-if="v$.location.$dirty && v$.location.onlyLetters.$invalid">
                            {{ v$.location.onlyLetters.$message }}
                        </p>
                        <p class="error-messages" v-if="v$.location.$dirty && v$.location.maxLength.$invalid">
                            {{ v$.location.maxLength.$message }}
                        </p>
                    </div>
                </b-col>
                <b-col cols="12" lg="12" md="6" sm="12" class="mt-2">
                    <div class="mb-3">
                        <span class="p-float-label p-input-icon-right">
                            <i class="pi pi-info-circle" />
                            <InputText id="field-event-name" v-model="v$.name.$model"
                                :class="{ 'invalid-field-custom': v$.name.$error && v$.name.$dirty }" />
                            <label for="field-event-name" class="form-label-required">Nombre</label>
                        </span>
                        <div class="text-danger text-start pt-2">
                            <p class="error-messages" v-if="v$.name.$dirty && v$.name.required.$invalid">
                                {{ v$.name.required.$message }}
                            </p>
                            <p class="error-messages" v-if="v$.name.$dirty && v$.name.onlyLetters.$invalid">
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
                <b-col cols="12" lg="6" md="6" sm="12" class="mt-2 mb-3">
                    <div class="field">
                        <span class="p-float-label">
                            <Calendar id="fieldset-start" v-model="v$.start_date.$model" dateFormat="yy/mm/dd"
                                :class="{ 'invalid-field-custom': v$.start_date.$error && v$.start_date.$dirty }" />
                            <label for="fieldset-start" class="form-label-required">Fecha de inicio</label>
                        </span>
                        <div class="text-danger text-start pt-2">
                            <p class="error-messages" v-if="v$.start_date.$dirty && v$.start_date.required.$invalid">
                                {{ v$.start_date.required.$message }}
                            </p>
                            <p class="error-messages" v-if="v$.start_date.$dirty && v$.start_date.isBeforeEnd.$invalid">
                                {{ v$.start_date.isBeforeEnd.$message }}
                            </p>
                            <p class="error-messages" v-if="v$.start_date.$dirty && v$.start_date.isOneDayDifference.$invalid">
                                {{ v$.start_date.isOneDayDifference.$message }}
                            </p>
                        </div>
                    </div>
                </b-col>
                <b-col cols="12" lg="6" md="6" sm="12" class="mt-2 mb-3">
                    <div class="field">
                        <span class="p-float-label">
                            <Calendar id="fieldset-end" v-model="v$.end_date.$model" dateFormat="yy/mm/dd"
                                :class="{ 'invalid-field-custom': v$.end_date.$error && v$.end_date.$dirty }" />
                            <label for="fieldset-end" class="form-label-required">Fecha de fin</label>
                        </span>
                        <div class="text-danger text-start pt-2">
                            <p class="error-messages" v-if="v$.end_date.$dirty && v$.end_date.required.$invalid">
                                {{ v$.end_date.required.$message }}
                            </p>
                            <p class="error-messages" v-if="v$.end_date.$dirty && v$.end_date.isAfterStart.$invalid">
                                {{ v$.end_date.isAfterStart.$message }}
                            </p>
                        </div>
                    </div>
                </b-col>
                <b-col cols="12" lg="6" md="6" sm="12" class="mt-2 mb-3">
                    <div class="field">
                        <span class="p-float-label p-input-icon-right">
                            <i class="pi pi-clock"></i>
                            <Calendar id="field-event-start" v-model="v$.startHour.$model"
                                :class="{ 'invalid-field-custom': v$.startHour.$error && v$.startHour.$dirty }" :timeOnly="true"
                                hourFormat="12" />
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
                <b-col cols="12" lg="6" md="6" sm="12" class="mt-2 mb-3">
                    <div class="field">
                        <span class="p-float-label p-input-icon-right">
                            <i class="pi pi-clock"></i>
                            <Calendar id="field-event-end" v-model="v$.endHour.$model"
                                :class="{ 'invalid-field-custom': v$.endHour.$error && v$.endHour.$dirty }" :timeOnly="true" hourFormat="12" />
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
                <b-col cols="12" class="mt-3">
                    <div class="field">
                        <span class="p-float-label p-input-icon-right">
                        <Textarea id="field-event-description" rows="2" cols="30" v-model="v$.description.$model" :class="{ 'invalid-field-custom': v$.description.$error && v$.description.$dirty }"/>
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
            </b-row>
        </div>
        <template #footer>
            <Button :label="onUpdating ? 'Modificando...' :'Modificar' " :disabled="onUpdating" icon="pi pi-check" iconPos="right" class="button-options" @click="saveEvent"/>
            <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-plain" iconPos="right"
                @click="closeModal" />
        </template>
    </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog/Dialog';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, helpers, maxLength, minLength } from '@vuelidate/validators';
import { getGroupById } from '@/modules/groups/services/groups-services';
import utils from '@/kernel/utils';
import { onToast } from '@/kernel/alerts';
import eventServices from '../services/event-services';

export default {
    name: "UpdateEventModal",
    components: {
        Dialog,
        Button,
        Dropdown,
        InputText
    },
    props: {
        event: {
            type: Object,
        },
        visible: {
            type: Boolean,
        }
    },
    setup() {
        const eventData = reactive({
            title: '',
            description: '',
            type: null,
            location: '',
            start_date: '',
            end_date: '',
            startHour: '',
            endHour: '',
            name: '',
            id_group_member: ''
        });

        const rules = {
            title: {
                required: helpers.withMessage('El título del evento es requerido', required),
                onlyLetters: helpers.withMessage('El título solo puede contener letras y números', (value) => /^[a-zA-Z0-9\s]+$/.test(value)),
                minLength: helpers.withMessage("El título debe tener al menos 3 caracteres", minLength(3)),
                maxLength: helpers.withMessage("El título debe tener máximo de 30 caracteres", maxLength(30)),
            },
            name: {
                required: helpers.withMessage('El nombre del evento es requerido', required),
                onlyLetters: helpers.withMessage('El nombre solo puede contener letras y números', (value) => /^[a-zA-Z0-9\s]+$/.test(value)),
                minLength: helpers.withMessage("El nombre debe tener al menos 3 caracteres", minLength(3)),
                maxLength: helpers.withMessage("El nombre debe tener máximo de 30 caracteres", maxLength(30)),
            },
            description: {
                required: helpers.withMessage('La descripción es requerida', required),
                onlyLetters: helpers.withMessage('La descripción solo puede contener letras y números', (value) => /^[a-zA-Z0-9\s]+$/.test(value)),
                minLength: helpers.withMessage("La descripción debe tener al menos 3 caracteres", minLength(3)),
                maxLength: helpers.withMessage("La descripción debe tener máximo 70 caracteres", maxLength(100))
            },
            start_date: {
                required: helpers.withMessage('La fecha de inicio del evento es requerida', required),
                isBeforeEnd: helpers.withMessage('La fecha de inicio debe ser menor a la fecha de fin', (value) => utils.startDateBeforeEndDate(value, eventData.end_date)),
                isOneDayDifference: helpers.withMessage('El evento solo puede durar un día', (value) => utils.isOneDayDifference(value, eventData.end_date)),
            },
            end_date: {
                required: helpers.withMessage('La fecha de fin del evento es requerida', required),
                isAfterStart: helpers.withMessage('La fecha de fin debe ser mayor a la fecha de inicio', (value) => utils.endDateAfterStartDate(eventData.start_date, value)),
            },
            type: {
                required: helpers.withMessage('El tipo de evento es requerido', required),
            },
            location: {
                onlyLetters: helpers.withMessage('El nombre del lugar solo puede contener letras y números', (value) => /^[a-zA-Z0-9\s]+$/.test(value)),
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
        return { eventData, v$ }
    },
    methods: {
        closeModal() {
            this.resetValidation();
            this.$emit('update:visible', false);
        },
        resetValidation() {
            this.v$.$reset();
        },
        async saveEvent() {
            this.v$.$touch();
            if (this.v$.$invalid) {
                return;
            }
            const event = this.prepareObject();
            //actualizar
            try {
                this.onUpdating = true;
                const response = await eventServices.updateEvent(event);
                if (response.status === 'success') {
                    this.closeModal();
                    this.$emit('getEvents');
                    onToast('Éxito', 'Evento actualizado correctamente', 'success');
                    this.onUpdating = false;
                }
            }catch (error) {
                onToast('Error', 'Ocurrió un error al actualizar el evento', 'error');
            }finally {
                this.resetValidation();
                this.onUpdating = false;
            } 
        },
        async getGroup(){
            try {
                const response = await getGroupById(this.event.event.id_group_member);
                if(response.data.status === 'success'){
                    this.groups = response.data.data;
                }
            } catch (error) {
                console.log(error);
                onToast('Error', 'Ocurrió un error al obtener los grupos', 'error');
            }
        },
        prepareObject() {
            const startHour = this.eventData.startHour
            const endHour = this.eventData.endHour
            const {start_date, end_date} = utils.formatDate(this.eventData.start_date, startHour, this.eventData.end_date, endHour)
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
                id: this.idEvent
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
            return event;
        }
    },
    data() {
        return {
            types: [
                { label: 'Reunión', value: 'meeting' },
                { label: 'Sesión', value: 'session' },
                { label: 'Cumpleaños', value: 'birthday' },
                { label: 'Otro', value: 'other' }
            ],
            invites: [],
            groups: [],
            id_group_member: null,
            idEvent: null,
            onUpdating: false
        }
    },
    watch: {
        event: {
            handler() {
                const oldEvent = this.event.event;
                const startObj = utils.extractDateAndTime(oldEvent.start_date);
                const endObj = utils.extractDateAndTime(oldEvent.end_date);
                this.eventData.title = oldEvent.title ? oldEvent.title : '';
                this.eventData.description = oldEvent.description ? oldEvent.description : '';
                this.eventData.end_date = oldEvent.end_date ? endObj.date : '';
                this.eventData.start_date = oldEvent.start_date ? startObj.date : '';
                this.eventData.startHour = oldEvent.start_date ? startObj.time : '';
                this.eventData.endHour = oldEvent.end_date ? endObj.time : '';
                this.eventData.id_group_member = oldEvent.id_group_member ? oldEvent.id_group_member : null;
                this.eventData.type = oldEvent.type ? oldEvent.type : null;
                this.eventData.location = oldEvent.location ? oldEvent.location : '';
                this.eventData.name = oldEvent.name ? oldEvent.name : '';
                this.idEvent = oldEvent.id;
            },
            deep: true
        }
    },
}
</script>

<style scoped lang="scss">
@import '@/styles/colors';

.button-options {
    background: $primary-color;
    color: white;
    border: none;
    border-radius: 5px;
}

.button-options:hover{
   transform: translateY(-5px);
   box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
   background: $primary-color !important;
   border: none;
   cursor: pointer;
 }
.no-events-img {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.no-events-text {
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

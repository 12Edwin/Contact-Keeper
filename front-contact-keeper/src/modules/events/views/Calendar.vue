<template>
  <div class="main-content">
    <div class="content">
      <b-row>
        <b-col>
          <Panel header="Eventos" class="shadow-lg">
            <b-row>
              <b-col cols="12">
                <div class="calendar-container">
                  <template v-if="!isLoading">
                    <template v-if="items.length > 0">
                    <FullCalendar :options="calendarOptions" id="myCustomCalendar">
                      <template v-slot:eventContent='{ event }'>
                        <div class="my-custom-event" @click="handleEventClick(event)">
                          <span class="my-event-dot" :v-tooltip.top="eventType(event.extendedProps.type)"  :style="{'background-color': setDotBackgrund(event.extendedProps.type)}"></span>
                          <div class="my-event-info">
                            <span class="my-event-title"><b>{{ event.extendedProps.title ? event.extendedProps.title : event.extendedProps.name}}</b></span>
                            <span class="my-event-location">{{ event.extendedProps.location }}</span>
                            <span class="my-event-time">{{ formatCalendarDate(event.start) }} - {{ formatCalendarDate(event.end) }}</span>
                          </div>
                        </div>
                      </template>
                    </FullCalendar>
                    </template>
                    <template v-else>
                        <div class="no-events-img">
                          <img src="@/assets/no_events.svg" alt="No hay eventos" />
                          <p class="no-events-text">¡Aquí verás todos tus eventos por venir!</p>
                          <Button label="Crear evento" @click="openModalAddEvent()" class="p-button-text p-button-text mt-1 p-button-plain button-styles text" />
                        </div>
                    </template>
                  </template>
                  <template v-else>
                    <div class="content">
                      <CalendarSkeleton />
                    </div>
                  </template>
                </div>
              </b-col>
            </b-row>
          </Panel>
          <ModalEventInfo :event="selectedEvent" :visible.sync="showModalEventInfo" @close="showModalEventInfo = false"/>
          <ModalAddEvent :visible.sync="showModalAddEvent" @getEvents="getEvents"/>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import timeGridPlugin from '@fullcalendar/timegrid'
import Loader from "@/components/Loader.vue"
import ModalEventInfo from '@/modules/events/components/ModalEventInfo.vue'
import ModalAddEvent from '@/modules/events/components/ModalAddEvent.vue'
import moment from 'moment';
import Panel from 'primevue/panel'
import esLocale from '@fullcalendar/core/locales/es';
import Chip from 'primevue/chip';
import utils from '@/kernel/utils'
import eventServices from '../services/event-services'
import CalendarSkeleton from '@/components/CalendarSkeleton.vue'
import Tooltip from 'primevue/tooltip';
import { onError, onToast} from '@/kernel/alerts';
export default
{
  name: 'Calendar',
  components: {
    FullCalendar,
    Loader,
    ModalEventInfo,
    ModalAddEvent,
    Panel,
    Chip,
    CalendarSkeleton
  },
  directives: {
    'tooltip': Tooltip
},
  data() {
    return {
      sidebarVisible: false,
      showModalEventInfo: false,
      showModalAddEvent: false,
      items: [],
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
        initialView: 'dayGridMonth',
        locale: esLocale,
        weekends: false,
        dayMaxEventRows: 2,
        events: this.items,
        headerToolbar: {
          start: 'dayGridMonth,timeGridWeek,timeGridDay today prev,next',
          center: 'title',
          end: 'addEventButton'
        },
        customButtons: {
          addEventButton: {
            text: 'Agregar Evento',
            click: () => this.openModalAddEvent(),
          },
        },
        views: {
          dayGridMonth: {
            titleFormat: { year: 'numeric', month: 'long' }
          }
        },
        themeSystem: 'bootstrap',
        eventColor: '#007bff',
        eventTextColor: '#FFFFFF',
        eventBackgroundColor: '#007bff',
        eventBorderColor: '#007bff',
        bootstrapFontAwesome: false,
        buttonIcons: false,
        buttonText: {
          today: 'Hoy',
          month: 'Mes',
          week: 'Semana',
          day: 'Día',
          prev: '<',
          next: '>'
        },
        dayCellDidMount: function(info) {
          info.el.style.backgroundColor = 'white';
          info.el.style.color = 'black';
        },
        eventDidMount: function(info) {
          info.el.style.backgroundColor = '#000';
          info.el.style.borderColor = '#000';
          info.el.style.color = 'white';
        },
        viewDidMount: function(info) {
          const headerEl = info.el.querySelector('.fc-toolbar');
          if (headerEl) {
            headerEl.style.backgroundColor = 'white';
            headerEl.style.color = 'black';
          }
          const dayHeaderEls = info.el.querySelectorAll('.fc-col-header-cell');
          dayHeaderEls.forEach(el => {
            el.style.backgroundColor = 'white';
            el.style.color = 'black';
          });
        },
      },
      isLoading: false,
      selectedEvent: {},
    };
  },
  methods: {

    addEvent(eventData) {
      const newEvent = {
        title: eventData.title,
        start: eventData.startDate,
        end: eventData.endDate,
        description: eventData.description,
        status: 'info'
      };
      this.events.push(newEvent);
    },
    handleEventClick(event) {
      this.selectedEvent = event.extendedProps.event;
      this.showModalEventInfo = true;
    },
    setDotBackgrund(status) {
      let color = '';
      switch (status) {
        case 'meeting':
          color = '#007bff';
          break;
        case 'session':
          color = '#28a745';
          break;
        case 'event':
          color = '#ffc107';
          break;
        default:
          color = '#dc3545';
          break;
      }
      return color;
    },
    formatCalendarDate(pop){
      return moment(pop).format("YYYY-MM-DD")
    },
    openModalAddEvent() {
      console.log('openModalAddEvent')
      this.showModalAddEvent = true;
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
    },
    async getEvents(){
      try {
        this.items = []
        this.isLoading = true
        const userLogged = utils.getIdUserFromToke()
        console.log(userLogged)
        const response = await eventServices.getEvents(userLogged)
        if(response.status === "success"){
          this.isLoading = false
          response.data.forEach((event) => {
            this.items.push({
              title: event.title,
              start: new Date(event.start_date).toISOString(),
              end: new Date(event.end_date).toISOString(),
              location: event.location,
              name: event.name,
              event
            })
          })
        }
        this.isLoading = false
      } catch (error) {
        onToast('Error al obtener los eventos', 'Parece que hubo un error al obtener los eventos, por favor intenta de nuevo', 'error')
      }
    }
  },
  watch: {
  items: {
    handler(newEvents) {
      this.calendarOptions = { ...this.calendarOptions, events: newEvents };
    },
    deep: true
  }
},
  mounted() {
    this.getEvents()
  }
}
</script>

<style>
/* Estilos globales para FullCalendar */
.fc {
  background-color: white !important;
  color: black !important;
}

.fc .fc-button-primary {
  background-color: black !important;
  border-color: black !important;
  color: white !important;
}

.fc .fc-button-primary:not(:disabled):active,
.fc .fc-button-primary:not(:disabled).fc-button-active {
  background-color: black !important;
  border-color: black !important;
}

.fc .fc-col-header-cell-cushion,
.fc .fc-daygrid-day-number,
.fc .fc-daygrid-day-top {
  color: black !important;
}

.fc .fc-day-today {
  background-color: #f0f0f0 !important;
}

.calendar-container {
  width: 100%;
  min-width: 800px;
  overflow-x: auto;
}

#myCustomCalendar {
  width: 100%;
  max-height: 80vh;
}

.fade-class {
  animation-name: fade;
  animation-duration: 1s;
}

@keyframes fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-enter-active {
  transition: all 1s;
}

.fade-leave-active {
  transition: all 0.1s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fc-event {
  padding: 3px;
}

.my-custom-event {
  display: flex;
  align-items: center;
  padding-left: 10px;
  cursor: pointer;
  background-color: #000;
}

.my-event-dot {
  width: 10px;
  height: 10px;
  background-color: rgb(0, 0, 10);
  margin-right: 5px;
}

.my-event-info {
  display: flex;
  flex-direction: column;
}

.my-event-title {
  font-size: 14px;
  margin-bottom: 2px;
  color: white;
}

.my-event-time {
  font-size: 12px;
  color: white;
}
</style>


<style scoped lang="scss">
@import '@/styles/colors.scss';

/* Estilos existentes */
.my-event-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 10px;
}

.my-custom-event {
    display: flex;
    align-items: center;
    padding-left: 10px;
}

.my-event-location {
    font-size: 11px;
    margin-bottom: 2px;
}

.my-event-title {
    font-size: 14px;
    margin-bottom: 2px;
}
.my-event-time {
    font-size: 10px;
}
.main-content {
  display: flex;
}

.content {
  flex: 1;
  padding: 1rem;
  margin-left: 0;
  transition: margin-left 0.3s;
}
.no-events-img{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.no-events-text{
  margin-top: 1rem;
  font-size: 1.5rem;
  color: #333;
  
}
.button-styles{
  width: 15% !important;
  padding: 0.50rem !important;
  background-color: black !important;
  color: white !important;
  border: none;
  border-radius: 9px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  justify-content: center;
}

.button-styles:hover{
   transform: translateY(-5px);
   box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
   background: $primary-color !important;
   border: none;
   cursor: pointer;
 }


.p-panel{
 width: 100% !important;
}
</style>
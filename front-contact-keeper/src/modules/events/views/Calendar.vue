<template>
  <div class="main-content">
    <div class="content">
      <Panel header="Eventos" class="shadow-lg">
        <b-row>
          <b-col cols="12">
            <Loader v-if="isLoading" key="load" />
            <div v-else class="calendar-container">
              <FullCalendar :options="calendarOptions" :events="events" id="myCustomCalendar">
                <template v-slot:eventContent="{ event }">
                  <div class="my-custom-event" @click="handleEventClick(event)">
                    <span class="my-event-dot"></span>
                    <div class="my-event-info">
                      <span class="my-event-title"><b>{{ event.title }}</b></span>
                      <span class="my-event-time">{{ formatCalendarDate(event.start) }} - {{ formatCalendarDate(event.end) }}</span>
                    </div>
                  </div>
                </template>
              </FullCalendar>
            </div>
          </b-col>
        </b-row>
      </Panel>
      <ModalEventInfo :event="selectedEvent" :visible.sync="showModalEventInfo" @close="showModalEventInfo = false"/>
      <ModalAddEvent :visible.sync="showModalAddEvent" />
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
import Chip from 'primevue/chip';

export default
{
  name: 'Calendar',
  components: {
    FullCalendar,
    Loader,
    ModalEventInfo,
    ModalAddEvent,
    Panel,
    Chip
  },
  data() {
    return {
      sidebarVisible: false,
      showModalEventInfo: false,
      showModalAddEvent: false,
      events: [],
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
        initialView: 'dayGridMonth',
        weekends: false,
        dayMaxEventRows: 2,
        headerToolbar: {
          start: 'dayGridMonth,timeGridWeek,timeGridDay today prev,next',
          center: 'title',
          end: 'addEventButton'
        },
        customButtons: {
          addEventButton: {
            text: 'Agregar Evento',
            click: () => this.showModalAddEvent = true,
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
        events: [
          { title: 'Evento 1', start: '2024-07-18', end: '2024-07-18', description: 'Descripción del Evento 1' },
          { title: 'Evento 2', start: '2024-07-20', end: '2024-07-23', description: 'Descripción del Evento 2' },
          { title: 'Evento 3', start: '2024-07-22', end: '2024-07-25', description: 'Descripción del Evento 3' },
          { title: 'Evento 4', start: '2024-07-25', end: '2024-08-28', description: 'Descripción del Evento 4' },
          { title: 'Evento 5', start: '2024-08-28', end: '2024-08-28', description: 'Descripción del Evento 5' },
        ],
      },
      isLoading: false,
      selectedEvent: {},
    };
  },
  methods: {
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
    },

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
        this.selectedEvent = {
        title: event.title,
        startDate: event.start.toISOString().split('T')[0],
        endDate: event.end ? event.end.toISOString().split('T')[0] : event.start.toISOString().split('T')[0],
        description: event.extendedProps.description,
        status: event.extendedProps.status || 'No especificado',
        participants: event.extendedProps.participants || 'No especificado',
      };
      this.showModalEventInfo = true;
    },
    setDotBackground(status) {
      const colors = {
        success: 'green',
        warning: 'orange',
        danger: 'red',
        primary: 'blue',
        secondary: 'grey',
        info: 'cyan'
      };
      return colors[status] || 'grey';
    },
    formatCalendarDate(date){
      return moment(date).format('YYYY-MM-DD');
    },
  },
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


<style scoped>
/* Estilos existentes */
.main-content {
  display: flex;
}

.content {
  flex: 1;
  padding: 1rem;
  margin-left: 0;
  transition: margin-left 0.3s;
}
</style>
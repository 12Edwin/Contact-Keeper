<template>
    <div class="main-content">
      <Navbar @toggle-sidebar="toggleSidebar" />
      <SidebarAdmin :visible="sidebarVisible" @update:visible="sidebarVisible = $event" />
      <div class="content">
        <panel class="fade-class">
          <template #header>
            <div class="d-flex justify-content-between w-100 align-items-center">
              <p class="h5"><b>Eventos</b></p>
            </div>
          </template>
          <b-row>
            <b-col cols="12">
              <Loader v-if="isLoading" key="load" />
              <div v-else class="calendar-container">
                <FullCalendar :options="calendarOptions" :events="events" id="myCustomCalendar" />
              </div>
            </b-col>
          </b-row>
        </panel>
      </div>
    </div>
  </template>
  
  <script>
  import FullCalendar from '@fullcalendar/vue'
  import dayGridPlugin from '@fullcalendar/daygrid'
  import interactionPlugin from '@fullcalendar/interaction'
  import timeGridPlugin from '@fullcalendar/timegrid'
  import Navbar from '@/components/Navbar.vue'
  import SidebarAdmin from "@/components/SidebarAdmin.vue"
  import Loader from "@/components/Loader.vue"
  
  export default {
    components: {
      FullCalendar,
      Navbar,
      SidebarAdmin,
      Loader,
    },
    data() {
      return {
        sidebarVisible: false,
        calendarOptions: {
          plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
          initialView: 'dayGridMonth',
          weekends: false,
          dayMaxEventRows: 2,
          headerToolbar: {
                start: 'title',
                center: '',
                end: 'dayGridMonth,timeGridWeek,timeGridDay today prev,next'
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
          },
          dayCellDidMount: function(info) {
            info.el.style.backgroundColor = 'white';
            info.el.style.color = 'black';
          },
          eventDidMount: function(info) {
            info.el.style.backgroundColor = '#007bff';
            info.el.style.borderColor = '#007bff';
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
        events: [
          { title: 'Evento 1', start: '2024-07-18' },
          { title: 'Evento 2', start: '2024-07-20' },
          // Puedes añadir más eventos según necesites
        ],
        isLoading: false,
      }
    },
    methods: {
      toggleSidebar() {
        this.sidebarVisible = !this.sidebarVisible
      },
      addEvent() {
        const newEvent = {
          title: 'Nuevo Evento',
          start: '2024-07-25',
        };
        this.events.push(newEvent);
      },
      saveEvents() {
        // Aquí iría la lógica para guardar this.events en tu backend
        alert('Eventos guardados');
      },
      loadEvents() {
        // Aquí iría la lógica para cargar eventos desde tu backend
        alert('Eventos cargados');
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
  
  /* Estilos existentes */
  .main-content {
    display: flex;
  }
  
  .content {
    flex: 1;
    padding: 2rem;
    margin-left: 0;
    transition: margin-left 0.3s;
    margin-top: 70px;
  }
  
  .calendar-container {
    width: 100%;
    min-width: 800px; 
    overflow-x: auto; 
  }
  
  #myCustomCalendar {
    width: 100%;
    max-height: 75vh;
  }
  
  .fade-class {
    animation-name: fade;
    animation-duration: 1s;
  }
  
  @keyframes fade {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  .fade-enter-active {
    transition: all 1s;
  }
  
  .fade-leave-active {
    transition: all .1s;
  }
  
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }

  
  </style>
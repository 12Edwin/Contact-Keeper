<template>
  <div class="main-content">
    <Navbar @toggle-sidebar="toggleSidebar" />
    <SidebarAdmin :visible="sidebarVisible" @update:visible="sidebarVisible = $event" />
    <div class="content">
      <panel class="fadeclass">
        <template #header >
          <div class="d-flex justify-content-between w-100 align-items-center">
            <p class="h5"><b>Eventos</b></p>
          </div>
        </template>
        <b-row>
          <b-col cols="12">
            <Loader v-if="isLoading" key="load" />
            <div v-else class="calendar-container">
              <FullCalendar :options="calendarOptions" id="myCustomCalendar" />
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
import Navbar from '@/components/Navbar.vue'
import SidebarAdmin from "@/components/SidebarAdmin.vue"

export default {
    components: {
        FullCalendar,
        Navbar,
        SidebarAdmin,
    },
    data() {
        return {
            sidebarVisible: false,
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth',
                weekends: false,
                dayMaxEventRows: 2,
                headerToolbar: {
                    start: 'title',
                    center: '',
                    end: 'today prev,next'
                },
                views: {
                    dayGridMonth: {
                        titleFormat: { year: 'numeric', month: 'long' }
                    }
                },
            },
            events: [
                { title: 'event 1', date: '2024-07-18' },
                { title: 'event 2', date: '2024-07-20' }
            ],
            config: {
                background: '#333',
                color: 'white',
            },
            displayModal: false,
            isLoading: false
        }
    },
    methods: {
        toggleSidebar() {
            this.sidebarVisible = !this.sidebarVisible
        }
    }
}
</script>

<style>
#myCustomCalendar .fc-button {
  background: #333;
  color: #fff;
  border-color: #333;
  border-radius: 10px;
  box-sizing: border-box;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1); 
}

#myCustomCalendar .fc-button:hover {
  background-color:#333;
  border-color:#333;
}

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

.content.sidebar-open {
    margin-left: 250px;
}

.calendar-wrapper {
    display: flex;
    align-items: center;
    padding: 5rem;
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


.fadeclass {
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
  transition: all .1s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>

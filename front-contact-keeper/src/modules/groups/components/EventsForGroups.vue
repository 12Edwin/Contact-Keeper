<template>
  <Dialog
    :modal="true"
    :closeOnEscape="false"
    :closable="false"
    :visible.sync="visible"
    position="center"
    :contentStyle="{width: '35vw'}"
    class="custom-dialog"
    :autoZIndex="true"
  >
    <template v-slot:header>
      <h4>Próximos eventos</h4>
    </template>
    <TabView @tab-change="onTabChange">
      <TabPanel @change="onTabChange()" :header="`Eventos grupales (${localEvents.length})`">
        <div class="tab-content-scrollable">
          <template v-if="loading">
            <div class="skeleton-container">
              <div class="skeleton-item" v-for="index in 6" :key="index"></div>
            </div>
          </template>

        <!-- Mensaje cuando no hay eventos -->
        <template v-if="!loading && localEvents.length === 0">
          <div style="display: flex; justify-content: center; align-items: center;">
            <div class="text-center">
              <img src="@/assets/no_events.svg" alt="No hay eventos" class="no-events-img"/>
              <p>No hay eventos en este grupo.</p>
            </div>
          </div>
        </template>


          <!-- Mostrar eventos si hay alguno -->
          <template v-else>
            <b-row>
              <b-col v-for="(event, index) in localEvents" :key="event.id" cols="12" class="mb-2">
                <div class="event-container" :class="{ 'event-container--small': index > 0 }">
                  <div class="event-header">
                    <h5>Título</h5>
                  </div>
                  <p>{{ event.name }}</p>
                </div>
                <div class="event-container" :class="{ 'event-container--small': index > 0 }">
                  <div class="event-header">
                    <h5>Localización</h5>
                  </div>
                  <p>{{ event.location }}</p>
                </div>
                <div class="event-container" :class="{ 'event-container--small': index > 0 }">
                  <div class="event-header">
                    <h5>Tipo</h5>
                  </div>
                  <p>{{ translateTypeEvent(event.type)}}</p>
                </div>
                <div class="event-container" :class="{ 'event-container--small': index > 0 }">
                  <div class="event-header">
                    <h5>Fechas</h5>
                  </div>
                  <p>{{ formatEventDate(event.start_date)}} - {{ formatEventDate(event.end_date) }}</p>
                </div>
              </b-col>
            </b-row>
          </template>
        </div>
      </TabPanel>
      <TabPanel header="Mensajes" @change="onTabChange()">
        <template v-if="!gettingChat">
          <template v-if="messages.length > 0">
            <div ref="chatPanel" class="tab-content-scrollable chat-panel">
              <b-row>
                <b-col v-for="(message, index) in messages" :key="index" cols="12" :class="alignSide(message.id)">
                  <div class="chat-content">
                    <span v-if="showUsername(message.id)" class="chat-username">{{message.name}} {{ message.last_name }}</span>
                    <p>{{ message.message }}</p>
                    <span class="chat-timestamp">{{ formatDateChat(message.created_at) }}</span>
                  </div>
                </b-col>
              </b-row>
            </div>
          </template>
          <template v-else>
            <div class="no-events-img">
              <img src="@/assets/message_empty.svg" alt="Sin grupos" style="width: 120px; height: 120px;"/>
                <p class="no-events-text">Sin mensajes</p>
            </div>
          </template>
        </template>
        <template v-else>
          <ChatSkeleton />
        </template>
      </TabPanel>
    </TabView>
    <template #footer>
      <template v-if="!showInput">
        <Button label="Guardar" icon="pi pi-check" iconPos="right" class="button-options"/>
        <Button label="Cancelar" icon="pi pi-times" class="p-button-text p-button-plain" iconPos="right" @click="closeModal()"/>
      </template>
      <template v-else>
        
        <div class="chat-input-container">
            <textarea 
              type="text" 
              placeholder="Escribe un mensaje..."
              class="chat-input" 
              rows="1"
              @input="adjustTextareaHeight"
              v-model="message"
            />
            <Button class="send-button" :label="sendingMessage ? 'Enviando...' : 'Enviar'" :disabled="!message || sendingMessage" @click="onSendMessageTo()"></Button>
        </div>
      </template>
    </template>
  </Dialog>
</template>

<script>
import utils from '@/kernel/utils';
import Tooltip from 'primevue/tooltip';
import { getGroupById, sendMessage } from '../services/groups-services';
import { onToast } from '@/kernel/alerts';
import ChatSkeleton from '@/components/ChatSkeleton.vue';
import { formatDate } from '@fullcalendar/core';
export default {
  name: 'EventsForGroups',
  directives: {
    'tooltip': Tooltip
  },
  components: {
    ChatSkeleton
  },
  props: {
    visible: {
      type: Boolean,
    },
    group: {
      type: Object,
      default: () => ({})
    },
    events: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      loading: false, 
      timer: null,
      localEvents: [],
      messages: [],
      showInput: false,
      gettingChat: false,
      idGroup: null,
      message: '',
      sendingMessage: false,
    };
  },
  watch: {
    visible: {
      handler(val) {
        if (val) {
          this.resetModal();
        }
      },
      immediate: true
    },
    events: {
      handler(val) {
        if (val.length > 0) {
          this.localEvents = val;
          clearTimeout(this.timer);
          this.loading = false;
        }
      },
      immediate: true
    },
    group: {
      handler(val) {
        if (val.id) {
          this.getGroupMessages();
        }
      },
      immediate: true
    },
    messages() {
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    }
  },
  methods: {
    scrollToBottom() {
      const chatPanel = this.$refs.chatPanel;
      if (chatPanel) {
        chatPanel.scrollTop = chatPanel.scrollHeight;
      }
    },
    alignSide(idUser){
      const userLogged = utils.getIdUserFromToke()
      return userLogged === idUser ? 'd-flex justify-content-end align-items-end' : 'd-flex justify-content-start align-items-start'
    },
    showUsername(idUser){
      const userLogged = utils.getIdUserFromToke()
      return userLogged !== idUser
    },
    async onSendMessageTo(){
      try {
        this.sendingMessage = true;
        const message = {
          message: this.message,
          id_group: this.group.id,
          author: utils.getIdUserFromToke()
        }
        this.message = ''
        const response = await sendMessage(message);
        if(response){
          if(response.status === "success"){
            this.getGroupMessages()
            this.sendingMessage = false;
          }
        }
      } catch (error) {
        onToast('error', 'Hubo un error al enviar el mensaje', 'error');
      }finally{
        this.sendingMessage = false;
      }
    },
    formatDateChat(date){
      return utils.formatDateForChat(date);
    },
    formatEventDate(date){
      let dateFormatted = utils.splitDateTime(date);
      return dateFormatted.date + ' ' + dateFormatted.time;
    },
    translateTypeEvent(value) {
      switch (value) {
        case 'meeting':
          return 'Reunión';
        case 'session':
          return 'Sesión';
        case 'birthday':
          return 'Cumpleaños';
        case 'other':
          return 'Otro';
        default:
          return value;
      }
    },
    onTabChange(event) {
      const activeIndex = event.index;
      this.showInput = (activeIndex === 1);
    },
    adjustTextareaHeight(event) {
      const textarea = event.target;
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
    },
    closeModal() {
      this.$emit('update:visible', false);
    },
    startTimer() {
      this.timer = setTimeout(() => {
        if (this.localEvents.length === 0) {
          this.localEvents = [];
          this.loading = false;
        }
      }, 5000); 
    },
    resetModal() {
      this.loading = true; 
      this.localEvents = []; 
      clearTimeout(this.timer); 
      this.startTimer(); 
    },
    async getGroupMessages(){
      this.idGroup = this.group.id;
      if(this.idGroup){
        try {
          this.gettingChat = true;
          const response = await getGroupById(this.idGroup);
          if(response){
            if(response.status === "success"){
              this.messages = response.data.messages
              this.gettingChat = false;
            }
          }
        } catch (error) {
          onToast('error', 'Error', 'Ocurrió un error al obtener los mensajes del grupo');
        }finally{
          this.gettingChat = false;
        }
      }
    }
  },
  mounted() {
    this.getGroupMessages()
    this.scrollToBottom();
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  }
};
</script>

<style lang="scss" scoped>
@import '@/styles/colors';

.no-events-img {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-timestamp {
  font-size: 0.75rem;
  color: #b0b0b0;
  float: right;
  margin-left: 10px; 
}


.chat-content {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.5rem;
  margin-bottom: 15px;
  width: auto;
  max-width: 80%;
  word-wrap: break-word; 
  overflow-wrap: break-word;
  color: black;
  position: relative;
}

.chat-username {
  font-weight: bold;
  font-size: 0.85rem;
  color: $sidebar-items; 
  display: block;
  margin-bottom: 0.2rem;
}


.chat-input-container {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-top: 0.5px solid #ddd; 
}

.chat-input {
  width: 80%;
  padding: 0.5rem;
  border: 0.5px solid #ccc;
  border-radius: 10px;
  margin-right: 0.5rem;
  resize: none;
  overflow: hidden;
  transition: height 0.2s ease;
}

.send-button {
  padding: 0.5rem 1rem;
  background-color: $primary-color;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover {
  background-color: darken($primary-color, 10%);
}

.chat-input {
  width: 80%;
  padding: 0.5rem;
  border: 0.5px solid #ccc;
  border-radius: 10px;
}

.custom-dialog {
  .p-dialog {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  
  .p-dialog-enter-active,
  .p-dialog-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
  
  .p-dialog-enter, .p-dialog-leave-to {
    opacity: 0;
    transform: scale(0.9);
  }

  .tab-content-scrollable {
    max-height: 300px;
    overflow-y: auto;
    padding-right: 1rem;
  }

  .skeleton-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .skeleton-item {
    height: 1.5rem;
    background-color: #e0e0e0;
    border-radius: 4px;
    animation: pulse 1.5s infinite ease-in-out;
  }
  
  @keyframes pulse {
    0% {
      background-color: #e0e0e0;
    }
    50% {
      background-color: #c0c0c0;
    }
    100% {
      background-color: #e0e0e0;
    }
  }

  .event-container {
    margin-bottom: 0.5rem;
    border-bottom: solid 1px #dddddd;
    padding-bottom: 0.3rem;
    transition: all 0.3s ease;
  }

  .event-container--small {
    margin-bottom: 0.9rem;
  }

  .event-header {
    padding: 0.2rem;
    margin-bottom: 0.3rem;
    font-size: 1rem;
    border-bottom: solid 1px #dddddd;
  }

  p {
    margin: 0.2rem 0;
    font-size: 1rem;
    line-height: 1.5;
  }

  .button-options {
    background: $primary-color;
    color: white;
    border: none;
    border-radius: 5px;
  }
  
  .button-options:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(72, 70, 70, 0.3);
    background: $primary-color !important;
    cursor: pointer;
  }
}
</style>

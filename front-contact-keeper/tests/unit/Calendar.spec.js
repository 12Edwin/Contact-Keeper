import { shallowMount } from '@vue/test-utils';
import Calendar from '@/modules/events/views/Calendar.vue';
import FullCalendar from '@fullcalendar/vue';
import ModalEventInfo from '@/modules/events/components/ModalEventInfo.vue';
import ModalAddEvent from '@/modules/events/components/ModalAddEvent.vue';
import Loader from "@/components/Loader.vue";
import Panel from 'primevue/panel';
import Chip from 'primevue/chip';

jest.mock('@fullcalendar/vue', () => ({
    name: 'FullCalendar',
    props: ['options', 'events'],
    render: () => null,
  }));
  
  describe('Calendar.vue', () => {
    let wrapper;
  
    beforeEach(() => {
      wrapper = shallowMount(Calendar, {
        global: {
          components: {
            FullCalendar,
            Loader,
            ModalEventInfo,
            ModalAddEvent,
            Panel,
            Chip,
          },
        },
      });
    });
  
    it('debería renderizar correctamente', () => {
      expect(wrapper.exists()).toBe(true);
    });
  
    it('debería mostrar el componente Loader cuando isLoading es verdadero', async () => {
      wrapper.setData({ isLoading: true });
      await wrapper.vm.$nextTick();
      expect(wrapper.findComponent(Loader).exists()).toBe(true);
    });
  
    it('debería mostrar el calendario cuando isLoading es falso', async () => {
      wrapper.setData({ isLoading: false });
      await wrapper.vm.$nextTick();
      expect(wrapper.find('.calendar-container').exists()).toBe(true);
    });
  
    it('debería abrir el modal de información del evento al hacer clic en un evento del calendario', async () => {
      const mockEvent = {
        title: 'Evento de prueba',
        start: new Date(),
        end: new Date(),
        extendedProps: {
          description: 'Descripción del evento',
          status: 'info',
          participants: 'Test'
        }
      };
      wrapper.vm.handleEventClick(mockEvent);
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.selectedEvent).toEqual({
        title: 'Evento de prueba',
        startDate: new Date().toISOString().split('T')[0],
        endDate: new Date().toISOString().split('T')[0],
        description: 'Descripción del evento',
        status: 'info',
        participants: 'Test',
      });
      expect(wrapper.vm.showModalEventInfo).toBe(true);
    });
  
    it('debería formatear las fechas correctamente', () => {
      const formattedDate = wrapper.vm.formatCalendarDate('2024-07-18');
      expect(formattedDate).toBe('2024-07-18');
    });
  });
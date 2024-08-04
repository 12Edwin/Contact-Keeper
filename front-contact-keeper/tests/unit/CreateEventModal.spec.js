import { shallowMount } from '@vue/test-utils';
import CreateEventModal from '@/modules/events/components/CreateEventModal.vue'; // Ajusta la ruta según tu estructura
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import PickList from 'primevue/picklist';

describe('CreateEventModal.vue', () => {
    let wrapper;
  
    beforeEach(() => {
      wrapper = shallowMount(CreateEventModal, {
        global: {
          components: {
            Dialog,
            InputText,
            Dropdown,
            Button,
            PickList
          }
        }
      });
    });
  
    it('debería renderizar correctamente', () => {
      expect(wrapper.exists()).toBe(true);
    });
  
    it('debería mostrar el Dialog cuando visible es verdadero', () => {
      expect(wrapper.findComponent(Dialog).exists()).toBe(true);
    });
  
    it('debería inicializar con los datos por defecto', () => {
      expect(wrapper.vm.event).toEqual({
        name: '',
        type: null,
        invites: null
      });
      expect(wrapper.vm.types).toEqual([
        { label: 'Tipo 1', value: 'tipo1' },
        { label: 'Tipo 2', value: 'tipo2' }
      ]);
      expect(wrapper.vm.invites).toEqual([
        { label: 'Invitado 1', value: 'invitado1' },
        { label: 'Invitado 2', value: 'invitado2' }
      ]);
      expect(wrapper.vm.users).toEqual([
        { name: 'Usuario 1' },
        { name: 'Usuario 2' }
      ]);
      expect(wrapper.vm.guests).toEqual([
        { name: 'Invitado 1' },
        { name: 'Invitado 2' }
      ]);
    });
  
    it('debería llamar a createEvent cuando se hace clic en el botón Crear', async () => {
      const createEventSpy = jest.spyOn(wrapper.vm, 'createEvent');
      await wrapper.findAllComponents(Button)[0].trigger('click'); // Primer botón, Crear
      expect(createEventSpy).toHaveBeenCalled();
    });
  
    it('debería emitir el evento close al hacer clic en el botón Cancelar', async () => {
      await wrapper.findAllComponents(Button)[1].trigger('click'); // Segundo botón, Cancelar
      expect(wrapper.emitted().close).toBeTruthy();
    });
  
    it('debería llamar a onMoveToTarget cuando se mueven ítems al target en PickList', async () => {
      const mockEvent = { items: ['item1'] };
      const onMoveToTargetSpy = jest.spyOn(wrapper.vm, 'onMoveToTarget');
      await wrapper.findComponent(PickList).vm.$emit('moveToTarget', mockEvent);
      expect(onMoveToTargetSpy).toHaveBeenCalledWith(mockEvent);
    });
  
    it('debería llamar a onMoveToSource cuando se mueven ítems al source en PickList', async () => {
      const mockEvent = { items: ['item1'] };
      const onMoveToSourceSpy = jest.spyOn(wrapper.vm, 'onMoveToSource');
      await wrapper.findComponent(PickList).vm.$emit('moveToSource', mockEvent);
      expect(onMoveToSourceSpy).toHaveBeenCalledWith(mockEvent);
    });
  });
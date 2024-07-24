import { mount } from '@vue/test-utils';
import ModalAddEvent from '@/modules/events/components/ModalAddEvent.vue'; 


// Run Prueba
// yarn test:unit -- ModalAddEvent.spec.js

describe('ModalAddEvent.vue', () => {
  it('debería mostrar el modal cuando visible es true', async () => {
    const wrapper = mount(ModalAddEvent, {
      props: {
        visible: true,
      },
    });

    expect(wrapper.findComponent({ name: 'Dialog' }).props('visible')).toBe(true);
  });

  it('debería llamar a closeModal cuando se hace clic en el botón "Cancelar"', async () => {
    const wrapper = mount(ModalAddEvent, {
      props: {
        visible: true,
      },
    });

    const closeModalSpy = jest.spyOn(wrapper.vm, 'closeModal');
    await wrapper.find('button.p-button-text').trigger('click');
    
    expect(closeModalSpy).toHaveBeenCalled();
  });

  it('debería emitir el evento "update:visible" con valor false cuando se llama closeModal', async () => {
    const wrapper = mount(ModalAddEvent, {
      props: {
        visible: true,
      },
    });

    await wrapper.vm.closeModal();

    expect(wrapper.emitted('update:visible')[0]).toEqual([false]);
  });

  it('debería validar el campo título correctamente', async () => {
    const wrapper = mount(ModalAddEvent, {
      props: {
        visible: true,
      },
    });

    const input = wrapper.find('#title');
    await input.setValue('Evento');
    await input.trigger('input');

    expect(wrapper.vm.v$.title.$model).toBe('Evento');
    expect(wrapper.vm.v$.title.$error).toBe(false);
  });

});

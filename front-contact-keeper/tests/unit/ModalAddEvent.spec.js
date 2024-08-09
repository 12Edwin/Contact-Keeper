import { mount } from '@vue/test-utils';
import ModalAddEvent from '@/modules/events/components/ModalAddEvent.vue';

describe('ModalAddEvent.vue', () => {
  it('debería mostrar el modal cuando visible es true', () => {
    const wrapper = mount(ModalAddEvent, {
      propsData: {
        visible: true
      }
    });

    // Asegúrate de que el componente Dialog esté correctamente renderizado
    const dialog = wrapper.findComponent({ name: 'Dialog' });
    expect(dialog.exists()).toBe(true);
    expect(dialog.props('visible')).toBe(true);
  });

  it('debería llamar a closeModal cuando se hace clic en el botón "Cancelar"', async () => {
    const wrapper = mount(ModalAddEvent, {
      propsData: {
        visible: true
      }
    });

    // Usa un selector más específico si es necesario
    const button = wrapper.find('button.p-button-text');
    expect(button.exists()).toBe(true);

    const closeModalSpy = jest.spyOn(wrapper.vm, 'closeModal');
    await button.trigger('click');

    expect(closeModalSpy).toHaveBeenCalled();
  });

  it('debería validar el campo título correctamente', async () => {
    const wrapper = mount(ModalAddEvent, {
      propsData: {
        visible: true
      }
    });

    const input = wrapper.find('#title');
    expect(input.exists()).toBe(true);

    await input.setValue('Evento');
    await input.trigger('input');

    expect(wrapper.vm.v$.title.$model).toBe('Evento');
  });
});

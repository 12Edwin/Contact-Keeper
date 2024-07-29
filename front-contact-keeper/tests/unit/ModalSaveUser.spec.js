import { mount, shallowMount } from '@vue/test-utils';
import ModalSaveUser from '@/modules/users/components/ModalSaveUser.vue';
import { nextTick } from 'vue';

describe('ModalSaveUser.vue', () => {
  // Prueba de abierto del modal
  it('muestra el modal cuando la prop visible es verdadera', () => {
    const wrapper = mount(ModalSaveUser, {
      props: { visible: true },
    });
    expect(wrapper.findComponent({ name: 'Dialog' }).exists()).toBe(true);
  });

  it('oculta el modal cuando la prop visible es falsa', async () => {
    const wrapper = mount(ModalSaveUser, {
      props: { visible: false },
    });
    await nextTick(); // Asegura que Vue procese el cambio de props
    expect(wrapper.findComponent({ name: 'Dialog' }).exists()).toBe(false);
  });

  // Prueba de validaciones
  it('muestra mensaje de error si el nombre está vacío', async () => {
    const wrapper = shallowMount(ModalSaveUser, {
      props: { visible: true },
    });

    await wrapper.setData({ person: { name: '' } });
    await wrapper.vm.v$.$touch();

    expect(wrapper.text()).toContain('El nombre es requerido');
  });

  // Prueba del método saveUser
  it('no guarda el usuario si hay errores de validación', async () => {
    const wrapper = shallowMount(ModalSaveUser, {
      props: { visible: true }
    });

    await wrapper.setData({ person: { name: '' } });
    await wrapper.vm.v$.$touch();

    const saveUserSpy = jest.spyOn(wrapper.vm, 'saveUser');
    wrapper.vm.saveUser();
    
    expect(saveUserSpy).not.toHaveBeenCalled();
  });

  it('guarda el usuario si no hay errores de validación', async () => {
    const wrapper = shallowMount(ModalSaveUser, {
      props: { visible: true }
    });

    await wrapper.setData({ 
      person: { name: 'John', surname: 'Doe', lastname: 'Smith', email: 'john.doe@example.com', phone: '1234567890', password: 'Password1!', user_type: 'admin', username: 'johndoe' }
    });
    await wrapper.vm.v$.$touch();

    const saveUserSpy = jest.spyOn(wrapper.vm, 'saveUser');
    wrapper.vm.saveUser();

    expect(saveUserSpy).toHaveBeenCalled();
  });
});

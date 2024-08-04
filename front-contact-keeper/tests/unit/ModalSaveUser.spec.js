import { mount, shallowMount } from "@vue/test-utils";
import ModalSaveUser from "@/modules/users/components/ModalSaveUser.vue";
import VueCompositionAPI from "@vue/composition-api";
import Vue from "vue";

Vue.use(VueCompositionAPI);

describe("ModalSaveUser.vue", () => {
  it("muestra el modal cuando la prop visible es verdadera", () => {
    const wrapper = mount(ModalSaveUser, {
      propsData: { visible: true },
    });
    expect(wrapper.findComponent({ name: "Dialog" }).exists()).toBe(true);
  });

  it('cierra el modal al darle click en el boton "cancelar"', async () => {
    const wrapper = mount(ModalSaveUser, {
      propsData: {
        visible: true
      }
    });
    const button = wrapper.find('button.p-button-text');
    expect(button.exists()).toBe(true);

    const closeModalSpy = jest.spyOn(wrapper.vm, 'closeModal');
    await button.trigger('click');

    expect(closeModalSpy).toHaveBeenCalled();
  });


  it("muestra mensaje de error si el nombre está vacío", async () => {
    const wrapper = shallowMount(ModalSaveUser, {
      props: { visible: true },
    });

    await wrapper.setData({ person: { name: "" } });
    await wrapper.vm.v$.$touch();

    expect(wrapper.text()).toContain("El nombre es requerido");
  });

  it("guarda el usuario si no hay errores de validación", async () => {
    const wrapper = shallowMount(ModalSaveUser, {
      props: { visible: true },
    });

    await wrapper.setData({
      person: {
        name: "John",
        surname: "Doe",
        lastname: "Smith",
        email: "john.doe@example.com",
        phone: "1234567890",
        password: "Password1!",
        user_type: "admin",
        username: "johndoe",
      },
    });
    await wrapper.vm.v$.$touch();

    const saveUserSpy = jest.spyOn(wrapper.vm, "saveUser");
    wrapper.vm.saveUser();

    expect(saveUserSpy).toHaveBeenCalled();
  });
});

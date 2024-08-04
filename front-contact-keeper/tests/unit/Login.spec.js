import { mount, shallowMount } from "@vue/test-utils";
import LoginComponent from "@/modules/login/views/Login.vue";
import VueCompositionAPI from "@vue/composition-api";
import Vue from "vue";

Vue.use(VueCompositionAPI);

describe("LoginComponent.vue", () => {
  it("muestra el formulario de inicio de sesión cuando isLoggingIn es verdadero", () => {
    const wrapper = shallowMount(LoginComponent, {
      data() {
        return {
          isLoggingIn: true,
        };
      },
    });
    expect(wrapper.find("form.login-form").exists()).toBe(true);
  });

  it("muestra el formulario de registro cuando isLoggingIn es falso", () => {
    const wrapper = shallowMount(LoginComponent, {
      data() {
        return {
          isLoggingIn: false,
        };
      },
    });
    expect(wrapper.findComponent({ name: "SignUp" }).exists()).toBe(true);
  });

  it("muestra mensaje de error si el correo está vacío", async () => {
    const wrapper = shallowMount(LoginComponent);
    await wrapper.setData({ credentials: { email: "", password: "password123" } });
    await wrapper.vm.v$.$touch();
    expect(wrapper.text()).toContain("El correo es requerido");
  });

  it("muestra mensaje de error si la contraseña está vacía", async () => {
    const wrapper = shallowMount(LoginComponent);
    await wrapper.setData({ credentials: { email: "test@example.com", password: "" } });
    await wrapper.vm.v$.$touch();
    expect(wrapper.text()).toContain("La contraseña es requerida");
  });

  it("inicia sesión correctamente cuando no hay errores de validación", async () => {
    const wrapper = shallowMount(LoginComponent);
    await wrapper.setData({
      credentials: { email: "test@example.com", password: "password123" },
    });
    await wrapper.vm.v$.$touch();

    const loginSpy = jest.spyOn(wrapper.vm, "login");
    wrapper.vm.login();

    expect(loginSpy).toHaveBeenCalled();
  });
});

import { mount, shallowMount } from "@vue/test-utils";
import SignUp from "@/modules/login/views/SignUp.vue";
import VueCompositionAPI from "@vue/composition-api";
import Vue from "vue";

Vue.use(VueCompositionAPI);

describe("SignUp.vue", () => {
  it("muestra el formulario de registro", () => {
    const wrapper = shallowMount(SignUp);
    expect(wrapper.find("form.login-form").exists()).toBe(true);
  });

  it('cambia a formulario de inicio de sesión al hacer click en "Iniciar sesión"', async () => {
    const wrapper = mount(SignUp);
    const button = wrapper.find("button.p-button-text");
    expect(button.exists()).toBe(true);

    await button.trigger("click");
    expect(wrapper.emitted().showLoginForm).toBeTruthy();
  });

  it("muestra mensaje de error si el nombre de usuario está vacío", async () => {
    const wrapper = shallowMount(SignUp);
    await wrapper.setData({ username: "", password: "password123" });
    await wrapper.vm.$forceUpdate(); 
    const form = wrapper.find("form");
    await form.trigger("submit.prevent");

    expect(wrapper.find("input#username:invalid").exists()).toBe(true);
  });

  it("muestra mensaje de error si la contraseña está vacía", async () => {
    const wrapper = shallowMount(SignUp);
    await wrapper.setData({ username: "testuser", password: "" });
    await wrapper.vm.$forceUpdate();
    const form = wrapper.find("form");
    await form.trigger("submit.prevent");

    expect(wrapper.find("input#password:invalid").exists()).toBe(true);
  });
});

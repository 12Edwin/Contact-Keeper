import { mount, shallowMount } from "@vue/test-utils";
import Groups from "@/modules/groups/views/Groups.vue";
import VueCompositionAPI from "@vue/composition-api";
import Vue from "vue";
import Tooltip from "primevue/tooltip";
import Announcements from "@/modules/groups/components/GroupInfo.vue";

Vue.use(VueCompositionAPI);
Vue.directive("tooltip", Tooltip);

describe("Groups.vue", () => {
  beforeAll(() => {
    window.alert = jest.fn();
  });

  it("muestra la lista de grupos", () => {
    const wrapper = shallowMount(Groups);
    expect(wrapper.findAll(".card").length).toBe(wrapper.vm.groups.length);
  });

  it("abre el modal de información del grupo al hacer clic en el icono de información", async () => {
    const wrapper = mount(Groups);
    const infoIcon = wrapper.find(".pi-info-circle");
    await infoIcon.trigger("click");
    await Vue.nextTick();
    expect(wrapper.vm.showInfo).toBe(true);
    expect(wrapper.vm.groupSelected).toEqual(wrapper.vm.groups[0]);
  });

  it("muestra las iniciales del grupo correctamente", () => {
    const wrapper = shallowMount(Groups);
    const initials = wrapper.vm.getInitial(wrapper.vm.groups[0].name);
    expect(initials).toBe("GS");
  });

  it("renderiza el componente Announcements con las props correctas", async () => {
    const wrapper = mount(Groups);
    wrapper.setData({
      showInfo: true,
      groupSelected: wrapper.vm.groups[0],
    });
    await Vue.nextTick();
    const announcements = wrapper.findComponent(Announcements);
    expect(announcements.props().group).toEqual(wrapper.vm.groupSelected);
    expect(announcements.props().visible).toBe(true);
  });
});

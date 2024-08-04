// tests/unit/Users.spec.js
import { shallowMount, createLocalVue } from '@vue/test-utils';
import Users from '@/modules/users/views/Users.vue';
import Panel from 'primevue/panel';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ModalUserInfo from '@/modules/users/components/ModalUserInfo.vue';
import ModalSaveUser from '@/modules/users/components/ModalSaveUser.vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

const localVue = createLocalVue();
localVue.component('Panel', Panel);
localVue.component('DataTable', DataTable);
localVue.component('Column', Column);
localVue.component('ModalUserInfo', ModalUserInfo);
localVue.component('ModalSaveUser', ModalSaveUser);
localVue.component('InputText', InputText);
localVue.component('Button', Button);

describe('Users.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(Users, {
      localVue,
      data() {
        return {
          users: [
            { name: 'Raúl Domínguez', role: 'Anfitrión', email: '20213tn103@utez.edu.mx' },
            { name: 'Edwin Barragán', role: 'Invitado', email: '20213tn046@utez.edu.mx' },
            { name: 'Carlos González', role: 'Invitado', email: '20203tn103@utez.edu.mx' },
            { name: 'Noé Mérida', role: 'Invitado', email: '20213tn056@utez.edu.mx' },
            { name: 'Yahir Degante', role: 'Anfitrión', email: '20213tn103@utez.edu.mx' }
          ]
        }
      },
      stubs: ['Panel', 'DataTable', 'Column', 'ModalUserInfo', 'ModalSaveUser', 'InputText', 'Button']
    });
  });

  it('debería renderizar correctamente', () => {
    expect(wrapper.exists()).toBe(true);
  });

  it('debería mostrar el nombre del grupo en el encabezado', () => {
    const panelHeader = wrapper.findComponent(Panel).props('header');
    expect(panelHeader).toBe('Usuarios');
  });

  it('debería emitir un evento cuando se selecciona un usuario', async () => {
    const dataTable = wrapper.findComponent(DataTable);
    await dataTable.vm.$emit('row-select', { data: { name: 'Raúl Domínguez', role: 'Anfitrión', email: '20213tn103@utez.edu.mx' } });
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.displayModal).toBe(true);
    expect(wrapper.vm.selectedUser).toEqual({ name: 'Raúl Domínguez', role: 'Anfitrión', email: '20213tn103@utez.edu.mx' });
  });

  it('debería cambiar el placeholder cuando se cambia el tipo de búsqueda', async () => {
    await wrapper.vm.changeSearch();
    await wrapper.vm.$nextTick();

    const inputText = wrapper.findComponent(InputText);
    const placeholder = inputText.attributes('placeholder');
    expect(placeholder).toBe('Buscar por correo..');
  });

  it('debería abrir el modal para agregar un nuevo usuario', async () => {
    await wrapper.vm.openSaveModal();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.displaySaveModal).toBe(true);
  });
});
import { shallowMount, createLocalVue } from '@vue/test-utils';
import GroupInfo from '@/modules/groups/components/GroupInfo.vue'; // Asegúrate de que la ruta sea correcta
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
import Tooltip from 'primevue/tooltip';
import { fail } from '@jest/globals';

const localVue = createLocalVue();
localVue.directive('tooltip', Tooltip);

describe('GroupInfo.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(GroupInfo, {
      localVue,
      propsData: {
        visible: true,
        group: {
          name: 'Grupo Test',
          description: 'Descripción del grupo',
          members: [
            { name: 'Miembro 1', role: 'Rol 1' },
            { name: 'Miembro 2', role: 'Rol 2' }
          ]
        }
      },
      global: {
        components: {
          Dialog,
          Button,
          Avatar
        }
      }
    });
  });

  it('debería renderizar correctamente', () => {
    const result = wrapper.exists();
    console.log('Renderización Correcta:', result);
    expect(result).toBe(true);
  });

  it('debería mostrar el nombre del grupo en el encabezado', () => {
    const header = wrapper.find('h4'); // Verifica que este sea el selector correcto
    expect(header.exists()).toBe(true); // Asegúrate de que el elemento existe
    const headerText = header.text();
    const expectedText = 'Grupo Test';
    console.log('Nombre del Grupo en Encabezado:', headerText === expectedText);
    expect(headerText).toBe(expectedText);
  });

  it('debería mostrar los miembros del grupo', () => {
    const memberLabels = wrapper.findAll('.username').wrappers.map(wrapper => wrapper.text());
    const expectedLabels = ['Miembro 1', 'Miembro 2'];
    const result = memberLabels.every((label, index) => label === expectedLabels[index]);
    console.log('Miembros del Grupo:', result);
    expect(result).toBe(true);
  });

  it('debería emitir el evento update:visible cuando se hace clic en el botón Cancelar', async () => {
    const cancelButton = wrapper.findAllComponents(Button).wrappers.find(button => button.text() === 'Cancelar');
    if (cancelButton) {
      await cancelButton.trigger('click');
      await wrapper.vm.$nextTick();
      const emittedEvents = wrapper.emitted('update:visible');
      const result = emittedEvents && emittedEvents.length > 0;
      console.log('Evento update:visible Emitido:', result);
      expect(result).toBe(true);
    } else {
      console.log('Botón Cancelar no encontrado');
      throw new Error('Botón Cancelar no encontrado');
    }
  });

  it('debería aplicar la directiva tooltip en el ícono', () => {
    const icon = wrapper.find('.icon-styles');
    expect(icon.exists()).toBe(true); // Asegúrate de que el ícono existe
    const tooltipAttr = icon.attributes('aria-describedby'); // Verifica el atributo correcto
    const expectedTooltip = 'Expulsar';
    const hasTooltip = tooltipAttr === expectedTooltip;
    console.log('Directiva Tooltip Aplicada:', hasTooltip);
    expect(hasTooltip).toBe(true);
  });
  
});
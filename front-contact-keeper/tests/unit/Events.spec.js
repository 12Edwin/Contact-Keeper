import { shallowMount } from '@vue/test-utils';
import Events from '@/modules/events/views/Events.vue'; 
import Panel from 'primevue/panel';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import CreateEventModal from '@/modules/events/components/CreateEventModal.vue'; 
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

describe('Events.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(Events, {
      global: {
        components: {
          Panel,
          DataTable,
          Column,
          CreateEventModal,
          InputText,
          Button
        }
      }
    });
  });

  it('debería renderizar correctamente', () => {
    const result = wrapper.exists();
    console.log('Renderización Correcta:', result);
    expect(result).toBe(true);
  });

  it('debería mostrar el panel con el título Eventos', () => {
    const panel = wrapper.findComponent(Panel);
    const result = panel.exists() && panel.props('header') === 'Eventos';
    console.log('Panel con Título Eventos:', result);
    expect(result).toBe(true);
  });

  it('debería mostrar la barra de búsqueda y el botón Agregar evento', () => {
    const inputTextExists = wrapper.findComponent(InputText).exists();
    const buttonExists = wrapper.findComponent(Button).exists();
    const buttonLabel = wrapper.findComponent(Button).attributes('label') === 'Agregar evento';
    const result = inputTextExists && buttonExists && buttonLabel;
    console.log('Barra de Búsqueda y Botón Agregar Evento:', result);
    expect(result).toBe(true);
  });
  
  it('debería mostrar el modal CreateEventModal cuando showModal es verdadero', async () => {
    await wrapper.setData({ showModal: true });
    const result = wrapper.findComponent(CreateEventModal).exists();
    console.log('Mostrar Modal CreateEventModal:', result);
    expect(result).toBe(true);
  });

  it('debería ocultar el modal CreateEventModal cuando showModal es falso', async () => {
    await wrapper.setData({ showModal: false });
    const result = !wrapper.findComponent(CreateEventModal).exists();
    console.log('Ocultar Modal CreateEventModal:', result);
    expect(result).toBe(true);
  });

  it('debería mostrar la tabla con los eventos', () => {
    const dataTable = wrapper.findComponent(DataTable);
    const result = dataTable.exists() && dataTable.props('value').length === 2;
    console.log('Mostrar Tabla con Eventos:', result);
    expect(result).toBe(true);
  });
});
import { shallowMount } from '@vue/test-utils'
import Calendar from '@/modules/events/views/Calendar.vue'

//Para ejecutar esta prueba
//yarn test:unit -- calendar.spec.js

//Prueba de renderizado de mensajes
describe('Calendar', () => {
    it('renders a static message', () => {
        const wrapper = shallowMount(Calendar)
        expect(wrapper.text()).toContain('Static Message')
      })
    })


//Prueba de existencia de elementos
it('contains a specific class', () => {
    const wrapper = shallowMount(Calendar)
    expect(wrapper.find('.my-class').exists()).toBe(true)
  })


//Pruebas de propiedades
it('renders props.title correctly', () => {
  const title = 'Test Title'
  const wrapper = shallowMount(Calendar, {
    propsData: { title }
  })
  expect(wrapper.find('h1').text()).toBe(title)
})


//Prueba de atributos
it('sets the correct alt attribute for the image', () => {
    const altText = 'Image Alt Text'
    const wrapper = shallowMount(Calendar, {
      propsData: { altText }
    })
    expect(wrapper.find('img').attributes('alt')).toBe(altText)
  })

  
//Prueba de Estilos
it('applies the correct style to the element', () => {
    const wrapper = shallowMount(Calendar)
    expect(wrapper.find('.my-class').element.style.color).toBe('red')
  })

//Prueba de componentes hijos
it('renders child component', () => {
    const wrapper = shallowMount(Calendar)
    expect(wrapper.findComponent({ name: 'ChildComponent' }).exists()).toBe(true)
  })



  
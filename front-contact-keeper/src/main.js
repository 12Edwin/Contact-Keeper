import Vue from 'vue'
import App from './App.vue'
import router from './router'

// Bootstrap Vue
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

// PrimeVue
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/saga-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
Vue.use(PrimeVue)

// PrimeVue components
import Button from 'primevue/button'
import Panel from 'primevue/panel'
import InputText from 'primevue/inputtext'
import DataView from 'primevue/dataview'
import Toolbar from 'primevue/toolbar'
import Card from 'primevue/card'
import Dialog from 'primevue/dialog'
import Sidebar from 'primevue/sidebar'
import Avatar from 'primevue/avatar'
import Menu from 'primevue/menu'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Divider from "primevue/divider";
import Password from "primevue/password";
import Dropdown from 'primevue/dropdown';
import Checkbox from 'primevue/checkbox';


Vue.component('Button', Button)
Vue.component('Panel', Panel)
Vue.component('InputText', InputText)
Vue.component('DataView', DataView)
Vue.component('Toolbar', Toolbar)
Vue.component('Card', Card)
Vue.component('Dialog', Dialog)
Vue.component('Sidebar', Sidebar)
Vue.component('Avatar', Avatar)
Vue.component('Menu', Menu)
Vue.component('DataTable', DataTable)
Vue.component('Column', Column)
Vue.component('Divider', Divider)
Vue.component('Password', Password)
Vue.component('Dropdown', Dropdown)
Vue.component('Checkbox', Checkbox)
Vue.directive('tooltip', Tooltip);
Vue.component('Card', Card)
// PrimeVue services
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'
Vue.use(ConfirmationService)
Vue.use(ToastService)

// PrimeVue directives
import Tooltip from 'primevue/tooltip'
Vue.directive('tooltip', Tooltip)

// Axios
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)

// Global styles
import '@/styles/colors.scss'

Vue.config.productionTip = false

// Vue composition
import VueCompositionAPI from '@vue/composition-api'
Vue.use(VueCompositionAPI)


new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
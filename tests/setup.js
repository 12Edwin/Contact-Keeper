import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import Panel from 'primevue/panel';
import InputText from 'primevue/inputtext';
import DataView from 'primevue/dataview';
import Toolbar from 'primevue/toolbar';
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';
import Sidebar from 'primevue/sidebar';
import Avatar from 'primevue/avatar';
import Menu from 'primevue/menu';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Divider from 'primevue/divider';
import Password from 'primevue/password';
import Dropdown from 'primevue/dropdown';
import Checkbox from 'primevue/checkbox';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

// Make PrimeVue available throughout your project
Vue.use(PrimeVue);
Vue.use(ConfirmationService);
Vue.use(ToastService);

// Register PrimeVue components globally
Vue.component('Button', Button);
Vue.component('Panel', Panel);
Vue.component('InputText', InputText);
Vue.component('DataView', DataView);
Vue.component('Toolbar', Toolbar);
Vue.component('Card', Card);
Vue.component('Dialog', Dialog);
Vue.component('Sidebar', Sidebar);
Vue.component('Avatar', Avatar);
Vue.component('Menu', Menu);
Vue.component('DataTable', DataTable);
Vue.component('Column', Column);
Vue.component('Divider', Divider);
Vue.component('Password', Password);
Vue.component('Dropdown', Dropdown);
Vue.component('Checkbox', Checkbox);

// Register PrimeVue directives globally
Vue.directive('tooltip', Tooltip);

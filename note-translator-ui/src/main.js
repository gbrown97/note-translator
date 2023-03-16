import { createApp } from 'vue'
import App from './App.vue'
import vueRouter, {createRouter, createWebHistory} from 'vue-router'
import signup from './components/Signup.vue'
import note from './components/noteTransl.vue'
const routes = [
    {path: '/', component:  note},
    {path: '/signup', component: signup}
];
const router= createRouter({
    history: createWebHistory(),
    routes:routes,
});

const app=createApp(App);
app.use(router)
app.mount('#app')

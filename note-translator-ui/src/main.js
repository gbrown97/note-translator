import { createApp } from 'vue'
import App from './App.vue'
import  {createRouter, createWebHistory} from 'vue-router'
import signup from './components/Signup.vue'
import note from './components/noteTransl.vue'
import profile from './components/profile.vue'
import home from './components/homePage.vue'
import upload from './components/uploading.vue'

const routes = [
    {path: '/', component:  note},
    {path: '/signup', component: signup},
    {path: '/home', component:  home},
    {path: '/profile', component: profile},
    {path: '/upload', component: upload}

];
const router= createRouter({
    history: createWebHistory(),
    routes:routes,
});

const app=createApp(App);

app.use(router)
app.mount('#app')

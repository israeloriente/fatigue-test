import { createApp } from "vue";
import App from "./App.vue";
import "./style.scss";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from 'pinia';
import 'bootstrap/dist/css/bootstrap.min.css';

// Defina suas rotas
const routes = [
  {
    path: "/",
    component: () => import("./pages/HomePage.vue"),
  },
  {
    path: "/about",
    component: () => import("./pages/AboutPage.vue"),
  },
  {
    path: "/config",
    component: () => import("./pages/ConfigPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Crie e registre o Vue Router na aplicação
const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount("#app");

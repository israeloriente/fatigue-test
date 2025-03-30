import { createApp } from "vue";
import App from "./App.vue";
import "./style.scss";
import { createRouter, createWebHashHistory } from "vue-router";
import { createPinia } from 'pinia';
import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
import pt from "./locales/pt.json";
import VueSweetalert2 from 'vue-sweetalert2';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'sweetalert2/dist/sweetalert2.min.css';

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
  history: createWebHashHistory(),
  routes,
});

const i18n = createI18n({
  legacy: false,
  locale: "pt",
  messages: {
    en,
    pt,
  },
});

// Crie e registre o Vue Router na aplicação
const app = createApp(App);
app.use(router);
app.use(i18n);
app.use(VueSweetalert2)
app.use(createPinia());
app.mount("#app");

export { i18n };

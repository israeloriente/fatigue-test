import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";

// Defina suas rotas
const routes = [
  {
    path: "/",
    component: () => import("./pages/HomePage.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Crie e registre o Vue Router na aplicação
const app = createApp(App);
app.use(router);
app.mount("#app");

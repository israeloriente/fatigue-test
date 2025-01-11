<template>
  <div class="toolbar">
    <h1>{{ title }}</h1>
    <div class="links">
      <router-link to="/"> {{ $t("toolbar.home") }} </router-link>
      <router-link to="/about"> {{ $t("toolbar.about") }} </router-link>
      <router-link to="/config"> {{ $t("toolbar.settings") }} </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Toolbar",
  computed: {
    title() {
      switch (this.$route.path) {
        case "/home":
          return "Home Page";
        case "/about":
          return "About Page";
        case "/config":
          return "Config";
        default:
          return "Home";
      }
    },
  },
};
</script>

<style scoped lang="scss">
.toolbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1%;
  background-color: rgb(72, 163, 203);
  height: 30px;
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  h1 {
    font-size: larger;
    margin-top: 10px;
  }
}

.toolbar .links a {
  margin: 0 10px;
  text-decoration: none;
  color: white;
}
</style>

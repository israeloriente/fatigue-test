<template>
  <label class="switch">
    <input type="checkbox" v-model="localValue" @click="changed()" />
    <span class="slider round"></span>
  </label>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

// Defina as propriedades e eventos
const emit = defineEmits(["changed"]);
const props = defineProps({ value: Boolean });
const localValue = ref(props.value);

// Sincronize o valor local com as mudanças nas props
watch(
  () => props.value,
  (newValue) => {
    localValue.value = newValue;
  }
);

const changeLocalValue = () => {
  return (localValue.value = !localValue.value);
};

// Emita o evento quando o valor mudar
const changed = () => {
  emit("changed", !localValue.value);
};

defineExpose({
  changeLocalValue,
});
</script>

<style scoped lang="scss">
.switch {
  position: relative;
  display: inline-block;
  width: 30px;
  height: 17px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 13px;
  width: 13px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: rgb(72, 163, 203);
}

input:focus + .slider {
  box-shadow: 0 0 1px rgb(72, 163, 203);
}

input:checked + .slider:before {
  -webkit-transform: translateX(13px);
  -ms-transform: translateX(13px);
  transform: translateX(13px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>

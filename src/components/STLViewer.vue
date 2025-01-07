<template>
	<h1>Model 3D</h1>
	<div ref="rendererContainer" style="width: 100%; height: 100%;"></div>
  </template>

  <script>
  import { ref, onMounted } from "vue";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader";

  export default {
	name: "STLViewer",
	setup() {
	  const rendererContainer = ref(null);

	  onMounted(() => {
		const scene = new THREE.Scene();
		scene.background = new THREE.Color(0xeeeeee);

		const aspectRatio = rendererContainer.value.offsetWidth / rendererContainer.value.offsetHeight;
		const camera = new THREE.PerspectiveCamera(75, aspectRatio, 0.1, 1000);
		camera.position.set(3, 3, 3);

		const renderer = new THREE.WebGLRenderer({ antialias: true });
		renderer.setSize(rendererContainer.value.offsetWidth, rendererContainer.value.offsetHeight);
		rendererContainer.value.appendChild(renderer.domElement);

		// Adicionar luz direcional
		const light = new THREE.DirectionalLight(0xffffff, 1);
		light.position.set(10, 10, 10);
		scene.add(light);

		// Carregar o arquivo STL
		const loader = new STLLoader();
		loader.load("/model.stl", (geometry) => {
		  const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
		  const mesh = new THREE.Mesh(geometry, material);
		  scene.add(mesh);

		  // Ajustar a câmera para focar no objeto
		  const box = new THREE.Box3().setFromObject(mesh);
		  const size = box.getSize(new THREE.Vector3()).length();
		  const center = box.getCenter(new THREE.Vector3());
		  camera.position.copy(center.clone().add(new THREE.Vector3(size * 1.5, size * 1.5, size * 1.5)));
		  camera.lookAt(center);
		});

		// Função de animação
		const animate = () => {
		  requestAnimationFrame(animate);
		  renderer.render(scene, camera);
		};

		animate();
	  });

	  return {
		rendererContainer,
	  };
	},
  };
  </script>

  <style>
  /* Ajuste o tamanho do container */
  div {
	display: block;
	width: 100%;
	height: 100%;
  }
  </style>

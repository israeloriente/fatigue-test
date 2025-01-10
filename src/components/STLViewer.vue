<template>
  <div ref="container" class="three-container"></div>
</template>

<script>
import { markRaw } from "vue";
import * as THREE from "three";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default {
  data() {
    return {
      scene: markRaw(new THREE.Scene()),
      camera: markRaw(new THREE.PerspectiveCamera()),
      renderer: markRaw(new THREE.WebGLRenderer({ antialias: true, alpha: true })),
      controls: null,
    };
  },
  mounted() {
    this.initThree();
  },
  methods: {
    initThree() {
      this.camera.position.set(2, 44, 74);
      this.renderer.setClearColor(0x48a3cb, 0); // Transparente
      this.$refs.container.appendChild(this.renderer.domElement);

      const light = new THREE.AmbientLight(0xffffff, 1);
      this.scene.add(light);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(10, 10, 10);
      this.scene.add(directionalLight);
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.screenSpacePanning = true; // Permite pan em todos os sentidos
      this.controls.minPolarAngle = 0; // Permite olhar completamente para baixo
      this.controls.maxPolarAngle = Math.PI * 2; // Permite rotação completa
      this.controls.target.set(0, 0, 0); // Foco no alvo
      this.controls.update();
      this.animate();
      this.updateRendererSize();
      this.loadModel("src/assets/models/Dragon.stl");
    },
    animate() {
      requestAnimationFrame(this.animate);
      this.controls.update();
      this.renderer.render(this.scene, this.camera);
    },
    loadModel(path) {
      const loader = new STLLoader();
      loader.load(
        path,
        (geometry) => {
          // Cria o material e mesh
          const material = new THREE.MeshStandardMaterial();
          const mesh = new THREE.Mesh(geometry, material);
          mesh.rotation.x = 270 * (Math.PI / 180); // Rotaciona o objeto 90° no eixo Y
          mesh.position.set(0, -20, 0); // Posiciona o objeto no centro
          this.scene.add(mesh);
          this.updateRendererSize();
        },
        undefined,
        (error) => {
          console.error("Erro ao carregar o modelo STL:", error);
        }
      );
    },
    updateRendererSize() {
      const container = this.$refs.container;
      const { width, height } = container.getBoundingClientRect();
      this.renderer.setSize(width, height);
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
    },
  },
};
</script>

<style>
.three-container {
  width: 100%;
  height: 250px;
  overflow: hidden;
  position: relative;
  display: block;
  margin: auto;
  background-color: #48a3cb;
  border-radius: 25px;
}
</style>

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
      cameraCountAnimation: 1660,
      controls: null,
      timeout: null,
      directionalLight: null, // Armazena a luz direcional
    };
  },
  mounted() {
    this.initThree();
    window.addEventListener("scroll", this.handleScroll); // Adiciona o listener
  },
  unmounted() {
    window.removeEventListener("scroll", this.handleScroll); // Remove o listener
  },
  methods: {
    initThree() {
      this.camera.position.set(2, 44, 74);
      this.renderer.setClearColor(0x48a3cb, 0); // Transparente
      this.$refs.container.appendChild(this.renderer.domElement);

      const light = new THREE.AmbientLight(0xffffff, 1);
      this.scene.add(light);

      // Criação da luz direcional
      this.directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      this.directionalLight.position.set(10, 10, 10); // Posição inicial
      this.scene.add(this.directionalLight);

      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.screenSpacePanning = true; // Permite pan em todos os sentidos
      this.controls.minPolarAngle = 0; // Permite olhar completamente para baixo
      this.controls.maxPolarAngle = Math.PI * 2; // Permite rotação completa
      this.controls.target.set(0, 0, 0); // Foco no alvo
      this.controls.update();

      this.animate();
      this.updateRendererSize();
      this.loadModel("src/assets/models/Model.stl");
    },
    animate() {
      requestAnimationFrame(this.animate);
      this.controls.update();
      this.renderer.render(this.scene, this.camera);

      // Atualiza a posição da luz para seguir a câmera
      if (this.directionalLight) {
        this.directionalLight.position.copy(this.camera.position);
        this.directionalLight.target.position.copy(this.controls.target);
        this.directionalLight.target.updateMatrixWorld(); // Atualiza o alvo da luz
      }
    },
    loadModel(path) {
      const loader = new STLLoader();
      loader.load(
        path,
        (geometry) => {
          const material = new THREE.MeshStandardMaterial();
          const mesh = new THREE.Mesh(geometry, material);

          const boundingBox = new THREE.Box3().setFromObject(mesh);
          const boxSize = new THREE.Vector3();
          boundingBox.getSize(boxSize);
          const boxCenter = new THREE.Vector3();
          boundingBox.getCenter(boxCenter);
          mesh.position.set(-boxCenter.x, -boxCenter.y, -boxCenter.z);
          this.scene.add(mesh);

          const maxDim = Math.max(boxSize.x, boxSize.y, boxSize.z);
          this.camera.position.set(0, maxDim * 2, maxDim * 2);
          this.camera.lookAt(0, 0, 0);
          this.controls.target.set(0, 0, 0);
          this.controls.update();

          this.updateRendererSize();
        },
        undefined,
        (error) => {
          console.error("Erro ao carregar o modelo STL:", error);
        }
      );
    },
    handleScroll() {
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        const scrollPosition = window.scrollY + window.innerHeight;
        const pageHeight = document.documentElement.scrollHeight;

        if (scrollPosition >= pageHeight) {
          this.animateCamera();
          console.log("Chegou ao final da página!");
        }
      }, 100);
    },
    animateCamera() {
      if (this.cameraCountAnimation >= 800) {
        this.camera.position.set(0, this.cameraCountAnimation, this.cameraCountAnimation);
        this.cameraCountAnimation -= 8;
        requestAnimationFrame(this.animateCamera);
      } else {
        console.log("Animação concluída!");
      }
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

<template>
  <div ref="container" class="three-container"></div>
</template>

<script>
import { markRaw, onMounted, onUnmounted } from "vue";
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
      this.loadModel("src/assets/models/Model.stl");
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

          // Calcula o bounding box do objeto
          const boundingBox = new THREE.Box3().setFromObject(mesh);
          const boxSize = new THREE.Vector3();
          boundingBox.getSize(boxSize); // Tamanho do objeto
          const boxCenter = new THREE.Vector3();
          boundingBox.getCenter(boxCenter); // Centro do objeto
          mesh.position.set(-boxCenter.x, -boxCenter.y, -boxCenter.z);
          this.scene.add(mesh);
          // Ajusta a câmera para ficar na frente do objeto
          const maxDim = Math.max(boxSize.x, boxSize.y, boxSize.z); // Maior dimensão do objeto
          this.camera.position.set(0, 1660, 1660);
          // Posição diretamente na frente
          this.camera.lookAt(0, 0, 0); // Olha para o centro da cena
          this.controls.target.set(0, 0, 0); // Atualiza o foco da câmera
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
        this.cameraCountAnimation -= 7; // Incrementa o valor
        requestAnimationFrame(this.animateCamera); // Chama o próximo frame
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

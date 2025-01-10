<template>
  <div class="container">
    <h1>Sobre o Projeto - Teste de Carga Automatizado</h1>
    <p>
      Nosso projeto de faculdade foi desenvolvido com o objetivo de criar um sistema automatizado para realizar testes
      de carga em barras metálicas, utilizando tecnologias acessíveis e precisas. Ele combina sensores de carga com
      motores de passo para tensionar as barras, registrando dados fundamentais para análise estrutural.
    </p>

    <h2>Motivação do Projeto</h2>
    <p>
      A análise de resistência de materiais é essencial em diversas áreas da engenharia. Entretanto, métodos
      tradicionais de teste de carga muitas vezes requerem equipamentos caros e complexos. Buscando uma alternativa
      eficiente e econômica, desenvolvemos uma solução prática para realizar esses testes com alta precisão, utilizando
      sensores e atuadores controlados de forma programada.
    </p>

    <h2>Como Funciona</h2>
    <ul>
      <li>
        <strong>Sensor de Carga:</strong> Um sensor de carga foi integrado ao sistema para medir, em tempo real, a força
        aplicada à barra durante o processo de tensionamento. Esses dados são fundamentais para determinar o
        comportamento estrutural do material testado.
      </li>
      <li>
        <strong>Motor de Passo:</strong> Um motor de passo foi utilizado para aplicar a tensão de forma precisa e
        controlada. Ele permite ajustes minuciosos na força aplicada, garantindo a confiabilidade dos resultados.
      </li>
      <li>
        <strong>Barra de Teste:</strong> A barra metálica é fixada ao sistema, sendo tensionada progressivamente pelo
        motor enquanto o sensor monitora a força aplicada.
      </li>
      <li>
        <strong>Coleta e Análise de Dados:</strong> Os dados obtidos pelo sensor de carga são registrados e enviados
        para um sistema de monitoramento, onde são analisados para verificar os limites de elasticidade, resistência e
        deformação da barra.
      </li>
    </ul>

    <h2>Resultados Esperados</h2>
    <ul>
      <li>
        <strong>Confiabilidade:</strong> A utilização de sensores de alta precisão e motores de passo controlados
        garante resultados consistentes.
      </li>
      <li>
        <strong>Custo-benefício:</strong> O sistema foi projetado para ser mais acessível do que equipamentos
        industriais tradicionais.
      </li>
      <li>
        <strong>Automação:</strong> A combinação de hardware e software elimina a necessidade de intervenção manual
        durante o teste.
      </li>
    </ul>

    <h2>Aplicações Futuras</h2>
    <p>
      Este projeto pode ser expandido para testar outros materiais além de barras metálicas, como plásticos e
      compósitos, aumentando sua aplicabilidade em indústrias como construção civil, automotiva e aeroespacial. Além
      disso, melhorias no sistema, como o uso de sensores mais avançados e softwares de análise mais robustos, podem
      torná-lo uma ferramenta competitiva no mercado.
    </p>

    <h2>Equipe</h2>
    <p>
      O projeto foi desenvolvido por estudantes da <strong>[Nome do Curso]</strong> na
      <strong>[Nome da Instituição]</strong>, como parte de um trabalho de conclusão de curso. Nossa equipe foi
      responsável por todas as etapas do projeto, desde o design do sistema até a análise de resultados.
    </p>
  </div>
  <div class="row">
    <div class="col position-relative">
      <img src="../assets/gpi.jpeg" class="ml-3" alt="" />
    </div>
    <div class="col-6"><STLViewer /></div>
    <div class="col position-relative"><img src="../assets/brasao.jpeg" alt="" /></div>
  </div>
</template>

<script setup lang="ts">
import STLViewer from "../components/STLViewer.vue";
</script>

<style scoped>
.container {
  width: 100%;
  height: 60%;
  overflow: hidden;
  overflow-y: auto;
  padding: 5%;
  margin-bottom: 3%;
}
img {
  width: 40%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.position-relative {
  position: relative !important;
}
</style>

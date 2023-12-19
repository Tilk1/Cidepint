<template>
  <div>
    <Loading :loading="loading"></Loading>
    <canvas id="barras_verticales"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'
import Loading from './Loading.vue'
import ServicioEstadisticasClase from '../../services/EstadisticasServicio'

const data_api = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await new ServicioEstadisticasClase().getServiciosMasSolicitados()
    data_api.value = response
    loading.value = false
    renderChart()
  } catch (error) {
    console.log(error)
  }
})

function convertir_datos_a_grafico(jsonData) {
  const DataGrafico = {}
  jsonData.data.forEach((item) => {
    DataGrafico[item.servicio] = item.solicitudes
  })
  return DataGrafico
}

function renderChart() {
  const data = convertir_datos_a_grafico(data_api.value)
  const graph = document.getElementById('barras_verticales')
  new Chart(graph, {
    type: 'bar',
    options: {
      responsive: true
    },
    data: {
      labels: Object.keys(data),
      datasets: [
        {
          label: 'Servicios mas solicitados',
          data: Object.values(data),
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)'
          ],
          hoverOffset: 4
        }
      ]
    }
  })
}
</script>

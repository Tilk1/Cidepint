<template>
  <div>
    <Loading :loading="loading"></Loading>
    <canvas id="torta"></canvas>
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
  try{
    const response = await new ServicioEstadisticasClase().getSolicitudesPorEstado()
    data_api.value = response
    loading.value = false
    renderChart()
  }
  catch(error){
    console.log(error)
  }
})

function renderChart() {
  const data = data_api.value;
  const graph = document.getElementById('torta')
  new Chart(graph, {
    type: 'doughnut',
    options: {
      responsive: true
    },
    data: {
      labels: Object.keys(data),
      datasets: [
        {
          data: Object.values(data),
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)',
            'rgb(255, 159, 64)'
          ],
          hoverOffset: 4
        }
      ]
    }
  })
}
</script>

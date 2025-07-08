<template>
  <div v-if="visible" class="line-notif">
    <p v-if="loading">🔄 Chargement de l’état du trafic…</p>
    <div v-else>
      <p v-if="alertMessage">🚨 {{ alertMessage }}</p>
      <p v-else>✅ Aucune perturbation sur cette ligne.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const loading      = ref(false)
const alertMessage= ref(null)
const visible      = ref(false)

// Remplacez par **votre** token PRIM obtenu après inscription
const PRIM_TOKEN = 'VITE_PRIM_TOKEN'

async function fetchTraffic(lineParam) {
  loading.value = true
  alertMessage.value = null

  try {
    const res = await axios.get('/api/prim/idfm-disruptions_bulk',
      {
        headers: {
          Authorization: `Bearer ${PRIM_TOKEN}`
        }
      }
    )
    console.log('Réponse PRIM', res.status, res.data)
    const disruptions = res.data.disruptions || []
    // … ton filtrage …
  } catch (err) {
    console.error('Erreur API PRIM disruptions_bulk', err.response?.status, err.response?.data)
    alertMessage.value = `Erreur ${err.response?.status || ''}`
  } finally {
    loading.value = false
  }
}


function handleShowLine(e) {
  const lineParam = e.detail    // "ligne1", "ligne3b",…
  visible.value   = true
  fetchTraffic(lineParam)
}

onMounted(() => {
  window.addEventListener('show-line', handleShowLine)
})
onUnmounted(() => {
  window.removeEventListener('show-line', handleShowLine)
})
</script>

<style scoped>
.line-notif {
  position: absolute;
  top: 20px;
  right: 40px;
  background: #fff;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  min-width: 220px;
  font-family: sans-serif;
  z-index: 1000;
}
</style>

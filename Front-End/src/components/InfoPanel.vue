<template>
  <div class="info-panel">
    <!-- Connexity -->
    <div v-if="isConnexityView">
      <p v-if="loadingConnexity">Chargement de la connexité…</p>
      <p v-else-if="connexe">✅ Le graphe est <strong>connexe</strong>.</p>
      <p v-else>❌ Le graphe <strong>n'est pas</strong> connexe.</p>
    </div>

    <!-- Traffic -->
    <div v-if="isTrafficView">
      <p v-if="loadingTraffic">Chargement des alertes trafic…</p>
      <ul v-else>
        <li v-for="(alert, i) in trafficAlerts" :key="i">
          {{ alert.line }} – {{ alert.message }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

// états pour connexity
const loadingConnexity = ref(false)
const connexe         = ref(false)
// états pour traffic
const loadingTraffic  = ref(false)
const trafficAlerts   = ref([])
// quelle vue afficher
const currentView     = ref(null)

function handleConnexity(e) {
  currentView.value     = 'Connexity'
  loadingConnexity.value = true
  axios.get('http://127.0.0.1:8000/connexity/')
    .then(r => { connexe.value = r.data })
    .catch(() => { connexe.value = false })
    .finally(() => loadingConnexity.value = false)
}

function handleTraffic(e) {
  currentView.value     = 'Traffic'
  loadingTraffic.value  = true
  axios.get('https://api-ratp.pierre-grimaud.fr/v4/traffic')
    .then(r => { trafficAlerts.value = r.data.result.trafic || [] })
    .catch(() => { trafficAlerts.value = [] })
    .finally(() => loadingTraffic.value = false)
}

onMounted(() => {
  window.addEventListener('show-connexity', handleConnexity)
  window.addEventListener('show-traffic',   handleTraffic)
})
onUnmounted(() => {
  window.removeEventListener('show-connexity', handleConnexity)
  window.removeEventListener('show-traffic',   handleTraffic)
})

const isConnexityView = computed(() => currentView.value === 'Connexity')
const isTrafficView   = computed(() => currentView.value === 'Traffic')
</script>

<style scoped>
.info-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 0 8px 2px rgba(54,54,54,0.12);
  padding: 24px 18px;

  position: absolute;
  top: calc(40px + /* hauteur de ta sidebar */ 200px);  /* ajuste 200px selon la hauteur réelle de ta sidebar */
  right: 40px;
  z-index: 1000;
  min-width: 170px;
}

</style>

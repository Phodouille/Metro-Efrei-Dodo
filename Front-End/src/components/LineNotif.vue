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
const alertMessage = ref(null)
const visible      = ref(false)

// Remplacez par **votre** token PRIM obtenu après inscription
const PRIM_TOKEN = import.meta.env.VITE_PRIM_TOKEN

/**
 * @param {string} lineParam  doit valoir ex. 'ligne1', 'ligne3b', etc.
 */
async function fetchTraffic(lineParam) {
  console.log('fetchTraffic appelé avec', lineParam)
  loading.value = true
  alertMessage.value = null

  try {
    // exemple d'appel à l'endpoint officiel
    const url = 'https://prim.iledefrance-mobilites.fr/marketplace/general-message'
    const params = {
      LineRef: `STIF:Line::${mapLineCode(lineParam)}:`,
      InfoChannelRef: 'Perturbation'
    }
    const headers = {
      Accept: 'application/json',
      apikey: PRIM_TOKEN
    }

    console.log('→ GET', url, params)
    const res = await axios.get(url, { params, headers })
    console.log('Status:', res.status, 'Payload brut:', res.data)
    const sd = res.data.Siri.ServiceDelivery
    console.log('→ GeneralMessageDelivery:', sd.GeneralMessageDelivery)
    if (sd.GeneralMessageDelivery && sd.GeneralMessageDelivery.length) {
      console.log('→ InfoMessage:', sd.GeneralMessageDelivery[0].InfoMessage)
    }

    // on plonge dans la structure renvoyée par PRIM
    const messages = res.data
      .Siri
      .ServiceDelivery
      .GeneralMessageDelivery[0]
      .InfoMessage

    if (messages && messages.length) {
      // on prend le premier message comme alerte
      alertMessage.value = messages[0].MessageText
    } else {
      alertMessage.value = null
    }

  } catch (err) {
    console.error('Erreur API PRIM disruptions_bulk', err.response?.status, err.response?.data)
    alertMessage.value = `Erreur ${err.response?.status || ''}`
  } finally {
    loading.value = false
  }
}

/**
 * Transforme 'ligne1' → 'C01371', 'ligne2' → 'C01372', etc.
 * (à adapter à VOS codes exacts pour chaque ligne)
 */
function mapLineCode(lineParam) {
  const mapping = {
    ligne1:  'C01371',
    ligne2:  'C01372',
    ligne3:  'C01373',
    ligne3b: 'C01373B',
    ligne4:  'C01374',
    ligne5:  'C01375',
    ligne6:  'C01376',
    ligne7:  'C01377',
    ligne7b: 'C01377B',
    ligne8:  'C01378',
    ligne9:  'C01379',
    ligne10: 'C01380',
    ligne11: 'C01381',
    ligne12: 'C01382',
    ligne13: 'C01383',
    ligne14: 'C01384',
  }
  return mapping[lineParam] || ''
}

function handleShowLine(e) {
  const lineParam = e.detail
  console.log('handleShowLine reçu:', lineParam)
  if (!lineParam) return
  visible.value = true
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

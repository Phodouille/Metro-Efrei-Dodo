<template>
  <!-- InfoPanel n'existe que si Connexity ou News est actif -->
  <div
    v-if="isConnexityView || isNewsView"
    class="info-panel"
  >
    <!-- Connexity -->
    <div v-if="isConnexityView">
      <p v-if="loadingConnexity">Chargement de la connexité…</p>
      <p v-else-if="connexe">✅ Le réseau est <strong>connexe</strong>.</p>
      <p v-else>❌ Le réseau <strong>n'est pas</strong> connexe.</p>
    </div>

<!-- News -->
<div v-if="isNewsView">
  <p v-if="loadingNews">Chargement des dernières actualités…</p>
  <ul v-else>
    <li
      v-for="(actu, i) in newsItems"
      :key="actu.id || i"
      class="news-item"
    >
      <h4 v-html="actu.title"></h4>
      <p>{{ actu.description }}</p>
      <a :href="actu.link" target="_blank">
        {{ actu.buttontext || 'En savoir plus' }}
      </a>
    </li>
  </ul>
</div>


  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

// Connexity
const loadingConnexity = ref(false)
const connexe         = ref(false)

// News
const loadingNews = ref(false)
const newsItems   = ref([])

// Vue active
const currentView = ref(null)

function handleConnexity(e) {
  if (!e.detail) {
    if (currentView.value === 'Connexity') currentView.value = null
    return
  }
  currentView.value       = 'Connexity'
  loadingConnexity.value  = true
  axios.get('http://127.0.0.1:8000/connexity/')
    .then(r => { connexe.value = r.data })
    .catch(() => { connexe.value = false })
    .finally(() => { loadingConnexity.value = false })
}

function handleNews(e) {
  if (!e.detail) {
    if (currentView.value === 'News') currentView.value = null
    return
  }
  currentView.value = 'News'
  loadingNews.value = true
  axios.get('https://data.iledefrance-mobilites.fr/api/records/1.0/search/', {
    params: { dataset: 'actualites', rows: 5, sort: '-createddate' }
  })
    .then(res => { newsItems.value = res.data.records.map(rec => rec.fields) })
    .catch(() => { newsItems.value = [] })
    .finally(() => { loadingNews.value = false })
}

onMounted(() => {
  window.addEventListener('show-connexity', handleConnexity)
  window.addEventListener('show-news',       handleNews)
})

onUnmounted(() => {
  window.removeEventListener('show-connexity', handleConnexity)
  window.removeEventListener('show-news',       handleNews)
})

const isConnexityView = computed(() => currentView.value === 'Connexity')
const isNewsView      = computed(() => currentView.value === 'News')
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
  max-width: 350px;

  position: absolute;
  top: calc(140px + 200px);
  right: 40px;
  z-index: 1000;
  min-width: 170px;
}

.news-item h4 {
  margin: 0;
  font-size: 1.1em;
}
.news-item p {
  margin: 4px 0 8px;
  font-size: 0.9em;
}
.news-item a {
  font-size: 0.9em;
  color: #0074D9;
  text-decoration: none;
}
.news-item a:hover {
  text-decoration: underline;
}
</style>

import { defineStore } from 'pinia'
import {ref} from 'vue'

export const useNewStore = defineStore('newStore', () => {
  const sourceData = ref('')
  const destinationData = ref('')
  const pathDijkstraName = ref([])
  const pathDijkstraLine = ref([])
  const pathDijkstraDuration = ref(0)
  return { sourceData, destinationData, pathDijkstraName, pathDijkstraLine , pathDijkstraDuration}
})
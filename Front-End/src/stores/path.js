import { defineStore } from 'pinia'
import {ref} from 'vue'

export const useNewStore = defineStore('newStore', () => {
  const sourceData = ref('')
  const destinationData = ref('')
  return { sourceData, destinationData }
})
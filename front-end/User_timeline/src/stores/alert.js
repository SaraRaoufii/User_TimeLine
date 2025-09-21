import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

export const useAlertStore = defineStore('alert', () => {
  const message = ref('')
  const type = ref('info')   
  const visible = ref(false)

  const route = useRoute()
  watch(() => route.fullPath, () => {
    visible.value = false
  })

  function show(msg, t = 'info') {
    message.value = msg
    type.value = t
    visible.value = true

    setTimeout(() => {
      hide()
    }, 3000)
  }

  function hide() {
    visible.value = false
  }

  return { message, type, visible, show, hide }
})

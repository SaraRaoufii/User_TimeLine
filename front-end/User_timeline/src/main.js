import { createApp, h, provide } from 'vue'
import App from './App.vue'
import apolloClient from './apollo/client'
import router from './router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import './assets/tailwind.css'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { useUserStore } from './stores/user'


const vuetify = createVuetify({
  components,
  directives,
})

const pinia = createPinia()




const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
  },
  render: () => h(App),
})

app.use(pinia)
app.use(vuetify)
app.use(ElementPlus)
app.use(router)
app.mount('#app')

const userStore = useUserStore()
userStore.initUser()
console.log(userStore)


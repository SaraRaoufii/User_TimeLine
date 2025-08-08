import { createApp, h, provide } from 'vue'
import App from './App.vue'
import apolloClient from './apollo/client'
import router from './router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import * as lucide from 'lucide-vue-next'



const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
  },
  render: () => h(App),
})
app.use(router)
app.mount('#app')

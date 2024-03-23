import { createApp } from 'vue'
import router from '@/router/router'

import App from './App.vue'
import SearchRepos from './components/SearchRepos.vue'
import ReposCards from './components/ReposCards.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const vuetify = createVuetify({
    components,
    directives,
})
const app = createApp(App)

app.component('search-repos', SearchRepos)
app.component('repos-cards', ReposCards)

app.use(vuetify).use(router).mount('#app')

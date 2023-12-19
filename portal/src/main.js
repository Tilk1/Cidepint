import './assets/styles.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import vue3GoogleLogin from 'vue3-google-login'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(vue3GoogleLogin, {
    clientId: '1036650896074-fhkr6mj471n2q1p1q8j7jepn1re9lg6b.apps.googleusercontent.com'
  })


app.mount('#app')

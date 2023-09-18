// Svelte의 index.html 파일에서 참조하는 javaScripts 파일

import './app.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import App from './App.svelte'

const app = new App({
  target: document.getElementById('app'),
})

export default app

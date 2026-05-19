import '../scss/app.scss'
import { createApp } from 'vue'
import { pinia } from './stores/root.js'

// Registry: DOM id → lazy island loader
// Add new islands here — they are only loaded if their mount point exists in the page.
const islandRegistry = {
  'vue-theme-switcher': () => import('./islands/ThemeSwitcher.vue'),
  'vue-search-bar': () => import('./islands/SearchBar.vue'),
}

document.addEventListener('DOMContentLoaded', () => {
  Object.entries(islandRegistry).forEach(([id, loader]) => {
    const el = document.getElementById(id)
    if (!el) return

    // Props can be passed from Django templates via data-props="<json>"
    const props = el.dataset.props ? JSON.parse(el.dataset.props) : {}

    loader().then(({ default: component }) => {
      createApp(component, props).use(pinia).mount(el)
    })
  })
})

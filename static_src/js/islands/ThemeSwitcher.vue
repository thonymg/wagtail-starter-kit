<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUiStore } from '../stores/ui.js'

const ui = useUiStore()
const { theme } = storeToRefs(ui)

const options = [
  { value: 'auto', label: 'Auto' },
  { value: 'light', label: 'Light' },
  { value: 'dark', label: 'Dark' },
]

onMounted(() => ui.init())

function select(value) {
  ui.setTheme(value)
  // Close the Pico CSS dropdown by removing the open attribute
  document.querySelector('details.dropdown[open]')?.removeAttribute('open')
}
</script>

<template>
  <details class="dropdown">
    <summary role="button" class="contrast">Theme</summary>
    <ul>
      <li v-for="opt in options" :key="opt.value">
        <a href="#" @click.prevent="select(opt.value)">
          {{ opt.label }}
          <span v-if="theme === opt.value" aria-hidden="true"> ✓</span>
        </a>
      </li>
    </ul>
  </details>
</template>

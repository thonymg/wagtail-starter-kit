<script setup>
import { ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useSearchStore } from '../stores/search.js'

const props = defineProps({
  initialQuery: { type: String, default: '' },
})

const searchStore = useSearchStore()
const { results, loading, error, total, query } = storeToRefs(searchStore)

const input = ref(props.initialQuery)
let debounceTimer

watch(input, (val) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => searchStore.search(val), 300)
})

onMounted(() => {
  if (props.initialQuery) searchStore.search(props.initialQuery)
})
</script>

<template>
  <div class="vue-search-bar">
    <input
      v-model="input"
      type="search"
      placeholder="Search pages…"
      aria-label="Search"
      :aria-busy="loading"
    >

    <div
      v-if="loading"
      aria-busy="true"
      class="search-status"
    >
      Searching…
    </div>

    <p
      v-else-if="error"
      class="search-error"
    >
      <small>{{ error }}</small>
    </p>

    <template v-else-if="input && results.length === 0 && !loading">
      <p><small>No results for <strong>{{ query }}</strong></small></p>
    </template>

    <template v-else-if="results.length > 0">
      <p><small>{{ total }} result{{ total !== 1 ? 's' : '' }}</small></p>
      <ul class="search-results">
        <li
          v-for="result in results"
          :key="result.id"
        >
          <a :href="result.url">{{ result.title }}</a>
          <br v-if="result.description">
          <small v-if="result.description">{{ result.description }}</small>
        </li>
      </ul>
    </template>
  </div>
</template>

import { defineStore } from 'pinia'

export const useSearchStore = defineStore('search', {
  state: () => ({
    query: '',
    results: [],
    total: 0,
    loading: false,
    error: null,
  }),

  actions: {
    async search(query) {
      this.query = query

      if (!query.trim()) {
        this.results = []
        this.total = 0
        return
      }

      this.loading = true
      this.error = null

      try {
        const res = await fetch(`/api/search/?query=${encodeURIComponent(query)}`, {
          headers: { Accept: 'application/json' },
        })
        if (!res.ok) throw new Error(`Search error: ${res.status}`)
        const data = await res.json()
        this.results = data.results
        this.total = data.total
      } catch (e) {
        this.error = e.message
        this.results = []
        this.total = 0
      } finally {
        this.loading = false
      }
    },

    clear() {
      this.query = ''
      this.results = []
      this.total = 0
      this.error = null
    },
  },
})

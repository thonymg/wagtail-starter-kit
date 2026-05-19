import { defineStore } from 'pinia'

const STORAGE_KEY = 'picoPreferredColorScheme'

export const useUiStore = defineStore('ui', {
  state: () => ({
    // 'auto' | 'light' | 'dark' — persisted in localStorage
    theme: typeof localStorage !== 'undefined'
      ? (localStorage.getItem(STORAGE_KEY) ?? 'auto')
      : 'auto',
  }),

  actions: {
    setTheme(theme) {
      this.theme = theme

      const resolved = theme === 'auto'
        ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        : theme

      document.documentElement.setAttribute('data-theme', resolved)
      localStorage.setItem(STORAGE_KEY, theme)
    },

    init() {
      // Apply stored theme immediately on mount to avoid flash
      this.setTheme(this.theme)

      // React to OS-level changes when theme is set to 'auto'
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (this.theme === 'auto') this.setTheme('auto')
      })
    },
  },
})

import { createPinia } from 'pinia'

// Single Pinia instance shared across all islands.
// Each island does createApp(...).use(pinia) — they all share the same store state.
export const pinia = createPinia()

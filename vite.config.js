import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    tailwindcss(),
    vue(),
  ],

  // static_src is the frontend root — all JS/CSS paths are relative to it
  root: resolve(__dirname, 'static_src'),

  // Must match Django's STATIC_URL so asset URLs work in both dev and prod
  base: '/static/',

  build: {
    outDir: resolve(__dirname, 'static_compiled'),
    // Don't wipe the folder — images are built separately by scripts/images.cjs
    emptyOutDir: false,
    // Generates static_compiled/.vite/manifest.json — consumed by django-vite
    manifest: true,
    rollupOptions: {
      input: resolve(__dirname, 'static_src/js/main.js'),
    },
  },

  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    cors: true,
  },
})

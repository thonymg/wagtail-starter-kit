import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],

  // static_src is the frontend root — all JS/SCSS paths are relative to it
  root: resolve(__dirname, 'static_src'),

  // Must match Django's STATIC_URL so asset URLs work in both dev and prod
  base: '/static/',

  build: {
    outDir: resolve(__dirname, 'static_compiled'),
    // Don't wipe the folder — images are built separately by scripts/images.js
    emptyOutDir: false,
    // Generates static_compiled/.vite/manifest.json — consumed by django-vite
    manifest: true,
    rollupOptions: {
      input: resolve(__dirname, 'static_src/js/main.js'),
    },
  },

  css: {
    preprocessorOptions: {
      scss: {
        // Silence deprecation warnings from PicoCSS internals (not our code)
        silenceDeprecations: ['if-function'],
      },
    },
  },

  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    // Allow cross-origin requests from Django's dev server
    cors: true,
  },
})

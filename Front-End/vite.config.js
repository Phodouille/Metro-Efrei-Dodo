import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // Quand tu appelleras /api/prim/*, Vite redirigera vers prim.iledefrance-mobilites.fr/apis/*
      '^/api/prim/(.*)': {
        target: 'https://prim.iledefrance-mobilites.fr',
        changeOrigin: true,
        secure: true,
        rewrite: path => path.replace(/^\/api\/prim/, '/apis')
      }
    }
  }
})

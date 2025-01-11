import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server:{
    proxy:{
      '/api':{
        target:process.env.VITE_API_URL || 'http://127.0.0.1:5000',
        changeOrigin:true,
      },
    }
  },
  plugins: [react()],

})


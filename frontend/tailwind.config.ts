import type { Config } from 'tailwindcss'

// Tailwind configuration for the Elysia web interface
const config: Config = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx,css}'],
  theme: {
    extend: {}
  },
  plugins: []
}

export default config

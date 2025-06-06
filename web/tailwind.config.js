/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        sidebar: '#0C0C0E',
        'chat-start': '#0F1C29',
        'chat-end': '#050B14',
        'code-bg': '#0A0F18',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(circle at top center, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [
    require('tailwindcss/plugin')(function ({ addUtilities }) {
      addUtilities({
        '.bg-chat-gradient': {
          backgroundImage:
            'radial-gradient(circle at top center, #0F1C29, #050B14)',
        },
      })
    }),
  ],
}

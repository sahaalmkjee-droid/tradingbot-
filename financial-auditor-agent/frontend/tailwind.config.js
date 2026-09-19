/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        chalk: '#F8F9FA',
        emerald: {
          600: '#0D9488',
          700: '#0F766E',
        },
        amber: {
          600: '#D97706',
        },
        crimson: {
          600: '#DC2626',
        }
      }
    },
  },
  plugins: [],
}

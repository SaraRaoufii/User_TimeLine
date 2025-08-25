/** @type {import('tailwindcss').Config} */
export default {
  content: [
        "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        maincolor:'#1E3A8A',
        backgroundcolor: '#F5F7FA',
        lightblue: '#CADBEF',
        darkbrown: '#644C07',
        lightbrown: '#D3C394',
        graysecond: '#92929D',
        grayback: '#ECF0F1',
        lightgreen: '#AAE6AA',
        darkgreen: '#008a12',
        lightred: '#F68E8F',
        darkred: '#ee0202',
        inactive: '#FEFCF4',
      }
    },
  },
  plugins: [],
}


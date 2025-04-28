/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // src içindeki tüm component dosyalarında tarama yapar
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  theme: {
    extend: {
      fontFamily: {
        amatic: ['"Amatic SC"', 'cursive'],
      },
    },
  },
  plugins: [],
}

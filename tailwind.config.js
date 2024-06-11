/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./**/*.py"],
  theme: {
    extend: {},
    screens: {
      'lg': '1024px',
      'md': '768px',
      'sm': '640px'
    },
  },
  plugins: [],
  safelist: [],
};

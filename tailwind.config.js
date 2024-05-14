/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./**/*.py"],
  theme: {
    extend: {},
  },
  plugins: [],
  safelist: [
    "w-[180px]",
    "h-[180px]",
  ]
};

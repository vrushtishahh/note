/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
    screens: {
      'sm': '280px', 
      'md': '400px', 
      'lg': '700px',

    },
  },
  },
  plugins: [],
}


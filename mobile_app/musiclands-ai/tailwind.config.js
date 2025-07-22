/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        'festival-pink': '#FF6B9D',
        'festival-purple': '#C44EFD', 
        'festival-cyan': '#4ECFFD',
        'festival-green': '#44FFB3',
        'festival-red': '#FF1744',
      }
    },
  },
  plugins: [],
}


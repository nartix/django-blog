/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './components/**/*.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    fontFamily: {
      // Add the font name to the list of fonts
      sans: ['Poppins', 'system-ui', '-apple-system', 'BlinkMacSystemFont'],
      'font-mono': ['Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
    },
    extend: {},
  },
  plugins: [],
};

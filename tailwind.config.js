/** @type {import('tailwindcss').Config} */
module.exports = {
  // Les archives ne sont pas servies : les scanner ferait grossir la feuille de
  // classes que plus aucune page n'emploie.
  content: [
    "./index.html",
    "./404.html",
    "./fr/**/*.html",
    "./admin/**/*.html",
    "./assets/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        // Palette propre à NetSalaire : bleu pétrole. Elle remplace l'indigo par
        // défaut de Tailwind, que §10.1 compte comme un marqueur de site généré.
        brand: {
          50:  '#eef4f6',
          100: '#d6e5ea',
          200: '#b0ccd6',
          300: '#7fabba',
          400: '#4a8599',
          500: '#1f6a80',
          600: '#185563',
          700: '#134350',
          800: '#0e323c',
          900: '#0a242b',
        },
      },
    },
  },
  plugins: [],
}

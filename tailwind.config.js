/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/**/*.html'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#000000',
        'background-light': '#f6f6f8',
        'background-dark': '#101622',
      },
      fontFamily: {
        display: ['Manrope'],
      },
      borderRadius: {
        DEFAULT: '0.25rem',
        lg: '0.5rem',
        xl: '0.75rem',
        full: '9999px',
      },
    },
  },
  safelist: [
    // classes added dynamically via JS classList operations
    'bg-primary/5', 'bg-slate-100',
    'border', 'border-2', 'border-primary', 'border-transparent',
    'border-slate-200', 'cursor-not-allowed',
    'dark:bg-slate-800', 'dark:border-slate-700',
    'dark:text-slate-300', 'dark:text-slate-400',
    'font-bold', 'font-semibold',
    'hover:border-primary', 'hover:text-primary',
    'line-through', 'opacity-0', 'opacity-60',
    'shadow-sm', 'text-primary',
    'text-slate-400', 'text-slate-500', 'text-slate-700',
    // cancel booking button (generated inside JS renderCard)
    'bg-red-50', 'hover:bg-red-100', 'text-red-500',
    'dark:bg-red-900/10', 'dark:hover:bg-red-900/20',
  ],
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
};

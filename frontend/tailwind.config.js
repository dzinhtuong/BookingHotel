/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
    content: ['./src/**/*.{html,js}'],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Poppins', ...defaultTheme.fontFamily.sans],
            },
            colors: {
                primary: '#00aad3',
                secondary: 'ff567d',
            },
            keyframes: {
                slideIn: {
                    '0%': { transform: 'translateX(100%)' },
                    '100%': { transform: 'translateX(0)' },
                },
                slideOut: {
                    '100%': { transform: 'translateX(100%)' },
                    '0%': { transform: 'translateX(0)' },
                },
                fadeIn: {
                    '0%': { opacity: 0 },
                    '100%': { opacity: 1 },
                },
                growth: {
                    '0%': { transform: 'scale(0.7)' },
                    '100%': { transform: 'scale(1)' },
                },
                slideInFromTop: {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(0)' },
                },
            },
            animation: {
                'spin-slow': 'spin 3s linear infinite',
                'slide-in': 'slideIn .4s ease',
                'slide-out': 'slideOut .4s ease',
                'fade-in': 'fadeIn .4s ease',
                'growth-in': 'growth linear 0.1s',
                'slide-in-from-top': 'slideInFromTop .3s ease',
            },
            width: {
                1200: '1200px',
            },
            height: {
                header: '60px',
                'search-group': '520px'
            },
            boxShadow: {
                'custom-1': '2px 2px 4px rgba(0, 0, 0, 0.5)',
                
            },
        },
    },
    plugins: [],
};

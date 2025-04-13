module.exports = {
  // ...existing config...
  theme: {
    extend: {
      // ...existing theme extensions...
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'pulse': 'pulse 3s ease-in-out infinite',
        'grow-x': 'growX 0.5s ease-out forwards',
        'scale-in': 'scaleIn 0.4s ease-out forwards',
        'draw': 'draw 1.5s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0, transform: 'translateY(20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        pulse: {
          '0%, 100%': { opacity: 0.1, transform: 'scale(1)' },
          '50%': { opacity: 0.3, transform: 'scale(1.2)' },
        },
        growX: {
          '0%': { transform: 'scaleX(0)', transformOrigin: 'left' },
          '100%': { transform: 'scaleX(1)', transformOrigin: 'left' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0)' },
          '100%': { transform: 'scale(1)' },
        },
        draw: {
          '0%': { strokeDasharray: 1000, strokeDashoffset: 1000, opacity: 0 },
          '30%': { opacity: 1 },
          '100%': { strokeDasharray: 1000, strokeDashoffset: 0, opacity: 1 },
        },
      },
    },
  },
  // ...rest of config...
};

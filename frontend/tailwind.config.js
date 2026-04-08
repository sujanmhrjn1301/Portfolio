module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'caveat': ['Caveat', 'cursive'],
      },
      colors: {
        'dark-gray': '#1a1a1a',
        'medium-gray': '#2d2d30',
        'light-gray': '#3e3e42',
        'lighter-gray': '#ececf1',
      },
      typography: {
        DEFAULT: {
          css: {
            color: '#ececf1',
            a: {
              color: '#3b82f6',
              '&:hover': {
                color: '#1d4ed8',
              },
            },
          },
        },
      },
    },
  },
  plugins: [],
}

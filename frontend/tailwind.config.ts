import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          light: "#6FE7DD",
          DEFAULT: "#2BB7B3",
          dark: "#1F7A7A",
        },
        secondary: {
          DEFAULT: "#3D3D4E",
        },
        accent: {
          DEFAULT: "#F8B400",
        },
      },
    },
  },
  plugins: [],
};

export default config;

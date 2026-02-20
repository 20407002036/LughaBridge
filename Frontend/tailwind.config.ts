import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      // Universal spacing scale (LOCKED)
      spacing: {
        xs: '4px',      // Icon gaps, tight spacing
        sm: '8px',      // Element padding
        md: '16px',     // Standard gaps
        lg: '24px',     // Section spacing
        xl: '32px',     // Page margins
        '2xl': '48px',  // Hero spacing
        '3xl': '64px',  // Major sections
      },
      
      // Universal radius scale (LOCKED)
      borderRadius: {
        xs: '4px',      // Minimal
        sm: '8px',      // Chips, tags, small badges
        base: '12px',   // Standard
        md: '12px',     // Map md to base for compatibility
        lg: '16px',     // Modals, panels
        xl: '20px',     // Buttons, inputs (Rule Book)
        '2xl': '24px',  // Cards, Full-page containers
        '3xl': '32px',  // Large
      },
      
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      
      // Universal shadow depth (LOCKED)
      boxShadow: {
        'xs': '0 1px 2px rgba(0,0,0,0.04)',
        'sm': '0 1px 3px rgba(0,0,0,0.08)',
        'md': '0 4px 6px rgba(0,0,0,0.1)',
        'lg': '0 10px 15px rgba(0,0,0,0.1)',
        'xl': '0 20px 25px rgba(0,0,0,0.15)',
      },
      
      // Universal transition durations (LOCKED)
      transitionDuration: {
        fast: '150ms',  // Hover, focus states
        base: '250ms',  // Default interactions
        slow: '350ms',  // Page transitions
      },
      
      transitionTimingFunction: {
        spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)', // Playful animations
      },
      
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        gold: "hsl(var(--gold))",
        emerald: "hsl(var(--emerald))",
        "emerald-light": "hsl(var(--emerald-light))",
        obsidian: "hsl(var(--obsidian))",
        "obsidian-light": "hsl(var(--obsidian-light))",
        glass: "hsl(var(--glass))",
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pulse-glow": {
          "0%, 100%": { boxShadow: "0 4px 20px hsl(168 55% 45% / 0.25)" },
          "50%": { boxShadow: "0 4px 40px hsl(168 55% 45% / 0.4), 0 0 60px hsl(168 55% 45% / 0.15)" },
        },
        "mic-idle": {
          "0%, 100%": { boxShadow: "0 4px 20px hsl(230 65% 55% / 0.2)" },
          "50%": { boxShadow: "0 4px 30px hsl(230 65% 55% / 0.3)" },
        },
        "waveform": {
          "0%, 100%": { height: "4px" },
          "50%": { height: "16px" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(8px) scale(0.98)" },
          "100%": { opacity: "1", transform: "translateY(0) scale(1)" },
        },
        "ring-fill": {
          "0%": { strokeDashoffset: "100" },
          "100%": { strokeDashoffset: "var(--ring-offset)" },
        },
        "status-pulse": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        "wave-bars": {
          "0%": { transform: "scaleY(0.6)", opacity: "0.4" },
          "50%": { transform: "scaleY(1)", opacity: "1" },
          "100%": { transform: "scaleY(0.6)", opacity: "0.4" },
        },
        "wave-ring": {
          "0%": { boxShadow: "0 0 0 0 rgba(79, 106, 232, 0.15)" },
          "70%": { boxShadow: "0 0 0 12px rgba(79, 106, 232, 0)" },
          "100%": { boxShadow: "0 0 0 0 rgba(79, 106, 232, 0)" },
        },
        "ambient-float": {
          "0%": { transform: "translate3d(0,0,0) scale(1)", opacity: "0.25" },
          "50%": { transform: "translate3d(8px,-6px,0) scale(1.02)", opacity: "0.35" },
          "100%": { transform: "translate3d(0,0,0) scale(1)", opacity: "0.25" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in-up": "fade-in-up 0.25s ease-out forwards",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "mic-idle": "mic-idle 3s ease-in-out infinite",
        "slide-up": "slide-up 0.2s ease-out forwards",
        "status-pulse": "status-pulse 2s ease-in-out infinite",
        "wave-bars": "wave-bars 0.9s ease-in-out infinite",
        "wave-ring": "wave-ring 1.8s ease-out infinite",
        "ambient-float": "ambient-float 12s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;

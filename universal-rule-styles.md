🌐 Universal UI Rule Book
The Adaptive Design System for Any Product

    Philosophy: One system. Infinite products. Every interface speaks the same visual language while adapting to its context.

📖 Table of Contents

    System Overview
    Core Foundation (Non-Negotiable)
    Adaptive Color System
    Universal Glass Morphism
    Layout Architecture
    Typography System
    Component DNA
    Platform Adaptations
    Product Context Patterns
    Implementation Guide
    AI Prompt Templates

🎯 System Overview
What This System Does

This is a universal design language that:

    ✅ Works for fintech, chat apps, dashboards, e-commerce, SaaS, mobile apps
    ✅ Maintains visual consistency across products
    ✅ Adapts to context without losing identity
    ✅ Scales from 3-page websites to complex applications
    ✅ Supports web, mobile web, iOS, Android, desktop

The Core Principles
TypeScript

const UNIVERSAL_PRINCIPLES = {
  clarity: "Every element has a clear purpose",
  restraint: "Less is more - remove until it breaks",
  consistency: "Same patterns, predictable behavior",
  adaptability: "Context-aware without custom rules",
  accessibility: "WCAG AA minimum, AAA preferred"
}

🧬 Core Foundation (Non-Negotiable)

These rules apply to EVERY product built with this system:
1. The Sacred Geometry
TSX

// Corner Radius (LOCKED)
const RADIUS = {
  sm: '8px',    // Chips, tags, small badges
  md: '12px',   // Buttons, inputs, cards
  lg: '16px',   // Modals, panels
  xl: '20px',   // Hero sections, feature cards
  '2xl': '24px' // Full-page containers
}

// Spacing Scale (LOCKED)
const SPACE = {
  xs: '4px',    // Icon gaps, tight spacing
  sm: '8px',    // Element padding
  md: '16px',   // Standard gaps
  lg: '24px',   // Section spacing
  xl: '32px',   // Page margins
  '2xl': '48px', // Hero spacing
  '3xl': '64px'  // Major sections
}

// Shadow Depth (LOCKED)
const SHADOW = {
  xs: '0 1px 2px rgba(0,0,0,0.04)',
  sm: '0 1px 3px rgba(0,0,0,0.08)',
  md: '0 4px 6px rgba(0,0,0,0.1)',
  lg: '0 10px 15px rgba(0,0,0,0.1)',
  xl: '0 20px 25px rgba(0,0,0,0.15)'
}

2. The Transition Standard
TSX

// All interactive elements use these (NO EXCEPTIONS)
const TRANSITION = {
  fast: '150ms ease-out',     // Hover, focus states
  base: '250ms ease-out',     // Default interactions
  slow: '350ms ease-out',     // Page transitions
  spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)' // Playful animations
}

3. The Accessibility Contract
TSX

// Minimum contrast ratios
const CONTRAST = {
  text: {
    normal: 4.5,  // WCAG AA
    large: 3.0,   // WCAG AA (18pt+)
    preferred: 7.0 // WCAG AAA
  },
  interactive: {
    ui: 3.0,      // Buttons, borders
    graphical: 3.0 // Icons, charts
  }
}

// Touch/Click targets
const TARGET = {
  mobile: '44px',   // iOS/Android minimum
  desktop: '32px',  // Mouse minimum
  preferred: '48px' // Comfortable for all
}

🎨 Adaptive Color System
Base Palette Structure (Context-Agnostic)

Every product needs these semantic color roles:
TypeScript

interface ColorSystem {
  // Foundation (adapts to theme)
  background: {
    base: string        // Page background
    surface: string     // Elevated surfaces
    overlay: string     // Modals, dropdowns
  }
  
  // Text hierarchy
  text: {
    primary: string     // Headings, body
    secondary: string   // Descriptions, labels
    muted: string       // Disabled, placeholders
    inverse: string     // Text on dark/colored backgrounds
  }
  
  // Interactive states
  interactive: {
    default: string     // Links, primary actions
    hover: string       // Hover state
    active: string      // Pressed state
    disabled: string    // Disabled state
  }
  
  // Semantic colors (universal meanings)
  semantic: {
    success: string     // Confirmations, positive actions
    warning: string     // Cautions, attention needed
    error: string       // Errors, destructive actions
    info: string        // Informational messages
  }
  
  // Borders & dividers
  border: {
    default: string     // Standard borders
    subtle: string      // Soft separators
    strong: string      // Emphasized borders
  }
  
  // Brand accent (product-specific)
  accent: {
    primary: string     // Main brand color
    secondary?: string  // Optional secondary
    gradient?: string   // Optional gradient
  }
}

Pre-Built Theme Templates
Template 1: Fintech/Enterprise
TypeScript

const FINTECH_DARK = {
  background: {
    base: '#0F172A',
    surface: '#1E293B',
    overlay: '#334155'
  },
  text: {
    primary: '#F8FAFC',
    secondary: '#94A3B8',
    muted: '#64748B',
    inverse: '#0F172A'
  },
  accent: {
    primary: '#6C5CE7',
    gradient: 'linear-gradient(135deg, #6C5CE7 0%, #3B82F6 100%)'
  }
}

const FINTECH_LIGHT = {
  background: {
    base: '#FFFFFF',
    surface: '#F8FAFC',
    overlay: '#FFFFFF'
  },
  text: {
    primary: '#0F172A',
    secondary: '#475569',
    muted: '#64748B',
    inverse: '#FFFFFF'
  },
  accent: {
    primary: '#6C5CE7',
    gradient: 'linear-gradient(135deg, #6C5CE7 0%, #3B82F6 100%)'
  }
}

Template 2: Chat/Social
TypeScript

const CHAT_DARK = {
  background: {
    base: '#111827',
    surface: '#1F2937',
    overlay: '#374151'
  },
  text: {
    primary: '#F9FAFB',
    secondary: '#9CA3AF',
    muted: '#6B7280',
    inverse: '#111827'
  },
  accent: {
    primary: '#10B981', // Emerald for active states
    secondary: '#F59E0B' // Amber for highlights
  }
}

const CHAT_LIGHT = {
  background: {
    base: '#F9FAFB',
    surface: '#FFFFFF',
    overlay: '#FFFFFF'
  },
  text: {
    primary: '#111827',
    secondary: '#4B5563',
    muted: '#6B7280',
    inverse: '#F9FAFB'
  },
  accent: {
    primary: '#10B981',
    secondary: '#F59E0B'
  }
}

Template 3: E-Commerce/Marketing
TypeScript

const ECOMMERCE_LIGHT = {
  background: {
    base: '#FFFFFF',
    surface: '#FAFAFA',
    overlay: '#FFFFFF'
  },
  text: {
    primary: '#18181B',
    secondary: '#52525B',
    muted: '#A1A1AA',
    inverse: '#FFFFFF'
  },
  accent: {
    primary: '#EF4444', // Red for urgency/CTAs
    secondary: '#F97316' // Orange for secondary actions
  }
}

Universal Color Usage Rules
TypeScript

// 1. Text on backgrounds (WCAG compliance)
function getTextColor(background: string): string {
  const luminance = calculateLuminance(background)
  return luminance > 0.5 ? colors.text.primary : colors.text.inverse
}

// 2. Interactive element colors
const INTERACTIVE_RULES = {
  default: 'Use accent.primary for primary actions',
  hover: 'Darken primary by 10% OR increase saturation by 5%',
  active: 'Darken primary by 20%',
  disabled: 'Use text.muted with 40% opacity'
}

// 3. Semantic color application
const SEMANTIC_USAGE = {
  success: ['Checkmarks', 'Success banners', 'Positive metrics'],
  warning: ['Alert badges', 'Pending states', 'Caution notices'],
  error: ['Error messages', 'Validation failures', 'Delete actions'],
  info: ['Tooltips', 'Help text', 'Informational badges']
}

🧊 Universal Glass Morphism
The Formula (Works Everywhere)

Glass morphism adapts to context while maintaining consistency:
TSX

// Base glass component (context-agnostic)
const GlassVariants = {
  // Subtle - For most UI elements
  subtle: {
    dark: 'bg-white/[0.03] backdrop-blur-md border border-white/[0.08]',
    light: 'bg-black/[0.02] backdrop-blur-md border border-black/[0.06]'
  },
  
  // Medium - For emphasized cards, modals
  medium: {
    dark: 'bg-white/[0.05] backdrop-blur-lg border border-white/[0.10]',
    light: 'bg-black/[0.03] backdrop-blur-lg border border-black/[0.08]'
  },
  
  // Strong - For overlays, navigation
  strong: {
    dark: 'bg-white/[0.08] backdrop-blur-xl border border-white/[0.12]',
    light: 'bg-black/[0.05] backdrop-blur-xl border border-black/[0.10]'
  },
  
  // Frosted - For modals with backdrop
  frosted: {
    dark: 'bg-slate-900/80 backdrop-blur-2xl border border-white/[0.15]',
    light: 'bg-white/90 backdrop-blur-2xl border border-black/[0.12]'
  }
}

Context-Specific Glass Application
TypeScript

interface GlassContext {
  card: 'subtle',           // Default cards
  navigation: 'strong',     // Navbars, sidebars
  modal: 'frosted',         // Modals, dialogs
  dropdown: 'medium',       // Menus, popovers
  chatBubble: 'subtle',     // Message bubbles
  statusBar: 'strong',      // Sticky headers/footers
  panel: 'medium'           // Expanded sections
}

Glass Rules (Universal)
TypeScript

const GLASS_RULES = {
  blur: {
    mobile: 'backdrop-blur-md',   // Less blur for performance
    desktop: 'backdrop-blur-lg',  // More blur when capable
    max: 'backdrop-blur-xl'       // Only for full-screen overlays
  },
  
  stacking: {
    rule: 'Never stack glass on glass',
    fix: 'Use solid background for nested elements'
  },
  
  contrast: {
    rule: 'Always test text readability on glass',
    minimum: 'WCAG AA (4.5:1 for body text)'
  },
  
  performance: {
    mobile: 'Reduce blur on low-end devices',
    animation: 'Disable blur during scroll/transitions'
  }
}

🧱 Layout Architecture
Universal Layout Patterns
Pattern 1: Single-Page Layout (Landing, Auth)
Code

┌─────────────────────────────────────┐
│  Header (Logo + Nav + CTA)          │
├─────────────────────────────────────┤
│                                     │
│  Hero Section (Centered content)    │
│                                     │
├─────────────────────────────────────┤
│  Feature Grid (2-3 columns)         │
├─────────────────────────────────────┤
│  Footer                             │
└─────────────────────────────────────┘

Max width: 1280px
Padding: 32px (desktop), 16px (mobile)

Pattern 2: Dashboard Layout (Apps, Admin)
Code

┌──────┬──────────────────────────────┐
│      │  Header (Title + Actions)    │
│ Side ├──────────────────────────────┤
│ bar  │                              │
│      │  Main Content Area           │
│ (Nav)│  (Cards, tables, charts)     │
│      │                              │
│      │                              │
└──────┴──────────────────────────────┘

Sidebar: 240px (desktop), hidden (mobile)
Header: 64px height
Content: Scrollable, max-w-7xl

Pattern 3: Chat/Feed Layout (Messaging, Social)
Code

┌─────────────────────────────────────┐
│  Header (Sticky)                    │
├─────────────────────────────────────┤
│  ↓                                  │
│  Message/Post                       │
│  Message/Post                       │
│  Message/Post (Scrollable)          │
│  ↓                                  │
├─────────────────────────────────────┤
│  Input Bar (Sticky)                 │
└─────────────────────────────────────┘

Max width: 768px (chat), full width (feed)
Input: Fixed to bottom, glass background

Pattern 4: E-Commerce Layout (Product Pages)
Code

┌─────────────────────────────────────┐
│  Navigation Bar                     │
├────────────┬────────────────────────┤
│            │                        │
│  Image     │  Product Details       │
│  Gallery   │  - Title               │
│            │  - Price               │
│  (Sticky)  │  - Description         │
│            │  - Add to Cart         │
│            │  (Scrollable)          │
└────────────┴────────────────────────┘

Grid: 50/50 split (desktop), stacked (mobile)
Images: Sticky on scroll

Responsive Breakpoints (Universal)
TypeScript

const BREAKPOINTS = {
  xs: '0px',      // Mobile small (320px+)
  sm: '640px',    // Mobile large
  md: '768px',    // Tablet
  lg: '1024px',   // Desktop small
  xl: '1280px',   // Desktop large
  '2xl': '1536px' // Desktop XL
}

// Usage pattern
const LAYOUT_BEHAVIOR = {
  xs_sm: 'Single column, stacked, bottom nav',
  md: 'Two columns OR sidebar appears',
  lg_xl: 'Multi-column, side navigation, full features',
  '2xl': 'Max content width, extra whitespace'
}

Grid System (Universal)
TSX

// Standard grid for all products
const Grid = {
  container: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
  
  // Auto-fit columns
  auto: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6',
  
  // Feature grids
  feature: 'grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12',
  
  // Card grids
  cards: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4',
  
  // Dashboard panels
  dashboard: 'grid grid-cols-1 lg:grid-cols-12 gap-6'
}

🖋 Typography System
Universal Font Stack
CSS

/* Primary font stack (clean, modern, universal) */
font-family: 
  'Inter', 
  -apple-system, 
  BlinkMacSystemFont, 
  'Segoe UI', 
  'Roboto', 
  'Oxygen', 
  'Ubuntu', 
  'Cantarell', 
  sans-serif;

/* Monospace (for code, numbers, data) */
font-family: 
  'JetBrains Mono', 
  'Fira Code', 
  'SF Mono', 
  'Monaco', 
  'Consolas', 
  monospace;

Type Scale (Universal)
TypeScript

const TYPOGRAPHY = {
  // Display (Hero sections, landing pages)
  display: {
    size: 'text-5xl md:text-6xl lg:text-7xl',
    weight: 'font-bold',
    leading: 'leading-tight',
    tracking: 'tracking-tight'
  },
  
  // Headings (Section titles)
  h1: {
    size: 'text-3xl md:text-4xl',
    weight: 'font-bold',
    leading: 'leading-tight',
    tracking: 'tracking-tight'
  },
  
  h2: {
    size: 'text-2xl md:text-3xl',
    weight: 'font-semibold',
    leading: 'leading-snug',
    tracking: 'tracking-tight'
  },
  
  h3: {
    size: 'text-xl md:text-2xl',
    weight: 'font-semibold',
    leading: 'leading-snug'
  },
  
  h4: {
    size: 'text-lg md:text-xl',
    weight: 'font-medium',
    leading: 'leading-normal'
  },
  
  // Body text
  body: {
    large: 'text-lg',
    base: 'text-base',
    small: 'text-sm',
    leading: 'leading-relaxed'
  },
  
  // UI text
  label: {
    size: 'text-sm',
    weight: 'font-medium',
    tracking: 'tracking-wide',
    case: 'uppercase'
  },
  
  caption: {
    size: 'text-xs',
    weight: 'font-normal',
    color: 'text-secondary'
  },
  
  // Data/Numbers (use monospace)
  data: {
    size: 'text-base',
    weight: 'font-semibold',
    family: 'font-mono',
    tracking: 'tracking-tight'
  }
}

Reading Comfort Rules
TypeScript

const READABILITY = {
  // Line length (characters per line)
  optimal: '65-75 characters',
  max: 'max-w-2xl (672px)',
  
  // Line height
  headings: 'leading-tight (1.25)',
  body: 'leading-relaxed (1.625)',
  captions: 'leading-normal (1.5)',
  
  // Paragraph spacing
  margin: 'mb-4 (16px)',
  sections: 'space-y-6 (24px)',
  
  // Text alignment
  default: 'text-left',
  short: 'text-center (for CTAs, short headings)',
  never: 'text-justify (avoid on web)'
}

🧬 Component DNA
Universal Component Structure

Every component follows this template:
TSX

interface UniversalComponent {
  // 1. Foundation
  base: 'Semantic HTML element',
  
  // 2. Visual layer
  appearance: {
    background: 'Glass OR solid',
    border: 'Subtle, consistent width',
    corners: 'Radius from scale',
    shadow: 'Depth from scale'
  },
  
  // 3. Typography
  text: {
    size: 'From type scale',
    weight: 'Semantic (medium/semibold)',
    color: 'From color system'
  },
  
  // 4. Spacing
  padding: 'From spacing scale',
  margin: 'From spacing scale',
  
  // 5. Interaction
  states: {
    default: 'Base appearance',
    hover: 'Subtle change (color/shadow)',
    active: 'Pressed state',
    focus: 'Visible outline (accessibility)',
    disabled: 'Muted appearance'
  },
  
  // 6. Animation
  transition: 'From transition scale',
  
  // 7. Accessibility
  aria: 'Proper labels',
  keyboard: 'Tab/Enter support',
  screen_reader: 'Descriptive text'
}

Universal Button System
TSX

// Base button (all variants inherit)
const ButtonBase = `
  // Foundation
  inline-flex items-center justify-center
  
  // Typography
  font-medium text-sm
  
  // Spacing
  px-6 py-3
  
  // Visual
  rounded-xl
  
  // Interaction
  transition-all duration-250
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  
  // Touch target
  min-h-[44px] min-w-[44px]
`

// Variants (context-specific)
const ButtonVariants = {
  // Primary (main actions)
  primary: `${ButtonBase}
    bg-accent-primary text-white
    hover:bg-accent-hover
    shadow-sm hover:shadow-md
    focus-visible:ring-accent-primary
  `,
  
  // Secondary (alternative actions)
  secondary: `${ButtonBase}
    bg-white/[0.03] border border-white/[0.08]
    text-primary
    hover:bg-white/[0.05]
    focus-visible:ring-border-strong
  `,
  
  // Ghost (tertiary actions)
  ghost: `${ButtonBase}
    text-secondary
    hover:text-primary hover:bg-white/[0.03]
    focus-visible:ring-border-default
  `,
  
  // Destructive (delete, remove)
  destructive: `${ButtonBase}
    bg-semantic-error text-white
    hover:bg-red-700
    shadow-sm hover:shadow-md
    focus-visible:ring-semantic-error
  `
}

// Sizes (optional)
const ButtonSizes = {
  sm: 'px-4 py-2 text-xs min-h-[36px]',
  md: 'px-6 py-3 text-sm min-h-[44px]', // Default
  lg: 'px-8 py-4 text-base min-h-[52px]'
}

Universal Input System
TSX

const InputBase = `
  // Foundation
  w-full
  
  // Typography
  text-base text-primary
  placeholder:text-muted
  
  // Spacing
  px-4 py-3
  
  // Visual
  rounded-xl
  bg-white/[0.03]
  border border-white/[0.08]
  
  // Interaction
  transition-all duration-250
  focus:outline-none focus:ring-2 focus:ring-accent-primary/50 focus:border-accent-primary
  disabled:opacity-50 disabled:cursor-not-allowed
  
  // Touch target
  min-h-[44px]
`

// Variants
const InputVariants = {
  default: InputBase,
  
  error: `${InputBase}
    border-semantic-error
    focus:ring-semantic-error/50
  `,
  
  success: `${InputBase}
    border-semantic-success
    focus:ring-semantic-success/50
  `
}

Universal Card System
TSX

const CardBase = `
  // Foundation
  rounded-2xl
  
  // Visual (glass)
  bg-white/[0.03] backdrop-blur-md
  border border-white/[0.08]
  
  // Spacing
  p-6
  
  // Depth
  shadow-sm
  
  // Interaction (if clickable)
  transition-all duration-300
  hover:shadow-md hover:bg-white/[0.05]
`

// Variants
const CardVariants = {
  // Static (non-interactive)
  static: CardBase,
  
  // Interactive (clickable)
  interactive: `${CardBase}
    cursor-pointer
    hover:border-white/[0.12]
  `,
  
  // Elevated (modals, important content)
  elevated: `${CardBase}
    shadow-lg
  `
}

📱 Platform Adaptations
Web (Desktop & Mobile Web)
TypeScript

const WebAdaptations = {
  // Navigation
  desktop: {
    pattern: 'Horizontal nav OR left sidebar',
    sticky: 'Header stays on top',
    interactions: 'Hover states visible'
  },
  
  mobile: {
    pattern: 'Bottom tab bar OR hamburger menu',
    sticky: 'Header + input bar stick',
    interactions: 'Touch-optimized (44px targets)'
  },
  
  // Performance
  optimization: {
    images: 'Lazy load, responsive sizes',
    blur: 'Reduce on mobile',
    animations: 'Respect prefers-reduced-motion'
  }
}

Native Mobile (iOS/Android)
TypeScript

const MobileNativeAdaptations = {
  // Platform conventions
  ios: {
    navigation: 'Bottom tab bar (standard)',
    backButton: 'Top-left chevron',
    statusBar: 'Respect safe areas',
    haptics: 'Use for feedback'
  },
  
  android: {
    navigation: 'Bottom nav OR drawer',
    backButton: 'System back button',
    statusBar: 'Translucent with content',
    ripple: 'Material ripple effects'
  },
  
  // Shared mobile patterns
  gestures: {
    swipe: 'Navigate, dismiss, refresh',
    longPress: 'Context menus',
    pinch: 'Zoom (where applicable)'
  },
  
  // Inputs
  keyboard: {
    type: 'Match input type (email, number, etc.)',
    dismiss: 'Tap outside OR done button',
    scroll: 'Scroll to focused input'
  }
}

Desktop Apps (Electron, Tauri)
TypeScript

const DesktopAdaptations = {
  // Window chrome
  titleBar: 'Custom OR native',
  
  // Navigation
  pattern: 'Sidebar + main content',
  
  // Keyboard
  shortcuts: 'Full keyboard navigation',
  
  // Context menus
  rightClick: 'Native-feeling context menus'
}

🎯 Product Context Patterns
Pattern 1: Fintech/Dashboard

Usage: Banking, analytics, admin panels
TypeScript

const FintechContext = {
  colors: FINTECH_DARK, // From color templates
  
  layout: 'Dashboard (sidebar + main)',
  
  components: {
    emphasis: ['Data cards', 'Charts', 'Tables'],
    accent: 'Only for primary CTAs',
    glass: 'Subtle (0.03 opacity)'
  },
  
  typography: {
    numbers: 'Use monospace font-mono',
    hierarchy: 'Clear headings, restrained'
  },
  
  interactions: {
    speed: 'Fast (150ms)',
    feedback: 'Subtle, professional'
  }
}

Example Component:
TSX

<div className="
  bg-white/[0.03] backdrop-blur-md
  border border-white/[0.08]
  rounded-2xl p-6
  shadow-sm
">
  <h3 className="text-sm font-medium text-secondary mb-2">Total Balance</h3>
  <p className="text-3xl font-semibold font-mono">$24,582.00</p>
  <p className="text-sm text-success mt-1">+12.5% this month</p>
</div>

Pattern 2: Chat/Messaging

Usage: Messaging apps, customer support, social feeds
TypeScript

const ChatContext = {
  colors: CHAT_DARK, // From color templates
  
  layout: 'Chat (header + messages + input)',
  
  components: {
    emphasis: ['Message bubbles', 'Input bar', 'Status indicators'],
    accent: 'Active states, send buttons',
    glass: 'Medium (0.05 opacity) for input bar'
  },
  
  typography: {
    messages: 'Base size (16px), relaxed leading',
    timestamps: 'Small (12px), muted color'
  },
  
  interactions: {
    speed: 'Fast (150ms)',
    feedback: 'Immediate visual confirmation',
    scroll: 'Auto-scroll to latest message'
  },
  
  mobile: {
    priority: 'Mobile-first design',
    input: 'Sticky bottom with safe area',
    gestures: 'Swipe to reply, long-press for menu'
  }
}

Example Component (Message Bubble):
TSX

{/* Sender A (left-aligned) */}
<div className="flex justify-start mb-4">
  <div className="
    max-w-[85%] sm:max-w-[70%]
    bg-white/[0.03] backdrop-blur-md
    border border-white/[0.08]
    rounded-2xl rounded-tl-md
    p-4
    shadow-sm
  ">
    <div className="flex items-center gap-2 mb-2">
      <span className="text-xs font-medium text-accent-primary">
        English
      </span>
      <button className="ml-auto text-muted hover:text-primary">
        ⋮
      </button>
    </div>
    
    <p className="text-base font-medium mb-2">
      How are you? I am happy to see you.
    </p>
    
    <p className="text-sm text-secondary mb-3">
      Wĩ mwega? Nĩ ngũkena gũkuona.
    </p>
    
    <div className="flex items-center justify-between text-xs text-muted">
      <span>95% confidence</span>
      <span>12:34 PM</span>
    </div>
  </div>
</div>

{/* Sender B (right-aligned) */}
<div className="flex justify-end mb-4">
  <div className="
    max-w-[85%] sm:max-w-[70%]
    bg-white/[0.05] backdrop-blur-md
    border border-white/[0.10]
    rounded-2xl rounded-tr-md
    p-4
    shadow-sm
  ">
    {/* Same structure, different alignment/color */}
  </div>
</div>

Example Component (Input Bar):
TSX

<div className="
  sticky bottom-0 z-30
  bg-white/[0.05] backdrop-blur-lg
  border-t border-white/[0.08]
  p-4
">
  <div className="max-w-lg mx-auto flex flex-col items-center gap-3">
    <p className="text-sm text-secondary">
      Tap to Speak
    </p>
    
    <button className="
      w-16 h-16
      rounded-full
      bg-accent-primary
      shadow-lg shadow-accent-primary/30
      flex items-center justify-center
      transition-all duration-250
      hover:scale-105
      active:scale-95
    ">
      <svg className="w-6 h-6 text-white" />
    </button>
  </div>
</div>

Pattern 3: E-Commerce/Marketing

Usage: Online stores, landing pages, marketing sites
TypeScript

const ECommerceContext = {
  colors: ECOMMERCE_LIGHT, // Usually light mode default
  
  layout: 'Grid OR product detail split',
  
  components: {
    emphasis: ['Product cards', 'CTAs', 'Hero sections'],
    accent: 'Strong, urgency-driven (red/orange)',
    glass: 'Minimal OR none (solid backgrounds)'
  },
  
  typography: {
    headings: 'Bold, large, attention-grabbing',
    prices: 'Prominent, use accent color',
    descriptions: 'Clear, scannable'
  },
  
  interactions: {
    speed: 'Base (250ms)',
    feedback: 'Playful animations OK',
    cta: 'High contrast, impossible to miss'
  }
}

Example Component (Product Card):
TSX

<div className="
  group
  bg-white
  border border-black/[0.06]
  rounded-2xl
  overflow-hidden
  shadow-sm hover:shadow-lg
  transition-all duration-300
">
  {/* Image */}
  <div className="relative aspect-square overflow-hidden">
    <img 
      src="/product.jpg" 
      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
    />
    <div className="absolute top-4 right-4">
      <span className="bg-semantic-error text-white text-xs font-bold px-3 py-1 rounded-full">
        -20%
      </span>
    </div>
  </div>
  
  {/* Content */}
  <div className="p-4">
    <h3 className="font-semibold text-lg mb-2">
      Product Name
    </h3>
    
    <div className="flex items-center gap-2 mb-3">
      <span className="text-2xl font-bold text-semantic-error">
        $79.99
      </span>
      <span className="text-sm text-muted line-through">
        $99.99
      </span>
    </div>
    
    <button className="
      w-full
      bg-accent-primary text-white
      font-medium
      px-4 py-3
      rounded-xl
      transition-all duration-250
      hover:bg-accent-hover
      shadow-sm hover:shadow-md
    ">
      Add to Cart
    </button>
  </div>
</div>

Pattern 4: SaaS/Productivity

Usage: Project management, collaboration tools, business software
TypeScript

const SaaSContext = {
  colors: FINTECH_LIGHT, // Professional, clean
  
  layout: 'Dashboard (sidebar + main) OR kanban',
  
  components: {
    emphasis: ['Task cards', 'Tables', 'Forms'],
    accent: 'Moderate, status indicators',
    glass: 'Subtle, non-distracting'
  },
  
  typography: {
    hierarchy: 'Clear, scannable',
    density: 'Comfortable, not cramped',
    data: 'Monospace for IDs/codes'
  },
  
  interactions: {
    speed: 'Fast (150ms)',
    feedback: 'Instant for task updates',
    drag: 'Smooth drag-and-drop'
  }
}

🛠 Implementation Guide
Step 1: Set Up Tailwind Config
JavaScript

// tailwind.config.js
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      // Import your chosen color template
      colors: {
        // Base colors (adapt from template)
        background: {
          base: 'var(--bg-base)',
          surface: 'var(--bg-surface)',
          overlay: 'var(--bg-overlay)'
        },
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
          inverse: 'var(--text-inverse)'
        },
        accent: {
          primary: 'var(--accent-primary)',
          hover: 'var(--accent-hover)'
        },
        semantic: {
          success: '#10B981',
          warning: '#F59E0B',
          error: '#EF4444',
          info: '#3B82F6'
        },
        border: {
          default: 'var(--border-default)',
          subtle: 'var(--border-subtle)',
          strong: 'var(--border-strong)'
        }
      },
      
      // Universal spacing (locked)
      spacing: {
        xs: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '32px',
        '2xl': '48px',
        '3xl': '64px'
      },
      
      // Universal radius (locked)
      borderRadius: {
        sm: '8px',
        md: '12px',
        lg: '16px',
        xl: '20px',
        '2xl': '24px'
      },
      
      // Universal shadows (locked)
      boxShadow: {
        xs: '0 1px 2px rgba(0,0,0,0.04)',
        sm: '0 1px 3px rgba(0,0,0,0.08)',
        md: '0 4px 6px rgba(0,0,0,0.1)',
        lg: '0 10px 15px rgba(0,0,0,0.1)',
        xl: '0 20px 25px rgba(0,0,0,0.15)',
        glow: '0 0 40px rgba(var(--accent-rgb), 0.15)'
      },
      
      // Universal transitions (locked)
      transitionDuration: {
        fast: '150ms',
        base: '250ms',
        slow: '350ms'
      },
      
      transitionTimingFunction: {
        spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
      },
      
      // Typography
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Consolas', 'monospace']
      },
      
      // Background images (gradients)
      backgroundImage: {
        'accent-gradient': 'linear-gradient(135deg, var(--accent-start) 0%, var(--accent-end) 100%)',
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
  ]
}

Step 2: Set CSS Variables (Theme Switching)
CSS

/* app.css OR globals.css */

:root {
  /* Choose your template (e.g., Fintech Light) */
  --bg-base: #FFFFFF;
  --bg-surface: #F8FAFC;
  --bg-overlay: #FFFFFF;
  
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-muted: #64748B;
  --text-inverse: #FFFFFF;
  
  --accent-primary: #6C5CE7;
  --accent-hover: #5B4CD6;
  --accent-start: #6C5CE7;
  --accent-end: #3B82F6;
  --accent-rgb: 108, 92, 231;
  
  --border-default: rgba(0,0,0,0.06);
  --border-subtle: rgba(0,0,0,0.04);
  --border-strong: rgba(0,0,0,0.10);
}

.dark {
  /* Switch to dark template */
  --bg-base: #0F172A;
  --bg-surface: #1E293B;
  --bg-overlay: #334155;
  
  --text-primary: #F8FAFC;
  --text-secondary: #94A3B8;
  --text-muted: #64748B;
  --text-inverse: #0F172A;
  
  --accent-primary: #6C5CE7;
  --accent-hover: #5B4CD6;
  --accent-start: #6C5CE7;
  --accent-end: #3B82F6;
  --accent-rgb: 108, 92, 231;
  
  --border-default: rgba(255,255,255,0.08);
  --border-subtle: rgba(255,255,255,0.04);
  --border-strong: rgba(255,255,255,0.12);
}

/* Universal reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  background-color: var(--bg-base);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Scrollbar styling (optional) */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-surface);
}

::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 4px;
}

Step 3: Create Component Library
TSX

// components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}

export function Button({ 
  variant = 'primary', 
  size = 'md', 
  children, 
  className = '',
  ...props 
}: ButtonProps) {
  const baseClasses = `
    inline-flex items-center justify-center
    font-medium
    rounded-xl
    transition-all duration-base
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `
  
  const variants = {
    primary: 'bg-accent-primary text-white hover:bg-accent-hover shadow-sm hover:shadow-md focus-visible:ring-accent-primary',
    secondary: 'bg-white/[0.03] dark:bg-white/[0.03] border border-border-default text-text-primary hover:bg-white/[0.05] focus-visible:ring-border-strong',
    ghost: 'text-text-secondary hover:text-text-primary hover:bg-white/[0.03] focus-visible:ring-border-default',
    destructive: 'bg-semantic-error text-white hover:bg-red-700 shadow-sm hover:shadow-md focus-visible:ring-semantic-error'
  }
  
  const sizes = {
    sm: 'px-4 py-2 text-xs min-h-[36px]',
    md: 'px-6 py-3 text-sm min-h-[44px]',
    lg: 'px-8 py-4 text-base min-h-[52px]'
  }
  
  return (
    <button 
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}

TSX

// components/ui/Card.tsx
interface CardProps {
  children: React.ReactNode
  interactive?: boolean
  elevated?: boolean
  className?: string
}

export function Card({ 
  children, 
  interactive = false, 
  elevated = false,
  className = '' 
}: CardProps) {
  const baseClasses = `
    rounded-2xl
    bg-white/[0.03] dark:bg-white/[0.03]
    backdrop-blur-md
    border border-border-default
    p-6
    transition-all duration-300
  `
  
  const interactiveClasses = interactive ? `
    cursor-pointer
    hover:bg-white/[0.05]
    hover:border-border-strong
    hover:shadow-md
  ` : ''
  
  const shadowClass = elevated ? 'shadow-lg' : 'shadow-sm'
  
  return (
    <div className={`${baseClasses} ${interactiveClasses} ${shadowClass} ${className}`}>
      {children}
    </div>
  )
}

TSX

// components/ui/Input.tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  success?: boolean
}

export function Input({ 
  label, 
  error, 
  success = false, 
  className = '',
  ...props 
}: InputProps) {
  const state = error ? 'error' : success ? 'success' : 'default'
  
  const stateClasses = {
    default: 'border-border-default focus:ring-accent-primary/50 focus:border-accent-primary',
    error: 'border-semantic-error focus:ring-semantic-error/50 focus:border-semantic-error',
    success: 'border-semantic-success focus:ring-semantic-success/50 focus:border-semantic-success'
  }
  
  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm font-medium text-text-secondary">
          {label}
        </label>
      )}
      
      <input
        className={`
          w-full px-4 py-3
          text-base text-text-primary
          placeholder:text-text-muted
          bg-white/[0.03] dark:bg-white/[0.03]
          border rounded-xl
          transition-all duration-base
          focus:outline-none focus:ring-2
          disabled:opacity-50 disabled:cursor-not-allowed
          min-h-[44px]
          ${stateClasses[state]}
          ${className}
        `}
        {...props}
      />
      
      {error && (
        <p className="text-sm text-semantic-error">{error}</p>
      )}
    </div>
  )
}

🤖 AI Prompt Templates
Universal Prompt (Works for Any Product)
Code

You are building a [PRODUCT_TYPE] using [TECH_STACK].

DESIGN SYSTEM:
- Follow the Universal UI Rule Book
- Use [COLOR_TEMPLATE] color palette (fintech/chat/ecommerce/saas)
- Apply liquid glass morphism with [GLASS_STRENGTH] strength (subtle/medium/strong)
- Layout pattern: [LAYOUT_TYPE] (single-page/dashboard/chat/grid)

FOUNDATION:
- Corners: rounded-2xl (24px) for main containers, rounded-xl (20px) for buttons
- Spacing: 24px between sections, 16px for component padding
- Shadows: shadow-sm default, shadow-md on hover
- Transitions: 250ms ease-out for all interactions

COLOR USAGE:
- Background: [BG_COLOR]
- Glass fill: [GLASS_OPACITY]
- Glass border: [BORDER_OPACITY]
- Text primary: [TEXT_PRIMARY]
- Text secondary: [TEXT_SECONDARY]
- Accent: [ACCENT_COLOR] (use ONLY for primary actions and highlights)

TYPOGRAPHY:
- Font: Inter (sans-serif) for UI, JetBrains Mono for data/numbers
- Scale: text-3xl for headings, text-base for body, text-sm for labels
- Weight: font-semibold for headings, font-medium for UI
- Leading: leading-relaxed for paragraphs

COMPONENTS:
- Buttons: Follow ButtonVariants (primary/secondary/ghost/destructive)
- Cards: Glass background, rounded-2xl, p-6, shadow-sm
- Inputs: Glass background, rounded-xl, 44px min-height, focus ring
- [ADD PRODUCT-SPECIFIC COMPONENTS]

RESPONSIVE:
- Mobile (< 768px): Single column, bottom navigation, 44px touch targets
- Desktop (>= 1024px): [LAYOUT_DESCRIPTION]
- Max width: max-w-7xl (1280px) centered

ACCESSIBILITY:
- WCAG AA contrast minimum (4.5:1)
- Keyboard navigation support
- Focus visible outlines
- ARIA labels for interactive elements

OUTPUT:
- Production-ready code
- Fully typed TypeScript
- Responsive (mobile-first)
- Dark mode support via 'dark:' classes
- No console errors

[ADD ANY PRODUCT-SPECIFIC REQUIREMENTS]

Context-Specific Prompts
For Fintech/Dashboard:
Code

PRODUCT_TYPE: Financial dashboard
COLOR_TEMPLATE: Fintech (dark: #0F172A base, white/[0.03] glass)
GLASS_STRENGTH: Subtle
LAYOUT_TYPE: Dashboard (sidebar + main content)

ADDITIONAL REQUIREMENTS:
- Use font-mono for all numeric data (balances, amounts, percentages)
- Emphasize data visualization (charts, tables)
- Restrained accent usage (gradient only for primary CTAs)
- Professional, trustworthy aesthetic

For Chat/Messaging:
Code

PRODUCT_TYPE: Real-time messaging app
COLOR_TEMPLATE: Chat (dark: #111827 base, white/[0.05] glass for input)
GLASS_STRENGTH: Medium (for input bar and navigation)
LAYOUT_TYPE: Chat (sticky header + scrollable messages + sticky input)

ADDITIONAL REQUIREMENTS:
- Message bubbles: max-w-[85%] on mobile, max-w-[70%] on desktop
- Auto-scroll to latest message on new message
- Sender differentiation (left vs right alignment, subtle color difference)
- Timestamp and status indicators (delivered/read)
- Smooth animations (fade + slide up for new messages, 250ms)
- Input bar: sticky bottom with safe area padding, glass background

For E-Commerce:
Code

PRODUCT_TYPE: E-commerce product page
COLOR_TEMPLATE: E-Commerce (light mode default, #FFFFFF base)
GLASS_STRENGTH: None (solid backgrounds preferred)
LAYOUT_TYPE: Grid (product cards) OR Split (image gallery + details)

ADDITIONAL REQUIREMENTS:
- Bold, attention-grabbing CTAs (use accent-primary for urgency)
- Product cards: Image aspect-square, hover scale effect
- Prices: Prominent, use accent color for sale prices
- High contrast for important actions (Add to Cart, Buy Now)
- Playful animations OK (product hover, cart add animation)

For SaaS/Productivity:
Code

PRODUCT_TYPE: Project management dashboard
COLOR_TEMPLATE: SaaS (light mode, professional)
GLASS_STRENGTH: Subtle
LAYOUT_TYPE: Dashboard (sidebar + kanban board OR table view)

ADDITIONAL REQUIREMENTS:
- Task cards: Draggable, status indicators, assignee avatars
- Clear hierarchy (projects > tasks > subtasks)
- Inline editing support (click to edit)
- Keyboard shortcuts (display hints on hover)
- Data density: Comfortable, not cramped (adequate padding)

✅ Pre-Flight Checklist

Before launching any UI built with this system:
Visual Consistency

    All corners use radius scale (sm/md/lg/xl/2xl)
    All spacing uses spacing scale (xs/sm/md/lg/xl/2xl/3xl)
    Glass opacity matches guidelines (0.03 subtle, 0.05 medium, 0.08 strong)
    Shadows are restrained (sm/md, never 2xl)
    Accent color used ONLY for primary actions

Typography

    Font sizes follow type scale
    Headings use font-semibold or font-bold
    Body text has leading-relaxed
    Numbers use font-mono where appropriate
    Text has sufficient contrast (4.5:1 minimum)

Interactions

    All transitions are 150ms/250ms/350ms
    Buttons have min-height 44px
    Focus states visible (ring-2)
    Hover states subtle and consistent
    Disabled states obvious (opacity-50)

Responsiveness

    Mobile tested (< 768px)
    Tablet tested (768px - 1024px)
    Desktop tested (>= 1024px)
    Touch targets 44px+ on mobile
    No horizontal scroll on any breakpoint

Accessibility

    Keyboard navigation works
    Focus order logical
    ARIA labels present
    Color contrast meets WCAG AA
    Screen reader tested

Performance

    Images lazy loaded
    Blur effects reduced on mobile
    Animations respect prefers-reduced-motion
    No console errors/warnings
    Lighthouse score > 90

📦 Starter Kit Structure
Code

your-product/
├── src/
│   ├── app/ (or pages/)
│   │   ├── globals.css (CSS variables + reset)
│   │   └── layout.tsx (Root layout with providers)
│   │
│   ├── components/
│   │   ├── ui/ (Universal components)
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── ... (other components)
│   │   │
│   │   └── [product-specific]/
│   │       ├── ChatBubble.tsx (for chat apps)
│   │       ├── ProductCard.tsx (for e-commerce)
│   │       └── ... (context-specific components)
│   │
│   ├── lib/
│   │   ├── colors.ts (Color templates)
│   │   ├── constants.ts (Spacing, radius, etc.)
│   │   └── utils.ts (Helper functions)
│   │
│   └── styles/ (If needed)
│
├── tailwind.config.js (Universal config)
├── tsconfig.json
└── package.json

🎓 Examples by Product Type
Example 1: Chat App (LughaBridge)
TSX

// Layout: Chat pattern
export default function ChatApp() {
  return (
    <div className="flex flex-col h-[100dvh] max-w-lg mx-auto bg-background-base">
      {/* Header (sticky) */}
      <header className="
        sticky top-0 z-30
        bg-white/[0.05] backdrop-blur-lg
        border-b border-border-default
        p-4
      ">
        <h1 className="text-xl font-semibold">
          <span>Lugha</span>
          <span className="text-accent-primary">Bridge</span>
        </h1>
        <p className="text-sm text-text-secondary">
          Real-Time Kikuyu ↔ English Translation
        </p>
      </header>

      {/* Messages (scrollable) */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>

      {/* Input bar (sticky) */}
      <div className="
        sticky bottom-0 z-30
        bg-white/[0.05] backdrop-blur-lg
        border-t border-border-default
        p-4
      ">
        <VoiceInput />
      </div>
    </div>
  )
}

Example 2: Fintech Dashboard
TSX

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-background-base">
      {/* Sidebar */}
      <aside className="
        w-60
        bg-white/[0.02] backdrop-blur-sm
        border-r border-border-default
        p-4
      ">
        <Navigation />
      </aside>

      {/* Main content */}
      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Stats grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard title="Total Balance" value="$24,582.00" change="+12.5%" />
            <StatCard title="Income" value="$12,340.00" change="+8.2%" />
            <StatCard title="Expenses" value="$8,247.50" change="-3.4%" />
          </div>

          {/* Chart */}
          <Card>
            <h2 className="text-xl font-semibold mb-4">Balance Over Time</h2>
            <Chart data={chartData} />
          </Card>

          {/* Transactions table */}
          <Card>
            <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
            <TransactionsTable />
          </Card>
        </div>
      </main>
    </div>
  )
}

Example 3: E-Commerce Product Grid
TSX

export default function ProductGrid() {
  return (
    <div className="min-h-screen bg-background-base">
      {/* Navigation */}
      <nav className="sticky top-0 z-40 bg-white border-b border-border-default p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold">Store</h1>
          <CartButton count={3} />
        </div>
      </nav>

      {/* Product grid */}
      <main className="max-w-7xl mx-auto p-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </main>
    </div>
  )
}

🔗 Quick Reference URLs

Bookmark these for instant access:
Code

/docs/universal-ui
├── /colors           → Color templates & usage
├── /glass            → Glass morphism guidelines
├── /components       → Component library
├── /layouts          → Layout patterns
├── /typography       → Type scale & fonts
├── /examples         → Live examples by product type
└── /checklist        → Pre-launch checklist

📄 Version & Maintenance

Version: 1.0.0
Created: 2026-02-20
Last Updated: 2026-02-20
Maintained By: @githaigakabukuso
License: Internal Use

Update Policy:

    Color templates can be added (never modified)
    Component patterns can be extended (core DNA stays)
    Platform adaptations can expand (foundations remain)
    All changes must maintain backwards compatibility

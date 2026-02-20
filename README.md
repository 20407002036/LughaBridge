# LughaBridge

Real-time voice translation between Kikuyu and English.

## Getting Started

### Prerequisites

You'll need Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

### Setup

```sh
# Step 1: Clone the repository
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory
cd lugha-bridge/lughabridge-connect

# Step 3: Install dependencies
npm install

# Step 4: Start the development server
npm run dev
```

The app will be available at `http://localhost:8080`

## Technologies

This project is built with:

- **Vite** - Fast build tool and dev server
- **TypeScript** - Type-safe JavaScript
- **React 18** - UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **shadcn-ui** - Component library

## Project Structure

```
src/
├── components/           # React components
│   └── lugha/           # LughaBridge-specific components
├── data/                # Mock data and types
├── pages/               # Page components
├── styles/              # Global styles
└── main.tsx             # Entry point
```

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Features

- Real-time Kikuyu ↔ English voice translation
- Glass morphism UI design
- Mobile-optimized interface
- Audio waveform visualization
- Message history with confidence indicators
- Demo mode for testing

# LughaBridge

A real-time translation and communication platform with separate backend and frontend applications.

## Project Structure

This is a monorepo containing:
- **Backend/** - Django backend with translation services, WebSocket support, and API
- **Frontend/** - React/TypeScript frontend with Vite, Tailwind CSS, and shadcn-ui

## Getting Started

### Frontend Development

The frontend is built with React, TypeScript, Vite, and Tailwind CSS.

```sh
# Step 1: Clone the repository
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the frontend directory
cd LughaBridge/Frontend

# Step 3: Install dependencies
npm install

# Step 4: Start the development server
npm run dev
```

The frontend dev server will run on `http://localhost:8080`

### Backend Development

The backend is a Django application with translation services.

```sh
# Step 1: Navigate to the backend directory
cd Backend

# Step 2: Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run migrations
python manage.py migrate

# Step 5: Start the development server
python manage.py runserver
```

## Technologies

### Frontend
- React with TypeScript
- Vite (build tool)
- Tailwind CSS
- shadcn-ui components
- npm (package manager)

### Backend
- Django
- Django Channels (WebSocket support)
- Translation services (NLLB, Groq, HuggingFace)
- Redis (caching and task queue)
- Q Cluster (async task processing)

## Development Notes

- Frontend runs on port 8080 (Vite dev server)
- Backend runs on port 8000 (Django dev server)
- Make sure to run both servers for full functionality
- The old demo file is preserved at `Frontend/demo.html`

# Frontend Setup Guide

## Prerequisites
- Node.js 14.0 or higher
- npm 6.0 or higher (comes with Node.js)

## Installation Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Configuration

Create a `.env.local` file in the frontend directory:

**File: .env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 3. Start Development Server
```bash
npm run dev
```

The application will be available at: `http://localhost:3000`

### 4. Build for Production
```bash
npm run build
npm start
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Create production build
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Component Structure

### Pages
- **pages/index.js** - Main application page with form and results

### Components
- **FileUploader.js** - Drag-and-drop file upload with validation
- **ResultsDisplay.js** - Results visualization and metrics

### Styles
- **styles/globals.css** - Global styling and component styles

### Libraries
- **lib/api.js** - API client with all endpoints

## Troubleshooting

- **Port 3000 in use**: Change port with `npm run dev -- -p 3001`
- **API connection errors**: Check if backend is running on port 5000
- **Build errors**: Delete `node_modules` and `.next` folders, then run `npm install` again
- **Environment variable not working**: Restart dev server after changing `.env.local`

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Tips
- Use production build for better performance
- Clear browser cache if CSS/JS doesn't update
- Use browser DevTools for debugging

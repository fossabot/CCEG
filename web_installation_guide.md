# CCEG Web Application Installation Guide

Complete guide to setting up the CCEG Dataset Generator web application.

## Prerequisites

Before you begin, ensure you have:

- **Node.js 18+** ([Download](https://nodejs.org))
- **npm 9+** (comes with Node.js)
- **Git** (optional, for cloning)

## Installation Steps

### Step 1: Create Project Structure

```bash
# Create main web application directory
mkdir cceg-web-app
cd cceg-web-app

# Create source directory structure
mkdir -p src/components
mkdir -p public
```

### Step 2: Create Configuration Files

Create the following files in your `cceg-web-app` directory:

#### 2.1 Create `package.json`
```bash
cat > package.json << 'EOF'
{
  "name": "cceg-dataset-generator",
  "version": "1.0.0",
  "description": "CCEG Dataset Generator - Web Interface",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.263.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
EOF
```

#### 2.2 Create `tsconfig.json`
```bash
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF
```

#### 2.3 Create `tsconfig.node.json`
```bash
cat > tsconfig.node.json << 'EOF'
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
EOF
```

#### 2.4 Create `vite.config.ts`
```bash
cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
EOF
```

#### 2.5 Create `tailwind.config.js`
```bash
cat > tailwind.config.js << 'EOF'
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF
```

#### 2.6 Create `postcss.config.js`
```bash
cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF
```

#### 2.7 Create `index.html`
```bash
cat > index.html << 'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CCEG Dataset Generator</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
EOF
```

### Step 3: Create Source Files

#### 3.1 Create `src/index.css`
```bash
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  color-scheme: dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #0f172a;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}

#root {
  width: 100%;
}
EOF
```

#### 3.2 Create `src/main.tsx`
```bash
cat > src/main.tsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF
```

#### 3.3 Create `src/App.tsx`
```bash
cat > src/App.tsx << 'EOF'
import CCEGDatasetGenerator from './components/CCEGDatasetGenerator'

function App() {
  return <CCEGDatasetGenerator />
}

export default App
EOF
```

#### 3.4 Create `src/components/CCEGDatasetGenerator.tsx`

Copy your existing `dataset.generator.tsx` file content here, or create a new one:

```bash
# If you have the file already:
cp /path/to/dataset.generator.tsx src/components/CCEGDatasetGenerator.tsx

# Make sure it exports as default:
# export default CCEGDatasetGenerator
```

### Step 4: Install Dependencies

```bash
# Install all dependencies
npm install
```

This will install:
- React and React DOM
- TypeScript
- Vite (build tool)
- Tailwind CSS
- Lucide React (icons)
- All dev dependencies

### Step 5: Run the Application

```bash
# Start development server
npm run dev
```

The application will automatically open at `http://localhost:3000`

## Verification

After running `npm run dev`, you should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

Open your browser to `http://localhost:3000` and you should see the CCEG Dataset Generator interface.

## Troubleshooting

### Issue: "Cannot find module 'vite'"
**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript errors
**Solution:**
```bash
npm run type-check
# Fix any type errors shown
```

### Issue: Port 3000 already in use
**Solution:** Edit `vite.config.ts` and change the port:
```typescript
server: {
  port: 3001,  // Change to any available port
  open: true
}
```

### Issue: Tailwind styles not loading
**Solution:**
```bash
# Ensure Tailwind is properly configured
npm run dev -- --force
```

## Building for Production

Once development is complete:

```bash
# Create optimized production build
npm run build

# Preview production build locally
npm run preview
```

Production files will be in the `dist/` directory.

## Deployment Options

### Option 1: Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Option 3: Static Hosting (AWS S3, GitHub Pages, etc.)
```bash
npm run build
# Upload contents of dist/ to your hosting provider
```

## Directory Structure After Setup

```
cceg-web-app/
├── node_modules/          # Dependencies (created by npm install)
├── public/                # Static assets
├── src/
│   ├── components/
│   │   └── CCEGDatasetGenerator.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── .gitignore
```

## Next Steps

1. ✅ Generate dataset using the web interface
2. ✅ Download generated JSONL files
3. ✅ Validate data using the validation script
4. ✅ Customize the generator as needed

## Support

For issues or questions:
- Documentation: See README_WEB.md
- Email: support@cceg-dataset.com
- GitHub Issues: [Create an issue](https://github.com/cceg-dataset/cceg-generator/issues)

## Additional Resources

- [Vite Documentation](https://vitejs.dev)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
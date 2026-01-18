# CCEG Dataset Generator - Web Application

Professional web interface for generating the Cloud Compliance Execution Graph (CCEG) dataset.

## Quick Start

### Prerequisites
- Node.js 18+ 
- npm 9+

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will open at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
.
├── src/
│   ├── components/
│   │   └── CCEGDatasetGenerator.tsx  # Main generator component
│   ├── App.tsx                        # App wrapper
│   ├── main.tsx                       # Entry point
│   └── index.css                      # Global styles
├── public/                            # Static assets
├── index.html                         # HTML template
├── package.json                       # Dependencies
├── tsconfig.json                      # TypeScript config
├── vite.config.ts                     # Vite config
└── tailwind.config.js                 # Tailwind CSS config
```

## Features

- ✅ Generate 10,000 synthetic compliance records
- ✅ Three-layer architecture (Intent, Execution, Remediation)
- ✅ Real-time progress tracking
- ✅ Download individual or all files
- ✅ File size display
- ✅ Professional UI with Tailwind CSS
- ✅ TypeScript for type safety
- ✅ Fast development with Vite

## Building for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

Production files will be in the `dist/` directory.

## Deployment

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

### Deploy to Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Deploy to GitHub Pages
```bash
npm run build
# Copy dist/ contents to gh-pages branch
```

## Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## License

See LICENSE.md in the root directory.

## Support

For issues or questions:
- Email:ruwanpuragepawannimeshranasing@gmail.com
- GitHub:https://github.com/Pa345-ai/CCEG.git

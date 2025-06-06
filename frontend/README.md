# Elysia Web UI

A minimal React 18 + TypeScript interface styled with Tailwind CSS that mimics ChatGPT's layout and hooks into a voice assistant named **Elysia**.

## Getting Started

Install dependencies and start the dev server:

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
npm run preview
```

### Swapping the API

The UI ships with a stub in `src/api.ts` that returns dummy responses. Replace the `sendMessage` function with your backend call to integrate a real assistant.

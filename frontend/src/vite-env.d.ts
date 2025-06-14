/// <reference types="vite/client" />
// vite-env.d.ts
interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_API_URL_DEV: string;
  }
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  
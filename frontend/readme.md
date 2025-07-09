# Frontend - Proyecto DB Cepas

Este documento describe la estructura y funcionalidad de la carpeta `frontend` de la aplicación.

---

## 🗂 Estructura de carpetas y archivos

```bash
frontend/
├── node_modules/        # Dependencias instaladas vía npm
├── public/              # Archivos estáticos (favicon, index.html)
├── src/                 # Código fuente principal
│   ├── components/      # Componentes React reutilizables
│   │   ├── CepasColumns.tsx        # Definición de columnas para tablas de cepas
│   │   ├── CepasTable.tsx          # Tabla que muestra la lista de cepas
│   │   ├── DropdownMenu.tsx        # Menú desplegable genérico
│   │   ├── ModalConfirmation.tsx   # Modal de confirmación de acciones
│   │   ├── PrivateRoute.tsx        # Componente de ruta protegida por autenticación
│   │   └── TableStatus.tsx         # Indicadores de estado para filas de tabla
│   │
│   ├── pages/           # Páginas principales de la aplicación
│   │   ├── HomePage.tsx         # Página de inicio con resumen de cepas
│   │   ├── LoginPage.tsx        # Formulario de inicio de sesión
│   │   ├── NewCepaPage.tsx      # Formulario para crear una nueva cepa
│   │   └── NewAttributePage.tsx # Formulario para añadir atributos a una cepa
│   │
│   ├── routers/         # Configuración de rutas (React Router)
│   │   └── AppRouter.tsx         # Definición de rutas públicas y privadas
│   │
│   ├── services/        # Lógica de comunicación con el backend (API)
│   │   ├── CepasQuery.ts         # Funciones para CRUD de cepas
│   │   └── UsersQuery.ts         # Función para login y obtención de usuario actual
│   │
│   ├── stores/          # Contextos y gestores de estado global
│   │   └── AuthContext.tsx       # Contexto de autenticación y manejo de token JWT
│   │
│   ├── types/           # Definiciones de tipos TypeScript comunes
│   │   └── ts-agrid-react.d.ts   # Tipos de terceros (UI grid)
│   │
│   ├── utils/           # Utilidades y helpers
│   │   ├── cepaUpdate.ts         # Función para formatear datos de actualización
│   │   ├── exportExcel.ts        # Exportación de datos a Excel
│   │
│   ├── App.tsx          # Componente raíz que envuelve el router y estilos globales
│   ├── index.css        # Estilos globales de TailwindCSS
│   └── main.tsx         # Punto de entrada React (renderizado en DOM)
├── .env.example         # Ejemplo de variables de entorno para el frontend
├── package.json         # Metadatos y scripts de NPM
└── tsconfig.json        # Configuración de TypeScript
```

---

## 🚀 Ejecución en modo desarrollo

1. Abre una terminal y sitúate en la carpeta `frontend`:
   ```bash
   cd frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```
4. Abre tu navegador en `http://localhost:5173` para ver la aplicación.

## 📖 Notas adicionales

- Utilizamos **Vite** como bundler para mejorar la velocidad de desarrollo.
- TailwindCSS provee los estilos utilitarios; revisa `index.css` para configuraciones globales.
- Sigue el patrón **container-presentational** para separar lógica de negocio de la UI.


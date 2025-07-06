// src/routers/AppRouter.tsx
import {Routes, Route, Navigate } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import NewCepaPage from '../pages/NewCepaPage';
import NewAtributePage from '../pages/NewAtributePage';
import LoginPage from '../pages/LoginPage';
import PrivateRoute from '../components/PrivateRoute';

export default function AppRouter() {
  return (
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home"  element={<HomePage />} />

        {/* Grupo de rutas protegidas */}
        <Route element={<PrivateRoute />}>
          <Route path="/home/addcepa"      element={<NewCepaPage />} />
          <Route path="/home/addatribute"  element={<NewAtributePage />} />
          {/* agrega aquí más rutas */}
        </Route>

        {/* Si no coincide ninguna, redirige */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
  );
}
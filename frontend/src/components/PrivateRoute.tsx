// src/components/PrivateRoute.tsx
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute: React.FC = () => {
  const token = localStorage.getItem('token');
  // Si no hay token, redirige a /login
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  // Si hay token, renderiza las rutas hijas
  return <Outlet />;
};

export default PrivateRoute;

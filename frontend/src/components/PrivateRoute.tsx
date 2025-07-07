// src/components/PrivateRoute.tsx
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../stores/AuthContext'

const PrivateRoute: React.FC = () => {
  const { user, token } = useAuth()
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  if (user?.isAdmin == false) {
    // Si el usuario no es admin, redirige a la página de inicio
    return <Navigate to="/home" replace />;
  }
  // Si hay token, renderiza las rutas hijas
  return <Outlet />;
};

export default PrivateRoute;

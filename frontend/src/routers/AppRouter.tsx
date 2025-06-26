// src/routers/AppRouter.tsx
import { Routes, Route } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import NewCepaPage from '../pages/NewCepaPage';
import NewAtributePage from '../pages/NewAtributePage';
import LoginPage from '../pages/LoginPage';

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/home/addCepa" element={<NewCepaPage />} />
      <Route path="/home/addAtribute" element={<NewAtributePage />} />
    </Routes>
  );
}

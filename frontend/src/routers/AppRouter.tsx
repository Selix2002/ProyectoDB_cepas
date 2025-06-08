// src/routers/AppRouter.tsx
import { Routes, Route } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import NewCepaPage from '../pages/NewCepaPage';
import NewAtributePage from '../pages/NewAtributePage';

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/addCepa" element={<NewCepaPage />} />
      <Route path="/addAtribute" element={<NewAtributePage />} />
    </Routes>
  );
}

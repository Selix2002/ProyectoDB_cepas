// src/components/DropdownMenu.tsx
import React from 'react'

interface DropdownMenuProps {
  isOpen: boolean
  onClose: () => void
}

export const DropdownMenu: React.FC<DropdownMenuProps> = ({ isOpen, onClose }) => {
  return (
    <div
      className={`fixed top-0 right-0 h-screen w-1/5 bg-gray-800 bg-opacity-70 shadow-lg z-50
        transform ${isOpen ? 'translate-x-0' : 'translate-x-full'}
        transition-transform duration-300 ease-in-out`}
    >
      {/* Botón de cierre */}
      <div className="flex justify-end p-4">
        <button
          onClick={onClose}
          className="text-gray-300 hover:text-white focus:outline-none"
        >
          Cerrar ✕
        </button>
      </div>

      {/* Opciones del menú */}
      <nav className="px-4 pt-2">
        <ul className="space-y-2">
          <li>
            <button className="w-full text-left text-white hover:bg-gray-700 rounded p-2">
              Opción 1
            </button>
          </li>
          <li>
            <button className="w-full text-left text-white hover:bg-gray-700 rounded p-2">
              Opción 2
            </button>
          </li>
          <li>
            <button className="w-full text-left text-white hover:bg-gray-700 rounded p-2">
              Opción 3
            </button>
          </li>
        </ul>
      </nav>
    </div>
  )
}

export default DropdownMenu

import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../stores/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login(username, password)   // ya se encarga de token + user
      navigate('/home')
    } catch {
      setError('Usuario o contraseña inválidos')
    }
  }
  return (
    <div className="relative font-sans min-h-screen antialiased bg-gradient-to-tr from-gray-900 to-green-800 pt-24 pb-5">
      {/* Banner de error fijo */}
      {error && (
        <div className="fixed top-0 left-0 right-0 bg-red-600 text-white text-center py-2 z-50">
          {error}
        </div>
      )}

      <div className="flex flex-col justify-center sm:w-96 sm:mx-auto mx-5 mb-5 space-y-8">
        <h1 className="font-bold text-center text-4xl text-yellow-500">
          Administrar <span className="text-blue-500">Cepas</span>
        </h1>
        <form onSubmit={handleSubmit} className="flex flex-col bg-white p-10 rounded-lg shadow space-y-6">
          <h2 className="font-bold text-xl text-center">
            Inicia sesión para continuar
          </h2>

          <div className="flex flex-col space-y-1">
            <input
              type="text"
              name="username"
              id="username"
              placeholder="Nombre de usuario"
              className="border-2 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-400 focus:shadow"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="flex flex-col space-y-1">
            <input
              type="password"
              name="password"
              id="password"
              placeholder="Contraseña"
              className="border-2 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-400 focus:shadow"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>


          <div className="flex flex-col-reverse sm:flex-row sm:justify-between items-center">
            <a
              href="/home"
              className="inline-block text-blue-500 hover:text-blue-800 hover:underline mt-3 sm:mt-0"
            >
              Ingresar como invitado
            </a>
            <button
              type="submit"
              className="bg-blue-500 text-white py-2 px-6 rounded hover:bg-blue-600 transition"
            >
              Aceptar
            </button>
          </div>
        </form>
        <div className="flex justify-center text-gray-500 text-sm">
          <p>&copy;2025, SM. Todos los derechos reservados.</p>
        </div>
      </div>
    </div>
  );
}

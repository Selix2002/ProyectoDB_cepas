// src/stores/AuthContext.tsx
import { useEffect, useState, createContext, useContext} from 'react'
import { login as apiLogin, getCurrentUser } from '../services/UsersQuery'
import type { User } from '../interfaces/index'
import type {ReactNode} from 'react'
import type { AuthContextType } from '../interfaces/index'
import { api } from '../services/api'


const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)

  // Al montar, leo token y trato de rehidratar el user
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      setToken(storedToken)
      api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
      getCurrentUser()
        .then(u => setUser(u))
        .catch(() => {
          // si falla (401), limpio todo
          localStorage.removeItem('auth_token')
          setToken(null)
        })
    }
  }, [])

  const login = async (username: string, password: string) => {
    const { accessToken } = await apiLogin(username, password)
    setToken(accessToken)
    localStorage.setItem('auth_token', accessToken)
    // Sólo *ahora* que tengo token, traigo el user
    const u = await getCurrentUser()
    setUser(u)
    console.log(u.isAdmin, 'user en AuthContext.tsx')
    localStorage.setItem('auth_user', JSON.stringify(u))
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('auth_user')
    localStorage.removeItem('auth_token')


    delete api.defaults.headers.common['Authorization']
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}

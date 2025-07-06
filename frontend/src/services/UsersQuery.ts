import axios from 'axios'
import type { Token, User, UserCreate } from '../interfaces/index'

// Base URL del backend, configurable desde variables de entorno
const API_BASE ='//localhost:8000'

/**
 * Obtiene todos los usuarios
 */
export async function getUsers(): Promise<User[]> {
  const response = await axios.get<User[]>(`${API_BASE}/users`)
  return response.data
}

/**
 * Crea un nuevo usuario
 */
export async function createUser(user: UserCreate): Promise<User> {
  const response = await axios.post<User>(
    `${API_BASE}/users`,
    user,
    {
      headers: { 'Content-Type': 'application/json' },
    }
  )
  return response.data
}

/**
 * Obtiene un usuario por ID
 */
export async function getUser(id: number): Promise<User> {
  const response = await axios.get<User>(`${API_BASE}/users/${id}`)
  return response.data
}

/**
 * Obtiene el usuario actualmente autenticado
 */
export async function getMyUser(): Promise<User> {
  const response = await axios.get<User>(`${API_BASE}/users/me`)
  return response.data
}

/**
 * Realiza login y obtiene el token de acceso
 */
export async function login(
  username: string,
  password: string,
): Promise<Token> {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)

  const response = await axios.post<Token>(
    `${API_BASE}/auth/login`,
    params,
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  )
  return response.data
}

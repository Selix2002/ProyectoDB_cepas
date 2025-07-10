// src/services/UsersQuery.ts
import type { Token, User } from '../interfaces/index'
import {api} from "./api";

export interface LoginToken {
  accessToken: string
}

export async function login(
    username: string,
    password: string
  ): Promise<LoginToken> {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
  
    const { data } = await api.post<Token>(
      `/auth/login`,
      params,
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    )
  
    // aquí hacemos el alias: tomo data.access_token y lo renombro a accessToken
    const { access_token: accessToken } = data  
    console.log('Token recibido:', accessToken)
  
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
    return { accessToken }
  }


  // esta interfaz solo la uso para mapear el JSON que devuelve el endpoint /users/me. 
interface RawUser {
  id: number
  username: string
  is_admin: boolean
}
export async function getCurrentUser(): Promise<User> {
  const { data: raw } = await api.get<RawUser>(
    `/users/me`
  )
  // aquí mapeamos is_admin → isAdmin
  const user: User = {
    id: raw.id,
    username: raw.username,
    isAdmin: raw.is_admin,
  }
  return user
}

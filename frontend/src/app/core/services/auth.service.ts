import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../api-base-url';
import { ActorAutenticado, RegistroPayload, TokensRespuesta } from '../models/actor.model';
import { RespuestaEstandar } from '../models/api-response.model';

const CLAVE_ACCESS_TOKEN = 'agora_access_token';
const CLAVE_REFRESH_TOKEN = 'agora_refresh_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);

  private readonly actorSignal = signal<ActorAutenticado | null>(this.leerActorDesdeTokenGuardado());
  readonly actor = this.actorSignal.asReadonly();
  readonly estaAutenticado = computed(() => this.actorSignal() !== null);

  async login(identificador: string, password: string): Promise<ActorAutenticado> {
    const respuesta = await firstValueFrom(
      this.http.post<RespuestaEstandar<TokensRespuesta>>(`${API_BASE_URL}/auth/login/`, {
        identificador,
        password,
      }),
    );
    return this.guardarSesion(respuesta.datos!);
  }

  async registrar(datos: RegistroPayload): Promise<ActorAutenticado> {
    const respuesta = await firstValueFrom(
      this.http.post<RespuestaEstandar<TokensRespuesta>>(`${API_BASE_URL}/auth/registro/`, datos),
    );
    return this.guardarSesion(respuesta.datos!);
  }

  cerrarSesion(): void {
    localStorage.removeItem(CLAVE_ACCESS_TOKEN);
    localStorage.removeItem(CLAVE_REFRESH_TOKEN);
    this.actorSignal.set(null);
  }

  obtenerAccessToken(): string | null {
    return localStorage.getItem(CLAVE_ACCESS_TOKEN);
  }

  private guardarSesion(tokens: TokensRespuesta): ActorAutenticado {
    localStorage.setItem(CLAVE_ACCESS_TOKEN, tokens.access);
    localStorage.setItem(CLAVE_REFRESH_TOKEN, tokens.refresh);
    const actor = this.decodificarActor(tokens.access);
    this.actorSignal.set(actor);
    return actor;
  }

  private leerActorDesdeTokenGuardado(): ActorAutenticado | null {
    const token = localStorage.getItem(CLAVE_ACCESS_TOKEN);
    if (!token) {
      return null;
    }
    try {
      return this.decodificarActor(token);
    } catch {
      return null;
    }
  }

  private decodificarActor(accessToken: string): ActorAutenticado {
    const payloadBase64 = accessToken.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const payload = JSON.parse(atob(payloadBase64));
    return {
      id: Number(payload.user_id),
      nombre: payload.nombre,
      rol: payload.rol,
      tipoActor: payload.tipo_actor,
    };
  }
}

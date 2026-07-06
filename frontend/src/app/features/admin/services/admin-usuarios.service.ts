import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { Multa } from '../../../core/models/multa.model';
import { RespuestaEstandar } from '../../../core/models/api-response.model';
import { Usuario, UsuarioDetalle } from '../models/admin.model';

@Injectable({ providedIn: 'root' })
export class AdminUsuariosService {
  private readonly http = inject(HttpClient);

  async listarUsuarios(): Promise<Usuario[]> {
    return firstValueFrom(this.http.get<Usuario[]>(`${API_BASE_URL}/admin/usuarios/`));
  }

  async obtenerDetalle(usuarioId: number): Promise<UsuarioDetalle> {
    const respuesta = await firstValueFrom(
      this.http.get<RespuestaEstandar<UsuarioDetalle>>(`${API_BASE_URL}/admin/usuarios/${usuarioId}/`),
    );
    return respuesta.datos!;
  }

  async suspender(usuarioId: number): Promise<Usuario> {
    const respuesta = await firstValueFrom(
      this.http.post<RespuestaEstandar<Usuario>>(`${API_BASE_URL}/admin/usuarios/${usuarioId}/suspender/`, {}),
    );
    return respuesta.datos!;
  }

  async anularMulta(multaId: number, justificacion: string): Promise<Multa> {
    const respuesta = await firstValueFrom(
      this.http.post<RespuestaEstandar<Multa>>(`${API_BASE_URL}/multas/${multaId}/anular/`, { justificacion }),
    );
    return respuesta.datos!;
  }
}

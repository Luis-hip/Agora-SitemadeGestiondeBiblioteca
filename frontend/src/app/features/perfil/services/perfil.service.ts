import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { RespuestaEstandar } from '../../../core/models/api-response.model';
import { Multa, Perfil } from '../models/perfil.model';

@Injectable({ providedIn: 'root' })
export class PerfilService {
  private readonly http = inject(HttpClient);

  async obtenerPerfil(): Promise<Perfil> {
    const respuesta = await firstValueFrom(
      this.http.get<RespuestaEstandar<Perfil>>(`${API_BASE_URL}/perfil/`),
    );
    return respuesta.datos!;
  }

  async pagarMulta(multaId: number): Promise<Multa> {
    const respuesta = await firstValueFrom(
      this.http.post<RespuestaEstandar<Multa>>(`${API_BASE_URL}/multas/${multaId}/pagar/`, {}),
    );
    return respuesta.datos!;
  }
}

import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { RespuestaEstandar } from '../../../core/models/api-response.model';
import { ConfiguracionBiblioteca, ConfiguracionBibliotecaPayload } from '../models/admin.model';

@Injectable({ providedIn: 'root' })
export class AdminConfiguracionService {
  private readonly http = inject(HttpClient);

  async obtenerConfiguracion(): Promise<ConfiguracionBiblioteca> {
    const respuesta = await firstValueFrom(
      this.http.get<RespuestaEstandar<ConfiguracionBiblioteca>>(`${API_BASE_URL}/admin/configuracion/`),
    );
    return respuesta.datos!;
  }

  async actualizarConfiguracion(payload: ConfiguracionBibliotecaPayload): Promise<ConfiguracionBiblioteca> {
    const respuesta = await firstValueFrom(
      this.http.patch<RespuestaEstandar<ConfiguracionBiblioteca>>(`${API_BASE_URL}/admin/configuracion/`, payload),
    );
    return respuesta.datos!;
  }
}

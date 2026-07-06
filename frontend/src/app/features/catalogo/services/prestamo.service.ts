import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { RespuestaEstandar } from '../../../core/models/api-response.model';
import { Prestamo } from '../models/catalogo.model';

@Injectable({ providedIn: 'root' })
export class PrestamoService {
  private readonly http = inject(HttpClient);

  async solicitarPrestamo(libroId: number): Promise<RespuestaEstandar<Prestamo>> {
    return firstValueFrom(
      this.http.post<RespuestaEstandar<Prestamo>>(`${API_BASE_URL}/prestamos/`, { libro_id: libroId }),
    );
  }
}

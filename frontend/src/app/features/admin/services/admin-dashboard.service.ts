import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { RespuestaEstandar } from '../../../core/models/api-response.model';
import { AdminMulta, AdminPrestamo, Dashboard, Devolucion } from '../models/admin.model';

@Injectable({ providedIn: 'root' })
export class AdminDashboardService {
  private readonly http = inject(HttpClient);

  async obtenerDashboard(): Promise<Dashboard> {
    const respuesta = await firstValueFrom(
      this.http.get<RespuestaEstandar<Dashboard>>(`${API_BASE_URL}/admin/dashboard/`),
    );
    return respuesta.datos!;
  }

  async listarPrestamos(filtros: { estado?: string; vencePronto?: boolean } = {}): Promise<AdminPrestamo[]> {
    let params = new HttpParams();
    if (filtros.estado) {
      params = params.set('estado', filtros.estado);
    }
    if (filtros.vencePronto) {
      params = params.set('vence_pronto', 'true');
    }
    return firstValueFrom(this.http.get<AdminPrestamo[]>(`${API_BASE_URL}/admin/prestamos/`, { params }));
  }

  async listarDevolucionesDeHoy(): Promise<Devolucion[]> {
    return firstValueFrom(this.http.get<Devolucion[]>(`${API_BASE_URL}/admin/devoluciones/`));
  }

  async listarMultas(filtros: { estado?: string } = {}): Promise<AdminMulta[]> {
    let params = new HttpParams();
    if (filtros.estado) {
      params = params.set('estado', filtros.estado);
    }
    return firstValueFrom(this.http.get<AdminMulta[]>(`${API_BASE_URL}/admin/multas/`, { params }));
  }
}

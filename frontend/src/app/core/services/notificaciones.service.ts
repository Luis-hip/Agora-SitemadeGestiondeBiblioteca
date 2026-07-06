import { Injectable, computed, inject, signal } from '@angular/core';

import { AdminDashboardService } from '../../features/admin/services/admin-dashboard.service';
import { PerfilService } from '../../features/perfil/services/perfil.service';
import { NotificacionItem } from '../models/notificacion.model';
import { AuthService } from './auth.service';

const DIAS_VENCIMIENTO_PROXIMO = 2;

@Injectable({ providedIn: 'root' })
export class NotificacionesService {
  private readonly authService = inject(AuthService);
  private readonly perfilService = inject(PerfilService);
  private readonly dashboardService = inject(AdminDashboardService);

  private readonly notificacionesSignal = signal<NotificacionItem[]>([]);
  readonly notificaciones = this.notificacionesSignal.asReadonly();
  readonly cantidad = computed(() => this.notificacionesSignal().length);

  async cargar(): Promise<void> {
    const actor = this.authService.actor();
    if (!actor) {
      this.notificacionesSignal.set([]);
      return;
    }
    try {
      if (actor.tipoActor === 'USUARIO') {
        this.notificacionesSignal.set(await this.construirParaUsuario());
      } else {
        this.notificacionesSignal.set(await this.construirParaBibliotecario());
      }
    } catch {
      this.notificacionesSignal.set([]);
    }
  }

  private async construirParaUsuario(): Promise<NotificacionItem[]> {
    const perfil = await this.perfilService.obtenerPerfil();
    const items: NotificacionItem[] = perfil.multas_pendientes.map((multa) => ({
      id: `multa-${multa.id}`,
      tipo: 'multa',
      mensaje: `Multa pendiente de $${multa.monto} por "${multa.prestamo.libro.titulo}".`,
    }));

    const limite = new Date();
    limite.setDate(limite.getDate() + DIAS_VENCIMIENTO_PROXIMO);

    for (const prestamo of perfil.prestamos_activos) {
      if (new Date(prestamo.fecha_dev_esperada) <= limite) {
        items.push({
          id: `prestamo-${prestamo.id}`,
          tipo: 'vencimiento',
          mensaje: `Tu prestamo de "${prestamo.libro.titulo}" vence el ${prestamo.fecha_dev_esperada}.`,
        });
      }
    }

    return items;
  }

  private async construirParaBibliotecario(): Promise<NotificacionItem[]> {
    const dashboard = await this.dashboardService.obtenerDashboard();
    const items: NotificacionItem[] = [];

    if (dashboard.kpis.vencimientos_proximos > 0) {
      items.push({
        id: 'vencimientos-proximos',
        tipo: 'vencimiento',
        mensaje: `${dashboard.kpis.vencimientos_proximos} prestamo(s) vencen en las proximas 48 horas.`,
      });
    }

    if (Number(dashboard.kpis.multas_pendientes_total) > 0) {
      items.push({
        id: 'multas-pendientes',
        tipo: 'multa',
        mensaje: `Hay multas pendientes por un total de $${dashboard.kpis.multas_pendientes_total}.`,
      });
    }

    return items;
  }
}

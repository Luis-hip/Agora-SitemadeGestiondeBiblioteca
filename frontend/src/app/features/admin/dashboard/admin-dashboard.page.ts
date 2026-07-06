import { Component, inject, signal } from '@angular/core';

import { ToastService } from '../../../core/services/toast.service';
import { clasesBadgeEstado } from '../../../shared/estado-badge.util';
import { AdminMulta, AdminPrestamo, Dashboard, Devolucion } from '../models/admin.model';
import { AdminDashboardService } from '../services/admin-dashboard.service';

type VistaDetalle = 'resumen' | 'activos' | 'vencimientos' | 'devoluciones' | 'multas';

@Component({
  selector: 'app-admin-dashboard-page',
  templateUrl: './admin-dashboard.page.html',
})
export class AdminDashboardPageComponent {
  private readonly dashboardService = inject(AdminDashboardService);
  private readonly toast = inject(ToastService);

  protected readonly dashboard = signal<Dashboard | null>(null);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);

  protected readonly vistaDetalle = signal<VistaDetalle>('resumen');
  protected readonly cargandoDetalle = signal(false);
  protected readonly itemsPrestamo = signal<AdminPrestamo[]>([]);
  protected readonly itemsDevolucion = signal<Devolucion[]>([]);
  protected readonly itemsMulta = signal<AdminMulta[]>([]);

  protected readonly tarjetas = [
    { id: 'activos' as const, etiqueta: 'Prestamos Activos', color: 'text-blue-700 bg-blue-50' },
    { id: 'devoluciones' as const, etiqueta: 'Devoluciones de Hoy', color: 'text-emerald-700 bg-emerald-50' },
    { id: 'multas' as const, etiqueta: 'Multas Pendientes', color: 'text-orange-700 bg-orange-50' },
    { id: 'vencimientos' as const, etiqueta: 'Vencimientos Proximos (48h)', color: 'text-red-700 bg-red-50' },
  ];

  constructor() {
    void this.cargarDashboard();
  }

  protected valorTarjeta(id: VistaDetalle): string {
    const kpis = this.dashboard()?.kpis;
    if (!kpis) {
      return '-';
    }
    switch (id) {
      case 'activos':
        return String(kpis.prestamos_activos);
      case 'devoluciones':
        return String(kpis.devoluciones_hoy);
      case 'multas':
        return `$${kpis.multas_pendientes_total}`;
      case 'vencimientos':
        return String(kpis.vencimientos_proximos);
      default:
        return '-';
    }
  }

  protected async verDetalle(vista: VistaDetalle): Promise<void> {
    this.vistaDetalle.set(vista);
    this.cargandoDetalle.set(true);
    try {
      if (vista === 'activos') {
        this.itemsPrestamo.set(await this.dashboardService.listarPrestamos({ estado: 'ACTIVO' }));
      } else if (vista === 'vencimientos') {
        this.itemsPrestamo.set(await this.dashboardService.listarPrestamos({ vencePronto: true }));
      } else if (vista === 'devoluciones') {
        this.itemsDevolucion.set(await this.dashboardService.listarDevolucionesDeHoy());
      } else if (vista === 'multas') {
        this.itemsMulta.set(await this.dashboardService.listarMultas({ estado: 'PENDIENTE' }));
      }
    } catch {
      this.toast.error('No se pudo cargar el detalle de esta metrica.');
    } finally {
      this.cargandoDetalle.set(false);
    }
  }

  protected volverAlResumen(): void {
    this.vistaDetalle.set('resumen');
  }

  protected clasesBadge(estado: string): string {
    return clasesBadgeEstado(estado);
  }

  private async cargarDashboard(): Promise<void> {
    this.cargando.set(true);
    this.error.set(null);
    try {
      this.dashboard.set(await this.dashboardService.obtenerDashboard());
    } catch {
      this.error.set('No se pudo cargar el panel de control.');
    } finally {
      this.cargando.set(false);
    }
  }
}

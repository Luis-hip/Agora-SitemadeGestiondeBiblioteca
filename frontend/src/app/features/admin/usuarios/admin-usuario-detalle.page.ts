import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Multa } from '../../../core/models/multa.model';
import { ToastService } from '../../../core/services/toast.service';
import { clasesBadgeEstado } from '../../../shared/estado-badge.util';
import { MultaDetalleModalComponent } from '../../../shared/multa-detalle-modal/multa-detalle-modal.component';
import { UsuarioDetalle } from '../models/admin.model';
import { AdminUsuariosService } from '../services/admin-usuarios.service';

@Component({
  selector: 'app-admin-usuario-detalle-page',
  imports: [MultaDetalleModalComponent],
  templateUrl: './admin-usuario-detalle.page.html',
})
export class AdminUsuarioDetallePageComponent {
  private readonly usuariosService = inject(AdminUsuariosService);
  private readonly toast = inject(ToastService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly usuarioId = Number(this.route.snapshot.paramMap.get('id'));

  protected readonly detalle = signal<UsuarioDetalle | null>(null);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);

  protected readonly multaSeleccionada = signal<Multa | null>(null);
  protected readonly anulando = signal(false);

  constructor() {
    void this.cargarDetalle();
  }

  protected volver(): void {
    this.router.navigate(['/admin/usuarios']);
  }

  protected clasesBadge(estado: string): string {
    return clasesBadgeEstado(estado);
  }

  protected abrirMulta(multa: Multa): void {
    this.multaSeleccionada.set(multa);
  }

  protected cerrarMulta(): void {
    this.multaSeleccionada.set(null);
  }

  protected async confirmarAnulacion(justificacion: string): Promise<void> {
    const multa = this.multaSeleccionada();
    if (!multa) {
      return;
    }
    this.anulando.set(true);
    try {
      await this.usuariosService.anularMulta(multa.id, justificacion);
      this.toast.exito('Multa anulada exitosamente.');
      setTimeout(() => this.multaSeleccionada.set(null), 600);
      await this.cargarDetalle();
    } catch (err) {
      const error = err as HttpErrorResponse;
      const mensaje = error.error?.mensaje ?? 'No se pudo anular la multa.';
      if (error.status === 422) {
        this.toast.advertencia(mensaje);
      } else {
        this.toast.error(mensaje);
      }
    } finally {
      this.anulando.set(false);
    }
  }

  private async cargarDetalle(): Promise<void> {
    this.cargando.set(true);
    this.error.set(null);
    try {
      this.detalle.set(await this.usuariosService.obtenerDetalle(this.usuarioId));
    } catch {
      this.error.set('No se pudo cargar el detalle de este usuario.');
    } finally {
      this.cargando.set(false);
    }
  }
}

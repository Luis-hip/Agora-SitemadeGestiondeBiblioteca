import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { ToastService } from '../../../core/services/toast.service';
import { AdminConfiguracionService } from '../services/admin-configuracion.service';

@Component({
  selector: 'app-admin-ajustes-page',
  imports: [ReactiveFormsModule],
  templateUrl: './admin-ajustes.page.html',
})
export class AdminAjustesPageComponent {
  private readonly configuracionService = inject(AdminConfiguracionService);
  private readonly toast = inject(ToastService);
  private readonly fb = inject(FormBuilder);

  protected readonly cargando = signal(true);
  protected readonly guardando = signal(false);

  protected readonly formulario = this.fb.nonNullable.group({
    tarifa_multa_diaria: [0, [Validators.required, Validators.min(0)]],
    dias_maximos_prestamo: [14, [Validators.required, Validators.min(1)]],
  });

  constructor() {
    void this.cargarConfiguracion();
  }

  protected alEnviarFormulario(evento: Event): void {
    evento.preventDefault();
    void this.guardar();
  }

  protected async guardar(): Promise<void> {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      return;
    }
    this.guardando.set(true);
    try {
      await this.configuracionService.actualizarConfiguracion(this.formulario.getRawValue());
      this.toast.exito('Configuracion actualizada exitosamente.');
    } catch (err) {
      const error = err as HttpErrorResponse;
      this.toast.error(error.error?.mensaje ?? 'No se pudo actualizar la configuracion.');
    } finally {
      this.guardando.set(false);
    }
  }

  private async cargarConfiguracion(): Promise<void> {
    this.cargando.set(true);
    try {
      const configuracion = await this.configuracionService.obtenerConfiguracion();
      this.formulario.setValue({
        tarifa_multa_diaria: Number(configuracion.tarifa_multa_diaria),
        dias_maximos_prestamo: configuracion.dias_maximos_prestamo,
      });
    } catch {
      this.toast.error('No se pudo cargar la configuracion de la biblioteca.');
    } finally {
      this.cargando.set(false);
    }
  }
}

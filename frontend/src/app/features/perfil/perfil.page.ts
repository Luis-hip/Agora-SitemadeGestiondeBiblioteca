import { HttpErrorResponse } from '@angular/common/http';
import { Component, ElementRef, QueryList, ViewChildren, computed, inject, signal } from '@angular/core';

import { ToastService } from '../../core/services/toast.service';
import { urlAvatar } from '../../shared/avatar.util';
import { MultaDetalleModalComponent } from '../../shared/multa-detalle-modal/multa-detalle-modal.component';
import { Multa, Perfil } from './models/perfil.model';
import { PerfilService } from './services/perfil.service';

type PestanaPrincipal = 'general' | 'activos' | 'multas' | 'historial' | 'config';
type SubPestanaHistorial = 'prestamos' | 'multas';

@Component({
  selector: 'app-perfil-page',
  imports: [MultaDetalleModalComponent],
  templateUrl: './perfil.page.html',
})
export class PerfilPageComponent {
  private readonly perfilService = inject(PerfilService);
  private readonly toast = inject(ToastService);

  protected readonly perfil = signal<Perfil | null>(null);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);

  protected readonly pestanaActiva = signal<PestanaPrincipal>('general');
  protected readonly subPestanaHistorial = signal<SubPestanaHistorial>('prestamos');

  protected readonly multaSeleccionada = signal<Multa | null>(null);
  protected readonly pagando = signal(false);

  protected readonly tieneMultasPendientes = computed(
    () => (this.perfil()?.multas_pendientes.length ?? 0) > 0,
  );

  protected readonly pestanas: { id: PestanaPrincipal; etiqueta: string }[] = [
    { id: 'general', etiqueta: 'General' },
    { id: 'activos', etiqueta: 'Prestamos Activos' },
    { id: 'multas', etiqueta: 'Multas Pendientes' },
    { id: 'historial', etiqueta: 'Historial' },
    { id: 'config', etiqueta: 'Configuraciones' },
  ];

  @ViewChildren('tabBtn') private tabButtons!: QueryList<ElementRef<HTMLButtonElement>>;

  constructor() {
    void this.cargarPerfil();
  }

  protected urlAvatarUsuario(nombre: string): string {
    return urlAvatar(nombre);
  }

  protected seleccionarPestana(pestana: PestanaPrincipal): void {
    this.pestanaActiva.set(pestana);
  }

  protected alPresionarTeclaEnPestanas(evento: KeyboardEvent): void {
    if (evento.key !== 'ArrowRight' && evento.key !== 'ArrowLeft') {
      return;
    }
    evento.preventDefault();
    const indiceActual = this.pestanas.findIndex((tab) => tab.id === this.pestanaActiva());
    const total = this.pestanas.length;
    const siguienteIndice =
      evento.key === 'ArrowRight' ? (indiceActual + 1) % total : (indiceActual - 1 + total) % total;

    this.pestanaActiva.set(this.pestanas[siguienteIndice].id);
    this.tabButtons.toArray()[siguienteIndice]?.nativeElement.focus();
  }

  protected seleccionarSubPestanaHistorial(sub: SubPestanaHistorial): void {
    this.subPestanaHistorial.set(sub);
  }

  protected abrirMulta(multa: Multa): void {
    this.multaSeleccionada.set(multa);
  }

  protected cerrarMulta(): void {
    this.multaSeleccionada.set(null);
  }

  protected async confirmarPago(): Promise<void> {
    const multa = this.multaSeleccionada();
    if (!multa) {
      return;
    }
    this.pagando.set(true);
    try {
      await this.perfilService.pagarMulta(multa.id);
      this.toast.exito('Multa pagada exitosamente.');
      setTimeout(() => this.multaSeleccionada.set(null), 600);
      await this.cargarPerfil();
    } catch (err) {
      const error = err as HttpErrorResponse;
      const mensaje = error.error?.mensaje ?? 'No se pudo procesar el pago de la multa.';
      if (error.status === 422) {
        this.toast.advertencia(mensaje);
      } else {
        this.toast.error(mensaje);
      }
    } finally {
      this.pagando.set(false);
    }
  }

  private async cargarPerfil(): Promise<void> {
    this.cargando.set(true);
    this.error.set(null);
    try {
      const perfil = await this.perfilService.obtenerPerfil();
      this.perfil.set(perfil);
    } catch {
      this.error.set('No se pudo cargar tu perfil. Intenta de nuevo mas tarde.');
    } finally {
      this.cargando.set(false);
    }
  }
}

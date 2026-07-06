import { Injectable, signal } from '@angular/core';

export type ToastTipo = 'exito' | 'advertencia' | 'error';

export interface ToastItem {
  id: number;
  tipo: ToastTipo;
  mensaje: string;
}

const DURACION_AUTO_DESCARTE_MS = 4000;

@Injectable({ providedIn: 'root' })
export class ToastService {
  private readonly toastsSignal = signal<ToastItem[]>([]);
  readonly toasts = this.toastsSignal.asReadonly();

  private contador = 0;

  exito(mensaje: string): void {
    this.mostrar('exito', mensaje, DURACION_AUTO_DESCARTE_MS);
  }

  advertencia(mensaje: string): void {
    this.mostrar('advertencia', mensaje, DURACION_AUTO_DESCARTE_MS);
  }

  error(mensaje: string): void {
    this.mostrar('error', mensaje, null);
  }

  cerrar(id: number): void {
    this.toastsSignal.update((lista) => lista.filter((toast) => toast.id !== id));
  }

  private mostrar(tipo: ToastTipo, mensaje: string, autoDescarteMs: number | null): void {
    const id = ++this.contador;
    this.toastsSignal.update((lista) => [...lista, { id, tipo, mensaje }]);
    if (autoDescarteMs !== null) {
      setTimeout(() => this.cerrar(id), autoDescarteMs);
    }
  }
}

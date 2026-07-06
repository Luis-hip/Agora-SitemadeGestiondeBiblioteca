import { Component, EventEmitter, HostListener, Input, Output, signal } from '@angular/core';

import { Multa } from '../../core/models/multa.model';

@Component({
  selector: 'app-multa-detalle-modal',
  templateUrl: './multa-detalle-modal.component.html',
})
export class MultaDetalleModalComponent {
  @Input({ required: true }) multa!: Multa;
  @Input() procesando = false;
  @Input() modoAdmin = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() pagarAhora = new EventEmitter<void>();
  @Output() anularMulta = new EventEmitter<string>();

  protected readonly justificacion = signal('');

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }

  protected confirmarAnulacion(): void {
    if (this.justificacion().trim().length === 0) {
      return;
    }
    this.anularMulta.emit(this.justificacion().trim());
  }
}

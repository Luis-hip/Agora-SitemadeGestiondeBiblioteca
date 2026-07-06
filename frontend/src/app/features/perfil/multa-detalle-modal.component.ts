import { Component, EventEmitter, HostListener, Input, Output } from '@angular/core';

import { Multa } from './models/perfil.model';

@Component({
  selector: 'app-multa-detalle-modal',
  templateUrl: './multa-detalle-modal.component.html',
})
export class MultaDetalleModalComponent {
  @Input({ required: true }) multa!: Multa;
  @Input() pagando = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() pagarAhora = new EventEmitter<void>();

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }
}

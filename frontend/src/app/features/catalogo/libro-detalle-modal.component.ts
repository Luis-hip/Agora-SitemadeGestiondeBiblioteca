import { Component, EventEmitter, HostListener, Input, Output } from '@angular/core';

import { Libro } from './models/catalogo.model';

@Component({
  selector: 'app-libro-detalle-modal',
  templateUrl: './libro-detalle-modal.component.html',
})
export class LibroDetalleModalComponent {
  @Input({ required: true }) libro!: Libro;
  @Input() enviando = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() solicitarPrestamo = new EventEmitter<void>();

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }
}

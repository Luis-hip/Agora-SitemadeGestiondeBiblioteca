import { Component, EventEmitter, HostListener, Input, Output } from '@angular/core';

@Component({
  selector: 'app-confirmar-eliminar-modal',
  templateUrl: './confirmar-eliminar-modal.component.html',
})
export class ConfirmarEliminarModalComponent {
  @Input({ required: true }) titulo!: string;
  @Input({ required: true }) mensaje!: string;
  @Input() eliminando = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() confirmar = new EventEmitter<void>();

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }
}

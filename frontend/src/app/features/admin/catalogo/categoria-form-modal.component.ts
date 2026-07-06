import { Component, EventEmitter, HostListener, Input, OnChanges, Output, signal } from '@angular/core';

import { Categoria } from '../../catalogo/models/catalogo.model';

export interface CategoriaPayload {
  nombre: string;
  descripcion: string;
}

@Component({
  selector: 'app-categoria-form-modal',
  templateUrl: './categoria-form-modal.component.html',
})
export class CategoriaFormModalComponent implements OnChanges {
  @Input() categoria: Categoria | null = null;
  @Input() guardando = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() guardar = new EventEmitter<CategoriaPayload>();

  protected readonly nombre = signal('');
  protected readonly descripcion = signal('');

  ngOnChanges(): void {
    this.nombre.set(this.categoria?.nombre ?? '');
    this.descripcion.set(this.categoria?.descripcion ?? '');
  }

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }

  protected alEnviarFormulario(evento: Event): void {
    evento.preventDefault();
    this.guardar.emit({ nombre: this.nombre().trim(), descripcion: this.descripcion().trim() });
  }
}

import { Component, EventEmitter, HostListener, Input, OnChanges, Output, signal } from '@angular/core';

import { Autor, Categoria } from '../../catalogo/models/catalogo.model';
import { Libro, LibroFormOutput } from '../models/admin.model';

@Component({
  selector: 'app-libro-form-modal',
  templateUrl: './libro-form-modal.component.html',
})
export class LibroFormModalComponent implements OnChanges {
  @Input({ required: true }) categorias: Categoria[] = [];
  @Input({ required: true }) autores: Autor[] = [];
  @Input() libro: Libro | null = null;
  @Input() guardando = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() guardar = new EventEmitter<LibroFormOutput>();

  protected readonly titulo = signal('');
  protected readonly isbn = signal('');
  protected readonly fechaPublicacion = signal('');
  protected readonly categoriaId = signal<number | null>(null);
  protected readonly disponible = signal(true);
  protected readonly stock = signal(1);
  protected readonly autorSeleccionadoId = signal<number | null>(null);
  protected readonly autorNuevoNombre = signal('');

  ngOnChanges(): void {
    this.titulo.set(this.libro?.titulo ?? '');
    this.isbn.set(this.libro?.isbn ?? '');
    this.fechaPublicacion.set(this.libro?.fecha_publicacion ?? '');
    this.categoriaId.set(this.libro?.categoria.id ?? this.categorias[0]?.id ?? null);
    this.disponible.set(this.libro?.disponible ?? true);
    this.stock.set(this.libro?.stock ?? 1);
    this.autorSeleccionadoId.set(this.libro?.autores[0]?.id ?? this.autores[0]?.id ?? null);
    this.autorNuevoNombre.set('');
  }

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }

  protected alEnviarFormulario(evento: Event): void {
    evento.preventDefault();
    if (!this.categoriaId()) {
      return;
    }
    this.guardar.emit({
      titulo: this.titulo().trim(),
      isbn: this.isbn().trim(),
      fecha_publicacion: this.fechaPublicacion(),
      disponible: this.disponible(),
      stock: this.stock(),
      categoria: this.categoriaId()!,
      autorSeleccionadoId: this.autorSeleccionadoId(),
      autorNuevoNombre: this.autorNuevoNombre(),
    });
  }
}

import { Component, EventEmitter, HostListener, Input, OnChanges, Output, signal } from '@angular/core';

import { Categoria } from './models/catalogo.model';

export interface FiltrosSeleccionados {
  categoriaIds: number[];
  soloDisponibles: boolean;
}

@Component({
  selector: 'app-filtros-catalogo-modal',
  templateUrl: './filtros-catalogo-modal.component.html',
})
export class FiltrosCatalogoModalComponent implements OnChanges {
  @Input({ required: true }) categorias: Categoria[] = [];
  @Input() categoriaIdsIniciales: number[] = [];
  @Input() soloDisponiblesInicial = false;

  @Output() cerrar = new EventEmitter<void>();
  @Output() aplicar = new EventEmitter<FiltrosSeleccionados>();

  protected readonly categoriaIdsSeleccionadas = signal<Set<number>>(new Set());
  protected readonly soloDisponibles = signal(false);

  ngOnChanges(): void {
    this.categoriaIdsSeleccionadas.set(new Set(this.categoriaIdsIniciales));
    this.soloDisponibles.set(this.soloDisponiblesInicial);
  }

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.cerrar.emit();
  }

  protected alternarCategoria(categoriaId: number, marcado: boolean): void {
    this.categoriaIdsSeleccionadas.update((actual) => {
      const siguiente = new Set(actual);
      if (marcado) {
        siguiente.add(categoriaId);
      } else {
        siguiente.delete(categoriaId);
      }
      return siguiente;
    });
  }

  protected estaSeleccionada(categoriaId: number): boolean {
    return this.categoriaIdsSeleccionadas().has(categoriaId);
  }

  protected alCambiarSoloDisponibles(marcado: boolean): void {
    this.soloDisponibles.set(marcado);
  }

  protected aplicarFiltros(): void {
    this.aplicar.emit({
      categoriaIds: Array.from(this.categoriaIdsSeleccionadas()),
      soloDisponibles: this.soloDisponibles(),
    });
  }
}

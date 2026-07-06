import { Component, ElementRef, EventEmitter, HostListener, Input, Output, inject, signal } from '@angular/core';

export interface AccionMenu {
  etiqueta: string;
  peligro?: boolean;
}

@Component({
  selector: 'app-three-dot-menu',
  templateUrl: './three-dot-menu.component.html',
})
export class ThreeDotMenuComponent {
  @Input({ required: true }) acciones: AccionMenu[] = [];
  @Output() accionSeleccionada = new EventEmitter<number>();

  protected readonly abierto = signal(false);
  private readonly elementRef = inject(ElementRef<HTMLElement>);

  protected alternar(evento: Event): void {
    evento.stopPropagation();
    this.abierto.update((valor) => !valor);
  }

  protected seleccionar(indice: number, evento: Event): void {
    evento.stopPropagation();
    this.abierto.set(false);
    this.accionSeleccionada.emit(indice);
  }

  @HostListener('document:click', ['$event'])
  protected alHacerClicFuera(evento: Event): void {
    if (!this.elementRef.nativeElement.contains(evento.target as Node)) {
      this.abierto.set(false);
    }
  }

  @HostListener('document:keydown.escape')
  protected alPresionarEscape(): void {
    this.abierto.set(false);
  }
}

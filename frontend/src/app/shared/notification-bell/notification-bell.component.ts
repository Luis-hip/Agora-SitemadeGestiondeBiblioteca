import { Component, ElementRef, HostListener, inject, signal } from '@angular/core';

import { NotificacionesService } from '../../core/services/notificaciones.service';

@Component({
  selector: 'app-notification-bell',
  templateUrl: './notification-bell.component.html',
})
export class NotificationBellComponent {
  protected readonly notificacionesService = inject(NotificacionesService);
  private readonly elementRef = inject(ElementRef<HTMLElement>);

  protected readonly abierto = signal(false);

  protected alternar(): void {
    const abrira = !this.abierto();
    this.abierto.set(abrira);
    if (abrira) {
      void this.notificacionesService.cargar();
    }
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

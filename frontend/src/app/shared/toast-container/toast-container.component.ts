import { Component, inject } from '@angular/core';

import { ToastService } from '../../core/services/toast.service';

@Component({
  selector: 'app-toast-container',
  templateUrl: './toast-container.component.html',
})
export class ToastContainerComponent {
  protected readonly toastService = inject(ToastService);

  protected clasesPorTipo(tipo: string): string {
    switch (tipo) {
      case 'exito':
        return 'bg-emerald-50 text-emerald-800 border-emerald-200';
      case 'advertencia':
        return 'bg-amber-50 text-amber-800 border-amber-200';
      default:
        return 'bg-red-50 text-red-800 border-red-200';
    }
  }
}

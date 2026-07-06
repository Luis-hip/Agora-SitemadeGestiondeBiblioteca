import { Component, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { NotificationBellComponent } from '../notification-bell/notification-bell.component';

@Component({
  selector: 'app-nav-bar',
  imports: [RouterLink, NotificationBellComponent],
  templateUrl: './nav-bar.component.html',
})
export class NavBarComponent {
  protected readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  protected cerrarSesion(): void {
    this.authService.cerrarSesion();
    this.router.navigate(['/login']);
  }
}

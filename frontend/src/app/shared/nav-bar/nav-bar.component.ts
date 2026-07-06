import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { urlAvatar } from '../avatar.util';
import { NotificationBellComponent } from '../notification-bell/notification-bell.component';

@Component({
  selector: 'app-nav-bar',
  imports: [RouterLink, RouterLinkActive, NotificationBellComponent],
  templateUrl: './nav-bar.component.html',
})
export class NavBarComponent {
  protected readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  protected urlAvatarActor(): string {
    return urlAvatar(this.authService.actor()?.nombre ?? '');
  }

  protected cerrarSesion(): void {
    this.authService.cerrarSesion();
    this.router.navigate(['/login']);
  }
}

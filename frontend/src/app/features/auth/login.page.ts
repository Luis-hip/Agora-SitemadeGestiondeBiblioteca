import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { ToastService } from '../../core/services/toast.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login.page.html',
})
export class LoginPageComponent {
  private readonly authService = inject(AuthService);
  private readonly toast = inject(ToastService);
  private readonly router = inject(Router);

  protected readonly identificador = signal('');
  protected readonly password = signal('');
  protected readonly enviando = signal(false);
  protected readonly errorInline = signal<string | null>(null);

  protected alEnviarFormulario(evento: Event): void {
    evento.preventDefault();
    void this.enviar();
  }

  protected async enviar(): Promise<void> {
    this.enviando.set(true);
    this.errorInline.set(null);
    try {
      const actor = await this.authService.login(this.identificador(), this.password());
      this.toast.exito('Inicio de sesion exitoso.');
      this.router.navigate([actor.tipoActor === 'USUARIO' ? '/perfil' : '/admin/dashboard']);
    } catch (err) {
      const error = err as HttpErrorResponse;
      this.errorInline.set(error.error?.mensaje ?? 'Correo/usuario o contrasena incorrectos.');
    } finally {
      this.enviando.set(false);
    }
  }
}

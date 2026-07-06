import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { ToastService } from '../../core/services/toast.service';

@Component({
  selector: 'app-registro-page',
  imports: [RouterLink],
  templateUrl: './registro.page.html',
})
export class RegistroPageComponent {
  private readonly authService = inject(AuthService);
  private readonly toast = inject(ToastService);
  private readonly router = inject(Router);

  protected readonly matricula = signal('');
  protected readonly nombre = signal('');
  protected readonly email = signal('');
  protected readonly telefono = signal('');
  protected readonly tipoUsuario = signal<'ESTUDIANTE' | 'PROFESOR'>('ESTUDIANTE');
  protected readonly password = signal('');
  protected readonly passwordConfirmacion = signal('');
  protected readonly enviando = signal(false);
  protected readonly errorInline = signal<string | null>(null);

  protected alEnviarFormulario(evento: Event): void {
    evento.preventDefault();
    void this.enviar();
  }

  protected async enviar(): Promise<void> {
    if (this.password() !== this.passwordConfirmacion()) {
      this.errorInline.set('Las contrasenas no coinciden.');
      return;
    }
    this.enviando.set(true);
    this.errorInline.set(null);
    try {
      await this.authService.registrar({
        matricula: this.matricula(),
        nombre: this.nombre(),
        email: this.email(),
        telefono: this.telefono(),
        tipo_usuario: this.tipoUsuario(),
        password: this.password(),
        password_confirmacion: this.passwordConfirmacion(),
      });
      this.toast.exito('Registro exitoso. Bienvenido a Agora.');
      this.router.navigate(['/perfil']);
    } catch (err) {
      const error = err as HttpErrorResponse;
      this.errorInline.set(error.error?.mensaje ?? 'No se pudo completar el registro.');
    } finally {
      this.enviando.set(false);
    }
  }
}

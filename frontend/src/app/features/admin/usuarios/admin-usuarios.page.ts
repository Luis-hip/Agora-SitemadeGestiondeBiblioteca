import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { ToastService } from '../../../core/services/toast.service';
import { urlAvatar } from '../../../shared/avatar.util';
import { AccionMenu, ThreeDotMenuComponent } from '../../../shared/three-dot-menu/three-dot-menu.component';
import { Usuario } from '../models/admin.model';
import { AdminUsuariosService } from '../services/admin-usuarios.service';

const ACCIONES_FILA: AccionMenu[] = [{ etiqueta: 'Suspender', peligro: true }];

@Component({
  selector: 'app-admin-usuarios-page',
  imports: [ThreeDotMenuComponent],
  templateUrl: './admin-usuarios.page.html',
})
export class AdminUsuariosPageComponent {
  private readonly usuariosService = inject(AdminUsuariosService);
  private readonly toast = inject(ToastService);
  private readonly router = inject(Router);

  protected readonly usuarios = signal<Usuario[]>([]);
  protected readonly cargando = signal(true);
  protected readonly acciones = ACCIONES_FILA;

  constructor() {
    void this.cargarUsuarios();
  }

  protected verDetalle(usuario: Usuario): void {
    this.router.navigate(['/admin/usuarios', usuario.id]);
  }

  protected urlAvatarUsuario(nombre: string): string {
    return urlAvatar(nombre);
  }

  protected async alSeleccionarAccion(usuario: Usuario): Promise<void> {
    try {
      await this.usuariosService.suspender(usuario.id);
      this.toast.exito(`Usuario ${usuario.nombre} suspendido.`);
      await this.cargarUsuarios();
    } catch (err) {
      const error = err as HttpErrorResponse;
      this.toast.error(error.error?.mensaje ?? 'No se pudo suspender al usuario.');
    }
  }

  private async cargarUsuarios(): Promise<void> {
    this.cargando.set(true);
    try {
      this.usuarios.set(await this.usuariosService.listarUsuarios());
    } catch {
      this.toast.error('No se pudo cargar la lista de usuarios.');
    } finally {
      this.cargando.set(false);
    }
  }
}

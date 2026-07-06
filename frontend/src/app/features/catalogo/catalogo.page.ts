import { HttpErrorResponse } from '@angular/common/http';
import { Component, effect, inject, signal } from '@angular/core';

import { ToastService } from '../../core/services/toast.service';
import { LibroDetalleModalComponent } from './libro-detalle-modal.component';
import { Categoria, Libro } from './models/catalogo.model';
import { CatalogoService } from './services/catalogo.service';
import { PrestamoService } from './services/prestamo.service';

@Component({
  selector: 'app-catalogo-page',
  imports: [LibroDetalleModalComponent],
  templateUrl: './catalogo.page.html',
})
export class CatalogoPageComponent {
  private readonly catalogoService = inject(CatalogoService);
  private readonly prestamoService = inject(PrestamoService);
  private readonly toast = inject(ToastService);

  protected readonly libros = signal<Libro[]>([]);
  protected readonly categorias = signal<Categoria[]>([]);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);

  protected readonly categoriaSeleccionada = signal<number | null>(null);
  protected readonly soloDisponibles = signal(false);

  protected readonly libroSeleccionado = signal<Libro | null>(null);
  protected readonly enviandoPrestamo = signal(false);

  protected readonly placeholdersSkeleton = Array.from({ length: 8 });

  constructor() {
    this.catalogoService
      .listarCategorias()
      .then((categorias) => this.categorias.set(categorias))
      .catch(() => this.toast.error('No se pudieron cargar las categorias.'));

    effect(() => {
      const categoriaId = this.categoriaSeleccionada();
      const soloDisponibles = this.soloDisponibles();
      this.cargarLibros(categoriaId, soloDisponibles);
    });
  }

  protected alCambiarCategoria(valor: string): void {
    this.categoriaSeleccionada.set(valor ? Number(valor) : null);
  }

  protected alCambiarSoloDisponibles(marcado: boolean): void {
    this.soloDisponibles.set(marcado);
  }

  protected abrirDetalle(libro: Libro): void {
    this.libroSeleccionado.set(libro);
  }

  protected cerrarDetalle(): void {
    this.libroSeleccionado.set(null);
  }

  protected async confirmarPrestamo(libro: Libro): Promise<void> {
    this.enviandoPrestamo.set(true);
    try {
      await this.prestamoService.solicitarPrestamo(libro.id);
      this.toast.exito(`Prestamo solicitado: ${libro.titulo}`);
      setTimeout(() => this.libroSeleccionado.set(null), 600);
      await this.cargarLibros(this.categoriaSeleccionada(), this.soloDisponibles());
    } catch (err) {
      const error = err as HttpErrorResponse;
      const mensaje = error.error?.mensaje ?? 'No se pudo procesar la solicitud de prestamo.';
      if (error.status === 422) {
        this.toast.advertencia(mensaje);
      } else {
        this.toast.error(mensaje);
      }
    } finally {
      this.enviandoPrestamo.set(false);
    }
  }

  private async cargarLibros(categoriaId: number | null, soloDisponibles: boolean): Promise<void> {
    this.cargando.set(true);
    this.error.set(null);
    try {
      const libros = await this.catalogoService.listarLibros({ categoriaId, soloDisponibles });
      this.libros.set(libros);
    } catch {
      this.error.set('No se pudo cargar el catalogo. Intenta de nuevo mas tarde.');
    } finally {
      this.cargando.set(false);
    }
  }
}

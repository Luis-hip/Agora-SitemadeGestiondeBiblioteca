import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';

import { ToastService } from '../../../core/services/toast.service';
import { BookCoverComponent } from '../../../shared/book-cover/book-cover.component';
import { AccionMenu, ThreeDotMenuComponent } from '../../../shared/three-dot-menu/three-dot-menu.component';
import { Autor, Categoria } from '../../catalogo/models/catalogo.model';
import { CatalogoService } from '../../catalogo/services/catalogo.service';
import { Libro, LibroFormOutput, LibroPayload } from '../models/admin.model';
import { AdminCatalogoService } from '../services/admin-catalogo.service';
import { CategoriaFormModalComponent, CategoriaPayload } from './categoria-form-modal.component';
import { ConfirmarEliminarModalComponent } from './confirmar-eliminar-modal.component';
import { LibroFormModalComponent } from './libro-form-modal.component';

type Pestana = 'libros' | 'categorias';

interface ElementoAEliminar {
  tipo: 'libro' | 'categoria';
  id: number;
  nombre: string;
}

const ACCIONES_FILA: AccionMenu[] = [{ etiqueta: 'Modificar' }, { etiqueta: 'Eliminar', peligro: true }];

@Component({
  selector: 'app-admin-catalogo-page',
  imports: [
    ThreeDotMenuComponent,
    LibroFormModalComponent,
    CategoriaFormModalComponent,
    ConfirmarEliminarModalComponent,
    BookCoverComponent,
  ],
  templateUrl: './admin-catalogo.page.html',
})
export class AdminCatalogoPageComponent {
  private readonly catalogoService = inject(CatalogoService);
  private readonly adminCatalogoService = inject(AdminCatalogoService);
  private readonly toast = inject(ToastService);

  protected readonly pestanaActiva = signal<Pestana>('libros');
  protected readonly libros = signal<Libro[]>([]);
  protected readonly categorias = signal<Categoria[]>([]);
  protected readonly autores = signal<Autor[]>([]);
  protected readonly cargando = signal(true);

  protected readonly acciones = ACCIONES_FILA;

  protected readonly modalLibroAbierto = signal(false);
  protected readonly libroEnEdicion = signal<Libro | null>(null);
  protected readonly guardandoLibro = signal(false);

  protected readonly modalCategoriaAbierto = signal(false);
  protected readonly categoriaEnEdicion = signal<Categoria | null>(null);
  protected readonly guardandoCategoria = signal(false);

  protected readonly elementoAEliminar = signal<ElementoAEliminar | null>(null);
  protected readonly eliminando = signal(false);

  constructor() {
    void this.cargarTodo();
  }

  protected seleccionarPestana(pestana: Pestana): void {
    this.pestanaActiva.set(pestana);
  }

  protected abrirCrearLibro(): void {
    this.libroEnEdicion.set(null);
    this.modalLibroAbierto.set(true);
  }

  protected abrirEditarLibro(libro: Libro): void {
    this.libroEnEdicion.set(libro);
    this.modalLibroAbierto.set(true);
  }

  protected cerrarModalLibro(): void {
    this.modalLibroAbierto.set(false);
  }

  protected async guardarLibro(salida: LibroFormOutput): Promise<void> {
    this.guardandoLibro.set(true);
    try {
      let autorId = salida.autorSeleccionadoId;
      if (salida.autorNuevoNombre.trim()) {
        const nuevoAutor = await this.adminCatalogoService.crearAutor({
          nombre: salida.autorNuevoNombre.trim(),
          nacionalidad: 'No especificada',
        });
        autorId = nuevoAutor.id;
      }
      if (!autorId) {
        this.toast.advertencia('Selecciona un autor existente o escribe uno nuevo.');
        return;
      }

      const payload: LibroPayload = {
        titulo: salida.titulo,
        isbn: salida.isbn,
        fecha_publicacion: salida.fecha_publicacion,
        disponible: salida.disponible,
        stock: salida.stock,
        categoria: salida.categoria,
        autores: [autorId],
      };

      const libro = this.libroEnEdicion();
      if (libro) {
        await this.adminCatalogoService.actualizarLibro(libro.id, payload);
        this.toast.exito('Libro modificado exitosamente.');
      } else {
        await this.adminCatalogoService.crearLibro(payload);
        this.toast.exito('Libro agregado exitosamente.');
      }
      this.modalLibroAbierto.set(false);
      await Promise.all([this.cargarLibros(), this.cargarAutores()]);
    } catch (err) {
      this.mostrarErrorToast(err, 'No se pudo guardar el libro.');
    } finally {
      this.guardandoLibro.set(false);
    }
  }

  protected abrirCrearCategoria(): void {
    this.categoriaEnEdicion.set(null);
    this.modalCategoriaAbierto.set(true);
  }

  protected abrirEditarCategoria(categoria: Categoria): void {
    this.categoriaEnEdicion.set(categoria);
    this.modalCategoriaAbierto.set(true);
  }

  protected cerrarModalCategoria(): void {
    this.modalCategoriaAbierto.set(false);
  }

  protected async guardarCategoria(payload: CategoriaPayload): Promise<void> {
    this.guardandoCategoria.set(true);
    try {
      const categoria = this.categoriaEnEdicion();
      if (categoria) {
        await this.adminCatalogoService.actualizarCategoria(categoria.id, payload);
        this.toast.exito('Categoria modificada exitosamente.');
      } else {
        await this.adminCatalogoService.crearCategoria(payload);
        this.toast.exito('Categoria creada exitosamente.');
      }
      this.modalCategoriaAbierto.set(false);
      await this.cargarCategorias();
    } catch (err) {
      this.mostrarErrorToast(err, 'No se pudo guardar la categoria.');
    } finally {
      this.guardandoCategoria.set(false);
    }
  }

  protected alSeleccionarAccionLibro(libro: Libro, indice: number): void {
    if (indice === 0) {
      this.abrirEditarLibro(libro);
    } else {
      this.elementoAEliminar.set({ tipo: 'libro', id: libro.id, nombre: libro.titulo });
    }
  }

  protected alSeleccionarAccionCategoria(categoria: Categoria, indice: number): void {
    if (indice === 0) {
      this.abrirEditarCategoria(categoria);
    } else {
      this.elementoAEliminar.set({ tipo: 'categoria', id: categoria.id, nombre: categoria.nombre });
    }
  }

  protected cerrarModalEliminar(): void {
    this.elementoAEliminar.set(null);
  }

  protected async confirmarEliminacion(): Promise<void> {
    const elemento = this.elementoAEliminar();
    if (!elemento) {
      return;
    }
    this.eliminando.set(true);
    try {
      if (elemento.tipo === 'libro') {
        await this.adminCatalogoService.eliminarLibro(elemento.id);
        this.toast.exito('Libro eliminado.');
        await this.cargarLibros();
      } else {
        await this.adminCatalogoService.eliminarCategoria(elemento.id);
        this.toast.exito('Categoria eliminada.');
        await this.cargarCategorias();
      }
      this.elementoAEliminar.set(null);
    } catch (err) {
      this.mostrarErrorToast(err, 'No se pudo eliminar el elemento.');
    } finally {
      this.eliminando.set(false);
    }
  }

  private mostrarErrorToast(err: unknown, mensajePorDefecto: string): void {
    const error = err as HttpErrorResponse;
    const mensaje = error.error?.mensaje ?? mensajePorDefecto;
    if (error.status === 422) {
      this.toast.advertencia(mensaje);
    } else {
      this.toast.error(mensaje);
    }
  }

  private async cargarLibros(): Promise<void> {
    this.libros.set(await this.catalogoService.listarLibros());
  }

  private async cargarCategorias(): Promise<void> {
    this.categorias.set(await this.catalogoService.listarCategorias());
  }

  private async cargarAutores(): Promise<void> {
    this.autores.set(await this.catalogoService.listarAutores());
  }

  private async cargarTodo(): Promise<void> {
    this.cargando.set(true);
    try {
      await Promise.all([this.cargarLibros(), this.cargarCategorias(), this.cargarAutores()]);
    } catch {
      this.toast.error('No se pudo cargar el catalogo.');
    } finally {
      this.cargando.set(false);
    }
  }
}

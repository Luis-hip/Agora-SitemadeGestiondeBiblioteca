import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { Autor, Categoria } from '../../catalogo/models/catalogo.model';
import { Libro, LibroPayload } from '../models/admin.model';

@Injectable({ providedIn: 'root' })
export class AdminCatalogoService {
  private readonly http = inject(HttpClient);

  async crearLibro(payload: LibroPayload): Promise<Libro> {
    return firstValueFrom(this.http.post<Libro>(`${API_BASE_URL}/catalogo/libros/`, payload));
  }

  async actualizarLibro(id: number, payload: LibroPayload): Promise<Libro> {
    return firstValueFrom(this.http.patch<Libro>(`${API_BASE_URL}/catalogo/libros/${id}/`, payload));
  }

  async eliminarLibro(id: number): Promise<void> {
    await firstValueFrom(this.http.delete(`${API_BASE_URL}/catalogo/libros/${id}/`));
  }

  async crearCategoria(payload: { nombre: string; descripcion: string }): Promise<Categoria> {
    return firstValueFrom(this.http.post<Categoria>(`${API_BASE_URL}/catalogo/categorias/`, payload));
  }

  async actualizarCategoria(id: number, payload: { nombre: string; descripcion: string }): Promise<Categoria> {
    return firstValueFrom(this.http.patch<Categoria>(`${API_BASE_URL}/catalogo/categorias/${id}/`, payload));
  }

  async eliminarCategoria(id: number): Promise<void> {
    await firstValueFrom(this.http.delete(`${API_BASE_URL}/catalogo/categorias/${id}/`));
  }

  async crearAutor(payload: { nombre: string; nacionalidad: string }): Promise<Autor> {
    return firstValueFrom(this.http.post<Autor>(`${API_BASE_URL}/catalogo/autores/`, payload));
  }
}

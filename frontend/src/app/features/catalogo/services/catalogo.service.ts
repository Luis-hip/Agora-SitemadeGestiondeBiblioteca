import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { API_BASE_URL } from '../../../core/api-base-url';
import { Autor, Categoria, FiltrosCatalogo, Libro } from '../models/catalogo.model';

@Injectable({ providedIn: 'root' })
export class CatalogoService {
  private readonly http = inject(HttpClient);

  async listarLibros(filtros: FiltrosCatalogo = {}): Promise<Libro[]> {
    let params = new HttpParams();
    if (filtros.categoriaIds && filtros.categoriaIds.length > 0) {
      params = params.set('categoria', filtros.categoriaIds.join(','));
    }
    if (filtros.soloDisponibles) {
      params = params.set('disponible', 'true');
    }
    return firstValueFrom(this.http.get<Libro[]>(`${API_BASE_URL}/catalogo/libros/`, { params }));
  }

  async listarCategorias(): Promise<Categoria[]> {
    return firstValueFrom(this.http.get<Categoria[]>(`${API_BASE_URL}/catalogo/categorias/`));
  }

  async listarAutores(): Promise<Autor[]> {
    return firstValueFrom(this.http.get<Autor[]>(`${API_BASE_URL}/catalogo/autores/`));
  }
}

import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { BookCoverComponent } from '../../shared/book-cover/book-cover.component';
import { Libro } from '../catalogo/models/catalogo.model';
import { CatalogoService } from '../catalogo/services/catalogo.service';

@Component({
  selector: 'app-landing-page',
  imports: [RouterLink, BookCoverComponent],
  templateUrl: './landing.page.html',
})
export class LandingPageComponent {
  private readonly catalogoService = inject(CatalogoService);
  protected readonly authService = inject(AuthService);

  protected readonly novedades = signal<Libro[]>([]);

  constructor() {
    this.catalogoService
      .listarLibros({ categoriaIds: [], soloDisponibles: false })
      .then((libros) => this.novedades.set(libros.slice(0, 4)))
      .catch(() => this.novedades.set([]));
  }
}

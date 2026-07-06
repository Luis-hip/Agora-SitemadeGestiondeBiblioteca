import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-admin-layout',
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './admin-layout.component.html',
})
export class AdminLayoutComponent {
  protected readonly modulos = [
    { ruta: 'dashboard', etiqueta: 'Panel de Control' },
    { ruta: 'catalogo', etiqueta: 'Catalogo' },
    { ruta: 'usuarios', etiqueta: 'Usuarios' },
    { ruta: 'ajustes', etiqueta: 'Ajustes' },
  ];
}

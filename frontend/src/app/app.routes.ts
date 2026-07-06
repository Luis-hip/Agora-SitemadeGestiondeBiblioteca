import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'catalogo', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login.page').then((m) => m.LoginPageComponent),
  },
  {
    path: 'catalogo',
    loadComponent: () => import('./features/catalogo/catalogo.page').then((m) => m.CatalogoPageComponent),
  },
  {
    path: 'perfil',
    loadComponent: () => import('./features/perfil/perfil.page').then((m) => m.PerfilPageComponent),
  },
];

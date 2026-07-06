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
  {
    path: 'admin',
    loadComponent: () => import('./features/admin/admin-layout.component').then((m) => m.AdminLayoutComponent),
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/admin/dashboard/admin-dashboard.page').then((m) => m.AdminDashboardPageComponent),
      },
      {
        path: 'catalogo',
        loadComponent: () =>
          import('./features/admin/catalogo/admin-catalogo.page').then((m) => m.AdminCatalogoPageComponent),
      },
      {
        path: 'usuarios',
        loadComponent: () =>
          import('./features/admin/usuarios/admin-usuarios.page').then((m) => m.AdminUsuariosPageComponent),
      },
      {
        path: 'usuarios/:id',
        loadComponent: () =>
          import('./features/admin/usuarios/admin-usuario-detalle.page').then(
            (m) => m.AdminUsuarioDetallePageComponent,
          ),
      },
      {
        path: 'ajustes',
        loadComponent: () =>
          import('./features/admin/ajustes/admin-ajustes.page').then((m) => m.AdminAjustesPageComponent),
      },
    ],
  },
];

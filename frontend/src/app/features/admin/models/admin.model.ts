import { Multa } from '../../../core/models/multa.model';
import { Libro, Prestamo } from '../../catalogo/models/catalogo.model';

export interface UsuarioResumen {
  id: number;
  nombre: string;
  email: string;
}

export interface AdminPrestamo extends Omit<Prestamo, 'usuario'> {
  usuario: UsuarioResumen;
}

export interface AdminMulta extends Omit<Multa, 'prestamo'> {
  prestamo: AdminPrestamo;
}

export interface Devolucion {
  id: number;
  prestamo: AdminPrestamo;
  fecha_devolucion: string;
  condicion: string;
}

export interface DashboardKpis {
  prestamos_activos: number;
  devoluciones_hoy: number;
  multas_pendientes_total: string;
  vencimientos_proximos: number;
}

export interface Dashboard {
  kpis: DashboardKpis;
  actividad_reciente: AdminPrestamo[];
}

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  matricula: string;
  telefono: string;
  estado: 'ACTIVO' | 'SUSPENDIDO';
  tipo_usuario: 'ESTUDIANTE' | 'PROFESOR';
}

export interface UsuarioDetalle {
  usuario: Usuario;
  prestamos_activos: Prestamo[];
  historial_prestamos: Prestamo[];
  multas_pendientes: Multa[];
  multas_pagadas: Multa[];
}

export interface LibroPayload {
  titulo: string;
  isbn: string;
  fecha_publicacion: string;
  disponible: boolean;
  categoria: number;
  autores: number[];
}

export interface LibroFormOutput {
  titulo: string;
  isbn: string;
  fecha_publicacion: string;
  disponible: boolean;
  categoria: number;
  autorSeleccionadoId: number | null;
  autorNuevoNombre: string;
}

export type { Libro };

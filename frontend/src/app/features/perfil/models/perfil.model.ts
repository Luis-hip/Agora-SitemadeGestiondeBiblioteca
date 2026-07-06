import { Prestamo } from '../../catalogo/models/catalogo.model';

export interface UsuarioPerfil {
  id: number;
  nombre: string;
  email: string;
  matricula: string;
  telefono: string;
  estado: 'ACTIVO' | 'SUSPENDIDO';
  tipo_usuario: 'ESTUDIANTE' | 'PROFESOR';
}

export interface Multa {
  id: number;
  prestamo: Prestamo;
  monto: string;
  dias_atraso: number;
  estado: 'PENDIENTE' | 'PAGADA' | 'ANULADA';
  fecha_generacion: string;
  fecha_pago: string | null;
}

export interface Perfil {
  usuario: UsuarioPerfil;
  prestamos_activos: Prestamo[];
  historial_prestamos: Prestamo[];
  multas_pendientes: Multa[];
  multas_pagadas: Multa[];
}

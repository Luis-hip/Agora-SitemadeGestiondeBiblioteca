import { Multa } from '../../../core/models/multa.model';
import { Prestamo } from '../../catalogo/models/catalogo.model';

export type { Multa };

export interface UsuarioPerfil {
  id: number;
  nombre: string;
  email: string;
  matricula: string;
  telefono: string;
  estado: 'ACTIVO' | 'SUSPENDIDO';
  tipo_usuario: 'ESTUDIANTE' | 'PROFESOR';
}

export interface Perfil {
  usuario: UsuarioPerfil;
  prestamos_activos: Prestamo[];
  historial_prestamos: Prestamo[];
  multas_pendientes: Multa[];
  multas_pagadas: Multa[];
}

import { Prestamo } from '../../features/catalogo/models/catalogo.model';

export interface Multa {
  id: number;
  prestamo: Prestamo;
  monto: string;
  dias_atraso: number;
  estado: 'PENDIENTE' | 'PAGADA' | 'ANULADA';
  fecha_generacion: string;
  fecha_pago: string | null;
  justificacion_anulacion: string | null;
}

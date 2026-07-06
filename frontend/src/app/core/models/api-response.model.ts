export interface RespuestaEstandar<T> {
  exito: boolean;
  codigo: number;
  datos: T | null;
  mensaje: string;
  detalle?: string;
}

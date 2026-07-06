const CLASES_POR_ESTADO: Record<string, string> = {
  ACTIVO: 'bg-blue-100 text-blue-700',
  PROXIMO_A_VENCER: 'bg-amber-100 text-amber-700',
  CERRADO: 'bg-stone-100 text-stone-600',
  VENCIDO: 'bg-red-100 text-red-700',
  PENDIENTE: 'bg-orange-100 text-orange-800',
  PAGADA: 'bg-emerald-100 text-emerald-700',
  ANULADA: 'bg-stone-100 text-stone-500',
  SUSPENDIDO: 'bg-red-100 text-red-700',
};

export function clasesBadgeEstado(estado: string): string {
  return CLASES_POR_ESTADO[estado] ?? 'bg-stone-100 text-stone-600';
}

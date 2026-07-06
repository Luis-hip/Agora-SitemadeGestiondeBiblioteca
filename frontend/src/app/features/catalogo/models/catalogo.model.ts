export interface Autor {
  id: number;
  nombre: string;
  nacionalidad: string;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}

export interface Libro {
  id: number;
  titulo: string;
  isbn: string;
  fecha_publicacion: string;
  disponible: boolean;
  categoria: Categoria;
  autores: Autor[];
}

export interface Prestamo {
  id: number;
  usuario: number;
  bibliotecario: number | null;
  libro: Libro;
  fecha_inicio: string;
  fecha_dev_esperada: string;
  estado: string;
}

export interface FiltrosCatalogo {
  categoriaIds?: number[];
  soloDisponibles?: boolean;
}

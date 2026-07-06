export type TipoActor = 'USUARIO' | 'BIBLIOTECARIO';
export type Rol = 'ESTUDIANTE' | 'PROFESOR' | 'BIBLIOTECARIO';

export interface ActorAutenticado {
  id: number;
  nombre: string;
  rol: Rol;
  tipoActor: TipoActor;
}

export interface TokensRespuesta {
  access: string;
  refresh: string;
  actor: {
    id: number;
    nombre: string;
    rol: string;
    tipo_actor?: string;
    email?: string;
  };
}

export interface RegistroPayload {
  matricula: string;
  nombre: string;
  email: string;
  telefono: string;
  tipo_usuario: 'ESTUDIANTE' | 'PROFESOR';
  password: string;
  password_confirmacion: string;
}

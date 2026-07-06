export function urlAvatar(nombre: string): string {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(nombre)}&background=random`;
}

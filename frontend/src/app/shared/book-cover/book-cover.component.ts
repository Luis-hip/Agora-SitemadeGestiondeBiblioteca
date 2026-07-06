import { Component, Input, OnChanges, signal } from '@angular/core';

@Component({
  selector: 'app-book-cover',
  templateUrl: './book-cover.component.html',
})
export class BookCoverComponent implements OnChanges {
  @Input({ required: true }) isbn!: string;
  @Input({ required: true }) titulo!: string;

  protected readonly sinPortada = signal(false);

  protected get urlPortada(): string {
    const isbnLimpio = this.isbn.replace(/[^0-9Xx]/g, '');
    return `https://covers.openlibrary.org/b/isbn/${isbnLimpio}-M.jpg`;
  }

  ngOnChanges(): void {
    this.sinPortada.set(false);
  }

  protected alFallarCarga(): void {
    this.sinPortada.set(true);
  }

  protected alCargar(evento: Event): void {
    const img = evento.target as HTMLImageElement;
    // OpenLibrary responde con una imagen de 1x1 cuando no existe portada para el ISBN.
    if (img.naturalWidth <= 1) {
      this.sinPortada.set(true);
    }
  }
}

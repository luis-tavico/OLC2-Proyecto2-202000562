export class Tab {
    ruta: string;
    nombre: string;
    contenido_anterior: string;
    contenido_actual: string;

    constructor(ruta: string, nombre: string, contenido_atnerior: string, contenido_actual: string) {
        this.ruta = ruta;
        this.nombre = nombre;
        this.contenido_anterior = contenido_atnerior;
        this.contenido_actual = contenido_actual;
    }
}
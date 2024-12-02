function numeroLetras(Valor, Moneda) {
    const unidades = ["", "UNO", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"];
    const decenas = ["", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"];
    const especiales = ["ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"];
    const centenas = ["", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"];

    Valor = Math.round(Valor * 100) / 100;
    const cantidad = Math.floor(Valor);
    const centavos = Math.round((Valor - cantidad) * 100);

    function convertirBloque(num) {
        let bloque = "";

        const tercerDigito = Math.floor(num / 100);
        const segundoDigito = Math.floor((num % 100) / 10);
        const primerDigito = num % 10;

        if (tercerDigito > 0) {
            bloque += (num === 100) ? "CIEN" : centenas[tercerDigito] + " ";
        }

        if (segundoDigito > 1) {
            bloque += decenas[segundoDigito] + " ";
            if (primerDigito > 0) {
                bloque += "Y " + unidades[primerDigito];
            }
        } else if (segundoDigito === 1 && primerDigito > 0) {
            bloque += especiales[primerDigito - 1];
        } else if (segundoDigito === 1 && primerDigito === 0) {
            bloque += decenas[segundoDigito];
        } else {
            bloque += unidades[primerDigito];
        }

        return bloque.trim();
    }

    let letras = "";
    if (cantidad === 0) {
        letras = "CERO";
    } else {
        let numeroBloques = 0;
        let numero = cantidad;

        do {
            const bloque = numero % 1000;
            if (bloque > 0) {
                const bloqueTexto = convertirBloque(bloque);
                if (numeroBloques === 1 && bloque === 1) {
                    letras = "MIL " + letras;
                } else {
                    letras = bloqueTexto + " " + (numeroBloques === 1 ? "MIL" : (numeroBloques === 2 ? "MILLONES" : "")) + " " + letras;
                }
            }
            numero = Math.floor(numero / 1000);
            numeroBloques++;
        } while (numero > 0);
    }

    // Ajuste en el formato de la moneda
    if (Moneda === "DÓLARES AMERICANOS") {
        letras += " Y " + centavos.toString().padStart(2, "0") + "/100 DÓLARES AMERICANOS";
    } else if (Moneda === "SOL" || Moneda === "SOLES") {
        letras += " Y " + centavos.toString().padStart(2, "0") + "/100 " + (cantidad === 1 ? "SOL" : "SOLES");
    }

    return letras.trim();
}

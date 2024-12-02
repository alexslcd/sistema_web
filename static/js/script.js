document.addEventListener("DOMContentLoaded", function() {
    const inputVendedor = document.getElementById("seleccionarVendedor");
    const sugerenciasDiv = document.getElementById("sugerenciasVendedores");

    inputVendedor.addEventListener("input", function() {
        const query = inputVendedor.value;

        if (query.length > 2) {  // Solo buscar si el término de búsqueda tiene más de 2 caracteres
            fetch(`/buscar_vendedores?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    console.log("Datos recibidos:", data);  // Verifica los datos recibidos
                    sugerenciasDiv.innerHTML = "";  // Limpiar las sugerencias previas
                    if (data.length > 0) {
                        data.forEach(vendedor => {
                            const item = document.createElement("a");
                            item.href = "#";
                            item.className = "list-group-item list-group-item-action";
                            item.textContent = vendedor.nombre;
                            item.dataset.id = vendedor.id;  // Guardar el ID del vendedor en un atributo data
                            item.addEventListener("click", function() {
                                inputVendedor.value = vendedor.nombre;
                                sugerenciasDiv.innerHTML = "";
                                // Aquí puedes hacer algo con el ID del vendedor si es necesario
                                console.log("Vendedor seleccionado ID:", vendedor.id);
                            });
                            sugerenciasDiv.appendChild(item);
                        });
                    } else {
                        sugerenciasDiv.innerHTML = "<p class='list-group-item'>No se encontraron resultados</p>";
                    }
                })
                .catch(error => {
                    console.error("Error al buscar vendedores:", error);
                });
        } else {
            sugerenciasDiv.innerHTML = "";  // Limpiar las sugerencias si la consulta es demasiado corta
        }
    });

    document.addEventListener("click", function(event) {
        if (!inputVendedor.contains(event.target) && !sugerenciasDiv.contains(event.target)) {
            sugerenciasDiv.innerHTML = "";  // Limpiar las sugerencias si se hace clic fuera del campo de búsqueda
        }
    });
});


//buscar cliente:
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("botonBuscarCliente").addEventListener("click", function() {
        const ruc = document.getElementById("cod_cliente").value;
        if (ruc) {
            fetch(`/buscar_cliente?ruc=${encodeURIComponent(ruc)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error); // Muestra un mensaje de error si no se encontraron datos
                        return;
                    }

                    // Actualizar los campos del formulario con los datos del cliente
                    document.getElementById("id_social").value = data.id_social || ''; // Asignar razon_social
                    document.getElementById("direccion_empresa").value = data.direccion_empresa || '';
                    document.getElementById("distrito").value = data.distrito || '';
                    document.getElementById("ciudad").value = data.ciudad || 'LIMA'; // Valor por defecto
                    document.getElementById("telefono_empresa").value = data.telefono_empresa || '';
                    document.getElementById("aval").value = data.aval || '';
                    document.getElementById("direccion_aval").value = data.direccion_aval || '';
                    document.getElementById("distrito_aval").value = data.distrito_aval || '';
                    document.getElementById("celular").value = data.celular || '';
                    document.getElementById("dni").value = data.dni || '';
                })
                .catch(error => {
                    console.error("Error al buscar el cliente:", error);
                    alert("Hubo un error al buscar el cliente. Por favor, inténtelo de nuevo.");
                });
        } else {
            alert("Por favor, ingrese un RUC.");
        }
    });
});


// buscar cliente

//registrar cliente
function registrarCliente() {
    const clienteData = {
        cod_cliente: document.getElementById("cod_cliente").value,
        razon_social: document.getElementById("id_social").value,
        domicilio: document.getElementById("direccion_empresa").value,
        localidad: document.getElementById("distrito").value,
        telefono: document.getElementById("telefono_empresa").value,
        contacto: document.getElementById("aval").value,
        celular: document.getElementById("celular").value,
        dni: document.getElementById("dni").value
    };

    fetch('/registrar_cliente', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(clienteData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cliente registrado con éxito");
            // Opcional: resetear el formulario o redirigir a otra página
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error al registrar el cliente:", error);
        alert("Hubo un error al registrar el cliente. Por favor, inténtelo de nuevo.");
    });
}

//registrar cliente
//guardar letras



//guardar letras


//borrar datos modal letras
// Función para limpiar ciertos inputs
function limpiarCiertosInputs() {
    // Limpia los inputs específicos
    document.getElementById("numero_boleta").value = "";
    document.getElementById("ref_giro").value = "";
    document.getElementById("fecha_giro").value = "";
    document.getElementById("fecha_vence").value = "";
    document.getElementById("dias_credito").value = "";
    document.getElementById("seleccionarVendedor").value = "";
    document.getElementById("importe").value = "";
    document.getElementById("importeLetras").value = "";
}

// Función para limpiar los demás inputs
function limpiarOtrosInputs() {
    // Limpia los demás inputs
    document.getElementById("cod_cliente").value = "";
    document.getElementById("id_social").value = "";
    document.getElementById("direccion_empresa").value = "";
    document.getElementById("distrito").value = "";
    document.getElementById("telefono_empresa").value = "";
    document.getElementById("aval").value = "";
    document.getElementById("direccion_aval").value = "";
    document.getElementById("distrito_aval").value = "";
    document.getElementById("celular").value = "";
    document.getElementById("dni").value = "";
}

//borrar datos modal letras


//letra para modificar

// Función para manejar la respuesta de la búsqueda
function manejarRespuesta(data) {
    console.log('Datos recibidos del servidor:', data); // Verifica qué datos se están recibiendo

    if (data.success) {
        cargarDatosModal(data.letra); // Llama a la función para llenar el modal
    } else {
        alert('No se encontró la letra o hubo un error.');
    }
}

// Función para enviar una solicitud AJAX
function cargarDatosModal(datos) {
    console.log('Datos a cargar en el modal:', datos); // Verifica los datos que se están cargando

    document.getElementById('numero_boleta_oculto').value = datos.numero_boleta || '';
    document.getElementById('ref_giro_nuevo').value = datos.ref_giro || '';
    document.getElementById('fecha_giro_nueva').value = datos.fecha_giro || '';
    document.getElementById('fecha_vencimiento_nueva').value = datos.fecha_vence || '';
    document.getElementById('importe_nuevo').value = datos.importe || '';
    document.getElementById('codigo_cliente_nuevo').value = datos.cod_cliente || '';
    document.getElementById('razon_social_nueva').value = datos.razon_social || '';
    document.getElementById('moneda_nueva').value = datos.moneda || '';
    document.getElementById('tipo_producto_nuevo').value = datos.tipo_producto || '';
    document.getElementById('cliente_vendedor_nuevo').value = datos.cliente_vendedor || '';
    document.getElementById('estado').value = datos.estado || '';


}


function obtenerDatosLetra() {
    var numeroBoleta = document.getElementById('numero_boleta_buscar').value;
    
    fetch('/buscar_letra/' + numeroBoleta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    
    .then(response => response.json())
    .then(data => manejarRespuesta(data))
    .catch(error => console.error('Error:', error));
}


//CAMBIADO
// Función para manejar la respuesta de la búsqueda de la letra
function manejarRespuesta(data) {
    console.log('Datos recibidos del servidor:', data);

    if (data.success) {
        cargarDatosModal(data.letra); // Llena el modal con los datos
        
        // Verificar el estado de la letra (convertir a mayúsculas para evitar problemas con minúsculas)
        let estadoLetra = data.letra.estado.toUpperCase();
        console.log(estadoLetra);
        //LO LLAMARE DESDE AQUI 

        if (estadoLetra === 'CANCELADA' || estadoLetra === 'ANULADA' || estadoLetra === 'ANULADO') {
            bloquearCamposFormulario();  // Bloquear campos si está CANCELADA o ANULADA
            alert(`La letra está ${estadoLetra} y no se pueden modificar los datos.`);
            
        } else {
            habilitarCamposFormulario();  // Habilitar campos si no está CANCELADA o ANULADA
        }

        $('#registroLetraModal').modal('show'); // Muestra el modal
    } else {
        alert('No se encontró la letra o hubo un error.');
    }
}

// Función para bloquear los campos del formulario
function bloquearCamposFormulario() {
    const campos = document.querySelectorAll('#registroLetraModal input, #registroLetraModal select');
    campos.forEach(campo => {
        // No bloquear el campo de número de boleta (campo de búsqueda y oculto)
        if (campo.id !== 'numero_boleta_buscar' && campo.id !== 'numero_boleta_oculto') {
            campo.disabled = true;  // Bloquea los campos
        }
    });
}


// Función para habilitar los campos del formulario
function habilitarCamposFormulario() {
    const campos = document.querySelectorAll('#registroLetraModal input, #registroLetraModal select');
     
    campos.forEach(campo => campo.disabled = false);  // Habilita los campos
}



function guardarLetra() {
    const letraData = {
        numero_boleta: document.getElementById("numero_boleta").value,
        ref_giro: document.getElementById("ref_giro").value,
        fecha_giro: document.getElementById("fecha_giro").value,
        fecha_vence: document.getElementById("fecha_vence").value,
        importe: document.getElementById("importe").value,
        cod_cliente: document.getElementById("cod_cliente").value,
        razon_social: document.getElementById("id_social").value,
        moneda: document.getElementById("moneda").value,
        tipo_producto: document.getElementById("tipo_producto").value,
        cliente_vendedor: document.getElementById("seleccionarVendedor").value,
        banco:document.getElementById("banco").value
    };

    fetch('/guardar_letra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(letraData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Letra registrada con éxito");


            //LLAMA A LOS DOS BOTONES PARA LIMPIAR Y REGISTRAR UNO NUEVO
            limpiarCiertosInputs();
            limpiarOtrosInputs();

            // Opcional: resetear el formulario o redirigir a otra página
        } else {
            alert('Rellene todos los campos del RUC y de la Letra');
            // alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error al registrar la letra:", error);
        alert("Hubo un error al registrar la letra. Por favor, inténtelo de nuevo.");
    });
}




function guardarDosLetras() {
    const letraData = {
        numero_boleta: document.getElementById("numero_boleta_buscar_1").value,
        ref_giro: document.getElementById("ref_giro").value,
        fecha_giro: document.getElementById("fecha_giro").value,
        fecha_vence: document.getElementById("fecha_vence").value,
        importe: document.getElementById("importe_nuevo_1").value,
        cod_cliente: document.getElementById("cod_cliente").value,
        razon_social: document.getElementById("id_social").value,
        moneda: document.getElementById("moneda").value,
        tipo_producto: document.getElementById("tipo_producto").value,
        cliente_vendedor: document.getElementById("seleccionarVendedor").value,
        banco: document.getElementById("banco").value
    };

    const letraData2 = {
        numero_boleta: document.getElementById("numero_boleta_buscar_2").value,
        ref_giro: document.getElementById("ref_giro").value,
        fecha_giro: document.getElementById("fecha_giro").value,
        fecha_vence: document.getElementById("fecha_vence").value,
        importe: document.getElementById("importe_nuevo_2").value,
        cod_cliente: document.getElementById("cod_cliente").value,
        razon_social: document.getElementById("id_social").value,
        moneda: document.getElementById("moneda").value,
        tipo_producto: document.getElementById("tipo_producto").value,
        cliente_vendedor: document.getElementById("seleccionarVendedor").value,
        banco: document.getElementById("banco").value
    };

    // Aquí combinamos ambos objetos dentro de un solo objeto
    const dataToSend = {
        letraData1: letraData,
        letraData2: letraData2
    };

    fetch('/guardar_dos_letras', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)  // Enviamos el objeto combinado
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Letras registradas con éxito");

            // Llama a los botones para limpiar y registrar uno nuevo
            limpiarCiertosInputs();
            limpiarOtrosInputs();

            // Opcional: resetear el formulario o redirigir a otra página
        } else {
            alert('Rellene todos los campos del RUC y de la Letra');
        }
    })
    .catch(error => {
        console.error("Error al registrar las letras:", error);
        alert("Hubo un error al registrar las letras. Por favor, inténtelo de nuevo.");
    });
}

function toggleView(event) {
    event.preventDefault();  // Evita el comportamiento predeterminado del botón

    var tablaContainer = document.getElementById('tabla-container');
    if (tablaContainer.style.display === 'none' || tablaContainer.style.display === '') {
        tablaContainer.style.display = 'block';
    } else {
        tablaContainer.style.display = 'none';
    }
}

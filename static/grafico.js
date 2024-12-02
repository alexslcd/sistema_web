document.addEventListener('DOMContentLoaded', function () {
    // Llamada a la API para obtener datos del servidor Flask
    fetch('/datos_grafico')
        .then(response => response.json())
        .then(data => {
            // Crear el gráfico con ECharts
            var myChart = echarts.init(document.getElementById('grafico'));

            var option = {
                title: {
                    text: 'Gráfico de Energía y Total ',
                },
                legend: {
                    data: ['Energía', 'Total'],
                },
                xAxis: {
                    type: 'category',
                    data: data.fechas.slice(-3), // Mostrar solo las últimas 3 fechas
                },
                yAxis: {
                    type: 'value',
                },
                series: [{
                    name: 'Energía',
                    data: data.energia.slice(-3), // Mostrar solo los últimos 3 valores de energía
                    type: 'line',
                }, {
                    name: 'Total',
                    data: data.total.slice(-3), // Mostrar solo los últimos 3 valores totales
                    type: 'line',
                }],
            };

            myChart.setOption(option);
        })
        .catch(error => console.error('Error al obtener datos:', error));
});

import math
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_login import LoginManager
import pymysql
from decimal import Decimal
from datetime import datetime 

             #descarga excel
from flask import send_file    #descarga excel
app = Flask(__name__)
from conexion import obtener_conexion_cursor
from login import login_bp
app = Flask(__name__)
app.secret_key = '@lexito'

app.register_blueprint(login_bp)


@app.route('/index')
def index():
    
    if not session.get('logged_in'):
        print("Usuario no autenticado. Redirigiendo al login.")
        return redirect(url_for('login.login'))  
   
    print("Usuario autenticado. Mostrando página principal.")
    return render_template('index.html')


@app.route('/')
def home():
    return redirect(url_for('login.login'))

@app.route('/logout', methods=['POST'])
def logout():
 
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Ruta para guardar la fecha en la base de datos
@app.route('/guardar_banco_fecha_multiples', methods=['POST'])
def guardar_banco_fecha_multiples():
    try:
        # Obtener los datos enviados desde el cliente
        data = request.json

        # Extraer los datos del objeto JSON
        banco_cobro = data.get('bancoCobro')
        fecha_entrega_banco = data.get('fechaEntregaBanco')
        numeros_letra = data.get('numerosLetra')

      
        db, cursor = obtener_conexion_cursor() 

        
        for numero_letra in numeros_letra:
            query = "UPDATE letras SET fecha_banco = %s, banco = %s WHERE numero_boleta = %s"
            cursor.execute(query, (fecha_entrega_banco, banco_cobro, numero_letra))

        # Commit de los cambios en la base de datos
        db.commit()

        # Ejemplo de respuesta exitosa
        response = {'message': 'Los datos se guardaron correctamente en la base de datos.'}
        return jsonify(response), 200

    except Exception as e:
        # En caso de error, devolver un mensaje de error
        print(f"Error: {e}")
        response = {'message': 'Error al guardar los datos en la base de datos.'}
        return jsonify(response), 500

    finally:
        # Cerrar la conexión a la base de datos
        db.close()

@app.route('/guardar_numero_unico', methods=['POST'])
def guardar_numero_unico():
    try:
        # Obtener los datos enviados desde el cliente
        data = request.json

        # Extraer los datos del objeto JSON
        numero_unico = data.get('numeroUnico')
        numeros_letra = data.get('numerosLetra')

        # Conexión a la base de datos
        db, cursor = obtener_conexion_cursor()

        # Actualizar el número único en la base de datos para las filas correspondientes
        for numero_letra in numeros_letra:
            query = "UPDATE letras SET numero_unico = %s WHERE numero_boleta = %s"
            cursor.execute(query, (numero_unico, numero_letra))

        # Confirmar los cambios en la base de datos
        db.commit()

        # Respuesta exitosa
        response = {'message': 'El número único se actualizó correctamente en la base de datos.'}
        return jsonify(response), 200

    except Exception as e:
        # En caso de error, devolver un mensaje de error
        print(f"Error: {e}")
        response = {'message': 'Error al actualizar el número único en la base de datos.'}
        return jsonify(response), 500

    finally:
        # Cerrar la conexión a la base de datos
        db.close()


# Ruta para guardar el estado y el banco de la letra
@app.route('/guardar_estado_letra_multiples', methods=['POST'])
def guardar_estado_letra_multiples():
    try:
        # Obtener los datos enviados desde el cliente
        data = request.json

        # Extraer los datos del objeto JSON
        estado_letra = data.get('estadoLetra')
        numeros_letra = data.get('numerosLetra')

        # Aquí debes agregar la lógica para conectarte a la base de datos
        # y ejecutar la consulta SQL para actualizar las filas correspondientes

        db, cursor = obtener_conexion_cursor()  # Suponiendo que esta función establece la conexión y devuelve el cursor

        # Iterar sobre los números de letra y actualizar las filas en la base de datos
        for numero_letra in numeros_letra:
            query = "UPDATE letras SET estado = %s WHERE numero_boleta = %s"
            cursor.execute(query, (estado_letra, numero_letra))

        # Commit de los cambios en la base de datos
        db.commit()

        # Ejemplo de respuesta exitosa
        response = {'message': 'Los datos se guardaron correctamente en la base de datos.'}
        return jsonify(response), 200

    except Exception as e:
        # En caso de error, devolver un mensaje de error
        print(f"Error: {e}")
        response = {'message': 'Error al guardar los datos en la base de datos.'}
        return jsonify(response), 500

    finally:
        # Cerrar la conexión a la base de datos
        db.close()



#nuevo actualizacion
#buscar letra para modificacion y guardar cambios
@app.route('/buscar_letra/<numero_boleta>', methods=['POST'])
def buscar_letra(numero_boleta):
    print(f"Número de boleta recibido: {numero_boleta}")

    conexion, cursor = obtener_conexion_cursor()
    try:
        cursor.execute("""
            SELECT numero_boleta, ref_giro, fecha_giro, fecha_vence, importe, cod_cliente, razon_social, moneda, tipo_producto, cliente_vendedor,estado
            FROM letras
            WHERE numero_boleta = %s
        """, (numero_boleta,))
        
        letra = cursor.fetchone()
        print(f"Datos recuperados de la base de datos: {letra}")

        if letra:
            resultado = {
                'success': True,
                'letra': {
                    'numero_boleta': letra[0],
                    'ref_giro': letra[1],
                    'fecha_giro': letra[2].strftime('%Y-%m-%d') if letra[2] else None,
                    'fecha_vence': letra[3].strftime('%Y-%m-%d') if letra[3] else None,
                    'importe': float(letra[4]),  # Convertir a float
                    'cod_cliente': letra[5],
                    'razon_social': letra[6],
                    'moneda': letra[7],
                    'tipo_producto': letra[8],
                    'cliente_vendedor': letra[9],
                    'estado':letra[10]
                    
                }
            }
        else:
            resultado = {'success': False, 'message': 'Letra no encontrada'}

    except Exception as e:
        print(f"Error al buscar letra: {e}")
        resultado = {'success': False, 'message': 'Error al buscar la letra'}
    finally:
        cursor.close()
        conexion.close()

    return jsonify(resultado)



@app.route('/guardar_cambios', methods=['POST'])
def guardar_cambios():
    data = request.form
    print("Datos recibidos para guardar:", data)
    
    # Extraer datos del formulario con los nombres correctos
    fecha_giro = data.get('fecha_giro_nueva')
    fecha_vence = data.get('fecha_vencimiento_nueva')
    importe = data.get('importe_nuevo')
    ref_giro = data.get('ref_giro_nuevo')
    cod_cliente = data.get('codigo_cliente_nuevo')
    razon_social = data.get('razon_social_nueva')
    moneda = data.get('moneda_nueva')
    tipo_producto = data.get('tipo_producto_nuevo')
    cliente_vendedor = data.get('cliente_vendedor_nuevo')
    numero_boleta = data.get('numero_boleta')  # Este es el campo oculto

    # Validar que las claves existan
    if not (fecha_giro and fecha_vence and importe and ref_giro and cod_cliente and razon_social and moneda and tipo_producto and cliente_vendedor and numero_boleta):
        return jsonify({'message': 'Hubo un error al guardar la letra'}), 400

    try:
        fecha_giro = datetime.strptime(fecha_giro, '%Y-%m-%d').date()
        fecha_vence = datetime.strptime(fecha_vence, '%Y-%m-%d').date()
        importe = float(importe)
    except ValueError:
        return jsonify({'message': 'Hubo un error al guardar la letra'}), 400

    # Conexión a la base de datos
    conn, cursor = obtener_conexion_cursor()
    try:
        sql = """
            UPDATE letras
            SET ref_giro = %s,
                fecha_giro = %s,
                fecha_vence = %s,
                importe = %s,
                cod_cliente = %s,
                razon_social = %s,
                moneda = %s,
                tipo_producto = %s,
                cliente_vendedor = %s
            WHERE numero_boleta = %s
        """
        cursor.execute(sql, (
            ref_giro,
            fecha_giro,
            fecha_vence,
            importe,
            cod_cliente,
            razon_social,
            moneda,
            tipo_producto,
            cliente_vendedor,
            numero_boleta
        ))
        conn.commit()
        return jsonify({'message': 'La letra se guardó correctamente'})
    except Exception:
        return jsonify({'message': 'Hubo un error al guardar la letra'}), 500
    finally:
        cursor.close()
        conn.close()
#buscar letra para modificacion y guardar cambios


#guardar numero unico masivo
@app.route('/filtrar_letras', methods=['GET'])
def filtrar_letras():
    fecha_banco = request.args.get('fecha_banco')
    
    conn, cursor = obtener_conexion_cursor()
    try:
        if fecha_banco:
            sql = """
                SELECT numero_boleta, fecha_banco, numero_unico
                FROM letras
                WHERE fecha_banco = %s
            """
            cursor.execute(sql, (fecha_banco,))
            letras = cursor.fetchall()
            
            return jsonify({
                'success': True, 
                'letras': [{'numero_boleta': letra[0], 'fecha_banco': letra[1], 'numero_unico': letra[2]} for letra in letras]
            })
        else:
            return jsonify({'success': False, 'message': 'Fecha de banco no proporcionada'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error al filtrar las letras'})
    finally:
        cursor.close()
        conn.close()
        
@app.route('/guardar_codigos', methods=['POST'])
def guardar_codigos():
    data = request.get_json()
    letras = data.get('letras', [])
    
    conn, cursor = obtener_conexion_cursor()
    try:
        for letra in letras:
            numero_boleta = letra.get('numero_boleta')
            numero_unico = letra.get('numero_unico')
            
            sql = """
                UPDATE letras
                SET numero_unico = %s
                WHERE numero_boleta = %s
            """
            cursor.execute(sql, (numero_unico, numero_boleta))
        
        conn.commit()
        return jsonify({'success': True, 'message': 'Códigos únicos guardados exitosamente.'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'guardar los códigos únicos.'})
    finally:
        cursor.close()
        conn.close()
#guardar numero unico masivo
# Ruta para guardar la fecha en la base de datos

#nueva actualizacion

#busqueda de vendedor:
@app.route('/buscar_vendedores', methods=['GET'])
def buscar_vendedores():
    query = request.args.get('query', '')
    vendedores = obtener_vendedores(query)
    return jsonify(vendedores)

def obtener_vendedores(query):
    conexion, cursor = obtener_conexion_cursor()
    try:
        consulta = "SELECT * FROM vendedores WHERE nombre LIKE %s"
        cursor.execute(consulta, ('%' + query + '%',))
        resultados = cursor.fetchall()
        # Convertir resultados a una lista de diccionarios
        resultados_dict = [{'id': r[0], 'nombre': r[1]} for r in resultados]
        return resultados_dict
    finally:
        cursor.close()
        conexion.close()

 #busqueda de vendedor:   

# Ruta para guardar la fecha en la base de datos
@app.route('/buscar_letras', methods=['POST'])
def buscar_letras():
    resultados_json = []
    try:
        db, cursor = obtener_conexion_cursor()

        # Obtener los parámetros del formulario
        letra = request.form.get('numeroBoleta')
        ruc = request.form.get('ruc')
        razon_social = request.form.get('razonSocial')
        fecha_desde = request.form.get('fechaDesde')
        fecha_hasta = request.form.get('fechaHasta')
        estado_letra = request.form.get('estadoLetra')
        tipo_fecha = request.form.get('tipoFecha')  # Selección del tipo de fecha

        # Depuración de valores recibidos
        print(f"Fecha Desde: {fecha_desde}")
        print(f"Fecha Hasta: {fecha_hasta}")
        print(f"Tipo de fecha seleccionado: {tipo_fecha}")

        # Asegurarse de que las fechas estén en formato correcto 'YYYY-MM-DD'
        if fecha_desde and fecha_hasta:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').strftime('%Y-%m-%d')
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'}), 400

        # Construcción de la consulta SQL
        query = """
        SELECT numero_boleta, cod_cliente, razon_social, fecha_giro, fecha_vence, importe, moneda, banco, 
               numero_unico, estado, tipo_producto, ref_giro, fecha_banco, cliente_vendedor 
        FROM letras WHERE TRUE
        """
        params = []

        # Agregar condiciones basadas en los parámetros recibidos
        if letra:
            query += " AND numero_boleta LIKE %s"
            params.append(f"%{letra}%")

        if ruc:
            query += " AND cod_cliente LIKE %s"
            params.append(f"%{ruc}%")

        if razon_social:
            query += " AND razon_social LIKE %s"
            params.append(f"%{razon_social}%")

        if estado_letra:
            query += " AND estado LIKE %s"
            params.append(f"%{estado_letra}%")

        # Aplicar la condición de fechas dependiendo del tipo seleccionado
        if fecha_desde and fecha_hasta:
            if tipo_fecha == 'vencimiento':
                query += " AND fecha_vence BETWEEN %s AND %s"
            elif tipo_fecha == 'giro':
                query += " AND fecha_giro BETWEEN %s AND %s"
            params.extend([fecha_desde, fecha_hasta])

        # Depuración de consulta y parámetros
        print(f"Query: {query}")
        print(f"Params: {params}")

        # Ejecutar la consulta con los parámetros, asegurarse de pasar los parámetros como tupla
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()

        # Procesar los resultados
        for resultado in resultados:
            resultados_json.append({
                'numero_boleta': resultado[0],
                'cod_cliente': resultado[1],
                'razon_social': resultado[2],
                'fecha_giro': str(resultado[3]),
                'fecha_vence': str(resultado[4]),
                'importe': resultado[5],
                'moneda': resultado[6],
                'banco': resultado[7],
                'numero_unico': resultado[8],
                'estado': resultado[9],
                'tipo_producto': resultado[10],
                'ref_giro': resultado[11],
                'fecha_banco': str(resultado[12]),
                'cliente_vendedor': resultado[13]
            })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Ocurrió un error en la búsqueda de letras.'}), 500

    finally:
        db.close()

    return jsonify(resultados_json)


# letra nueva  /vendedor
#buscar cliente
@app.route('/buscar_cliente', methods=['GET'])
def buscar_cliente():
    ruc = request.args.get('ruc')
    if not ruc:
        return jsonify({'error': 'RUC no proporcionado'}), 400

    conexion, cursor = obtener_conexion_cursor()

    try:
        # Modificar la consulta para incluir razon_social y otras columnas
        cursor.execute("""
            SELECT razon_social, domicilio, localidad, telefono, contacto, domicilio, localidad, celular, dni
            FROM cliente
            WHERE cod_cliente = %s
        """, (ruc,))
        
        cliente = cursor.fetchone()
        if cliente:
            resultado = {
                'id_social': cliente[0],  # razon_social
                'direccion_empresa': cliente[1],  # domicilio
                'distrito': cliente[2],  # localidad
                'telefono_empresa': cliente[3],  # telefono
                'aval': cliente[4],  # contacto
                'direccion_aval': cliente[5],  # domicilio
                'distrito_aval': cliente[6],  # localidad
                'celular': cliente[7],  # celular
                'dni': cliente[8]  # dni
            }
            return jsonify(resultado)
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500
    finally:
        cursor.close()
        conexion.close()
# buscar cliente

#registrar cliente
@app.route('/registrar_cliente', methods=['POST'])
def registrar_cliente():
    data = request.json

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    conexion, cursor = obtener_conexion_cursor()

    try:
        # Inserta los datos en la tabla cliente
        cursor.execute("""
            INSERT INTO cliente (cod_cliente, razon_social, domicilio, localidad, telefono, contacto, celular, dni)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['cod_cliente'],
            data['razon_social'],
            data['domicilio'],
            data['localidad'],
            data['telefono'],
            data['contacto'],
            data['celular'],
            data['dni']
        ))
        conexion.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        conexion.rollback()
        return jsonify({'error': 'Error al registrar el cliente'}), 500
    finally:
        cursor.close()
        conexion.close()
#registrar cliente
#guardar letra nueva
#UNA LETRA
@app.route('/guardar_letra', methods=['POST'])
def guardar_letra():
    try:
        data = request.json

        query = """
        INSERT INTO letras (numero_boleta, ref_giro, fecha_giro, fecha_vence, importe, cod_cliente, razon_social, moneda, tipo_producto, cliente_vendedor, estado, numero_unico,banco)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['numero_boleta'],
            data['ref_giro'],
            data['fecha_giro'],
            data['fecha_vence'],
            data['importe'],
            data['cod_cliente'],
            data['razon_social'],
            data['moneda'],
            data['tipo_producto'],
            data['cliente_vendedor'],
            'EMITIDA',  # Valor predeterminado para la columna 'estado'
            data.get('numero_unico', 123456),  # Valor predeterminado para 'numero_unico' si no está en los datos
            data['banco']
        )

        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error al insertar datos: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

#guardar letra nueva
# letra nueva  /vendedor






#DOS LETRAS


@app.route('/guardar_dos_letras', methods=['POST'])
def guardar_dos_letras():
    try:
        data = request.json
        
        letra_data_1 = data.get('letraData1')
        letra_data_2 = data.get('letraData2')

        query = """
        INSERT INTO letras (numero_boleta, ref_giro, fecha_giro, fecha_vence, importe, cod_cliente, razon_social, moneda, tipo_producto, cliente_vendedor, estado, numero_unico, banco)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values_1 = (
            letra_data_1['numero_boleta'],
            letra_data_1['ref_giro'],
            letra_data_1['fecha_giro'],
            letra_data_1['fecha_vence'],
            letra_data_1['importe'],
            letra_data_1['cod_cliente'],
            letra_data_1['razon_social'],
            letra_data_1['moneda'],
            letra_data_1['tipo_producto'],
            letra_data_1['cliente_vendedor'],
            'EMITIDA',  
            letra_data_1.get('numero_unico', 123456),  
            letra_data_1['banco']
        )

        # Insertar la segunda letra
        values_2 = (
            letra_data_2['numero_boleta'],
            letra_data_2['ref_giro'],
            letra_data_2['fecha_giro'],
            letra_data_2['fecha_vence'],
            letra_data_2['importe'],
            letra_data_2['cod_cliente'],
            letra_data_2['razon_social'],
            letra_data_2['moneda'],
            letra_data_2['tipo_producto'],
            letra_data_2['cliente_vendedor'],
            'EMITIDA',  
            letra_data_2.get('numero_unico', 123457), 
            letra_data_2['banco']
        )

        conexion, cursor = obtener_conexion_cursor()
        
        cursor.execute(query, values_1)
        cursor.execute(query, values_2)

        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({"success": True})
    except Exception as e:
        print(f"Error al insertar datos: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


























if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

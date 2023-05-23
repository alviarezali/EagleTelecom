from multiprocessing import connection
import pyodbc
from datetime import date,datetime, timedelta
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import requests
import pytz


# Conectar a la base de datos de Microsoft SQL Server

fecha_actual = date.today()
fecha_formateada_actual = fecha_actual.strftime("%Y/%m/%d")
fecha_corte = fecha_actual.replace(day=5).strftime("%Y/%m/%d")

print(fecha_corte)
conexion = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL server};"
    "Server=DESKTOP-2SI24S1;"
    "Database=testDB;"
    "uid=soporte;"
    "pwd=123;"
)
cursor = conexion.cursor()


# (LISTO) --- Función para agregar un nuevo cliente
def agregar_cliente():
    result = ""
    nombre = input("Ingrese el nombre del cliente: ").strip().capitalize()
    apellido = input("Ingrese el apellido del cliente: ").strip().capitalize()
    cedula = input("Ingrese la cédula del cliente: ").strip()
    direccion = input("Ingrese la dirección del cliente: ").strip().capitalize() #Separarla
    telefono = input("Ingrese el teléfono del cliente: ").strip()
    correo = input("Ingrese el correo del cliente: ").strip()
    while True:
        TipoServicio = input("Tipo de servicio del cliente? (Fibra Optica o Radio Enlace): ").strip().lower().split()
        if len(TipoServicio)==2 and TipoServicio[0] in ["fibra", "optica","radio","enlace"] and TipoServicio[1] in ["fibra", "optica","radio","enlace"]:
            for i in TipoServicio:
                result += i.capitalize()
            TipoServicio = result
            break 
        else: 
            print("******* Ingrese correctamente el tipo de servicio *******")
    
    while True:
        plan = input("¿Que plan de instalación adquirio el cliente? (Basico o Completo): ").strip().lower().split()
        if len(plan )==1 and plan[0] in ["basico", "completo"]:
            result = plan [0].capitalize()
            plan  = result
            break 
        else: 
            print("******* Ingrese correctamente el plan de instalación *******")
    
    monto =float(input("Ingrese el monto del plan adquirido: "))
    
    while True:
        TipoContrato = input("¿Que tipo de contrato es? (Residencial o Corporativo): ").strip().lower().split()
        if len(TipoContrato )==1 and TipoContrato [0] in ["residencial", "corporativo"]:
            result = TipoContrato [0].capitalize()
            TipoContrato  = result
            break 
        else: 
            print("******* Ingrese correctamente el tipo de contrato *******")
            
    FechaInicio = input("Fecha de inicio del contrato en formato YYYY/MM/DD: ").strip()
    if TipoServicio == "RadioEnlace":
        TipoAntena = input("Ingrese el modelo de la antena: ").strip()
    else:
        TipoAntena = "NoAplica"
    
    FechaPago = FechaInicio

    while True:
        EstadoServicio = input("Ingrese el estado del servicio: [Activo - Desactivo] ").strip().strip().lower().split()
        if len(EstadoServicio )==1 and EstadoServicio [0] in ["activo", "desactivo"]:
            result = EstadoServicio [0].capitalize()
            EstadoServicio  = result
            break 
        else: 
            print("******* Ingrese correctamente el estado del servicio *******")
    
    while True:
        respuesta = input("¿El cliente esta pagando el costo completo de la mensualidad? [Si - No]: ").lower().strip()
        if respuesta == "si" :
            MontoMensualidad = float(input("Ingrese el costo de la mensualidad: "))
            SaldoAbonado = 0.
            break
        elif respuesta =="no":
            MontoMensualidad = 0.00
            SaldoAbonado =  float(input("Ingrese el monto abonado: "))
            break
        else:
            print("Ingrese la respuesta correcta")
    
    

    while True:
        TipoPago =  input("Tipo de pago utilizado por el cliente [Dolar o Bolivar]: ").strip().strip().lower().split()
        if len(TipoPago )==1 and TipoPago [0] in ["dolar", "bolivar"]:
            result = TipoPago [0].capitalize()
            TipoPago  = result
            break 
        else: 
            print("******* Ingrese correctamente el tipo de pago *******")
    
 
    # Obtener el próximo ID disponible
    cursor.execute("SELECT ISNULL(MAX(ID), 0) + 1 FROM Clientes")
    proximo_id = cursor.fetchone()[0]

    # Insertar el nuevo cliente con el próximo ID disponible
    cursor.execute("INSERT INTO Clientes (ID, Nombre, Apellido, Cedula, Direccion, Telefono, Correo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (proximo_id, nombre, apellido, cedula, direccion, telefono, correo))
    cursor.execute(f"SELECT * from Clientes WHERE ID={proximo_id}")

    resultados = cursor.fetchall()  
    if resultados:
        encabezados = ["ID", "Nombre", "Apellido", "Cedula", "Direccion", "Telefono", "Correo"]
        tabla = formatear_datos_tabla(resultados, encabezados)
        print("-"*100)
        print(tabla)
    else:
        print("-"*100)
        print("No hay clientes que hayan pagado.")
        print("-"*100)


    cursor.execute("insert into Servicios (ID, TipoServicio, Pland, Monto, TipoContrato, FechaInicio, TipoAntena) values(?,?,?,?,?,?,?)",
                   (proximo_id, TipoServicio, plan, monto, TipoContrato, FechaInicio, TipoAntena))
    
    cursor.execute(f"SELECT * from Servicios WHERE ID={proximo_id}")
    resultados1 = cursor.fetchall()  
    if resultados:
        encabezados = ["ID", "TipoServicio", "Plan", "Monto", "TipoContrato", "FechaInicio", "TipoAntena"]
        tabla = formatear_datos_tabla(resultados1, encabezados)
        print("-"*100)
        print(tabla)
    else:
        print("-"*100)
        print("No hay clientes que hayan pagado.")
        print("-"*100)

    cursor.execute("insert into Contratos(ID, FechaPago, EstadoServicio, MontoMensualidad, TipoPago,SaldoAbonado)values(?,?,?,?,?,?)",
                   proximo_id, FechaPago, EstadoServicio, MontoMensualidad, TipoPago, SaldoAbonado)
    

    cursor.execute(f"SELECT * from Contratos WHERE ID={proximo_id}")
    resultados2 = cursor.fetchall()  
    if resultados:
        encabezados = ["ID", "FechaPago", "EstadoServicio", "MontoMensualidad", "TipoPago","SaldoAbonado"]
        tabla = formatear_datos_tabla(resultados2, encabezados)
        print("-"*100)
        print(tabla)
    else:
        print("-"*100)
        print("No hay clientes que hayan pagado.")
        print("-"*100)
    
    conexion.commit()


    print("Cliente agregado exitosamente.")
    

    

# Capitalize de todos los inputs
def GestionInput (input):
    return input.strip().capitalize()

# Formateo de datos en tabla
def formatear_datos_tabla(datos, encabezados):
    filas_formateadas = [list(map(str, fila)) for fila in datos]
    tabla = tabulate(filas_formateadas, headers=encabezados, tablefmt="fancy_grid")
    return tabla + "\n \n"+"-"*100

# Obtener la hora de la web o del sistema (Hora predeterminada)
def obtener_fecha_actualizada():
    '''Esta funcion no recibe ningun parametro, pero retorna dos.
    La primera es la hora del sistema o de la WEB.
    La segunda es un String donde se dice que la fecha es la del sistema, eso es para alertar al usuario.'''
    response = None  # Inicializar la variable response
    respuesta = None
    hora = None
    try:
        response = requests.get('https://www.google.com')
    except requests.exceptions.RequestException as e:
        pass
    
    if response and response.status_code == 200:  # Verificar si response tiene un valor y luego comprobar el status_code
        fecha = response.headers['date']
        fecha_datetime = datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %Z')
        utc_timezone = pytz.timezone('UTC')
        fecha_utc = utc_timezone.localize(fecha_datetime)
        venezuela_timezone = pytz.timezone('America/Caracas')
        fecha_venezuela = fecha_utc.astimezone(venezuela_timezone)
        # Establecer el día en 1
        fecha_venezuela_dia1 = fecha_venezuela.replace(day=1)
        hora = fecha_venezuela_dia1.strftime('%Y/%m/%d')
        
        
    else:
        fecha = datetime.now()
        respuesta = "\n***IMPORTANTE*** \nLa fecha predeterminada que se esta utilizando en el programa es la del sistema. Chequee que este \ncorrectamente actualizada o podria generar resultados incorrectos en sus consultad. \n" 
        # Establecer el día en 1
        fecha_dia1 = fecha.replace(day=1)
        hora = fecha_dia1.strftime('%Y/%m/%d')

    
    return hora, respuesta

# (LISTO) --- Función para eliminar un cliente
def eliminar_cliente():
    # Solicitar al usuario el valor de la cédula
    resp = input("\n¿Estas seguro(a) de querer borrar todos los registros del cliente? [SI - NO]: ").strip().capitalize()
    cedula = input("Ingrese el valor de la cédula: ").strip()
    

    if resp == "Si":
        cursor.execute(f"SELECT ID FROM Clientes WHERE Cedula = '{cedula}'")
        row = cursor.fetchone()
        if row:
            # Obtener el ID del cliente usando la cédula proporcionada
            cliente_id = row[0]

            # Borrar información de la tabla Servicios
            cursor.execute(f"DELETE FROM Servicios WHERE ID = {cliente_id}")

            # Borrar información de la tabla Contratos
            cursor.execute(f"DELETE FROM Contratos WHERE ID = {cliente_id}")

            # Borrar información de la tabla Clientes
            cursor.execute(f"DELETE FROM Clientes WHERE ID = {cliente_id}")

            conexion.commit()
            print("\nLa información se ha borrado exitosamente.")
        else:
            print("No se encontró un cliente con la cédula proporcionada.")
    else:
        print(f"El cliente {cedula} no ha sido borrado")

# Funcion para eliminar solo la celda de un cliente
def eliminar_celda_cliente():
    cedula = input("\n- Ingrese la Cedula del cliente que desea eliminar: ").strip()
    fecha = input("- Fecha del registro que desea eliminar en formato YYYY/MM/DD: ").strip()

    cursor.execute(f"DELETE FROM Contratos FROM Clientes WHERE Clientes.ID = Contratos.ID AND Clientes.Cedula = '{cedula}' AND Contratos.FechaPago = '{fecha}'")
    conexion.commit()
    print(f"\n********* El cliente {cedula} en la fecha {fecha} ha sido borrado exitosamente. *********\n")
# (LISTO) --- Función para obtener los clientes que han pagado 
def obtener_clientes_pagados():
    condicion = input("¿Desea ingresar una fecha personalizada para la consulta de los clientes que han pagado? [Si - No]: ").strip().capitalize()
    if condicion == "Si":
        fecha_input =input("Ingrese una fecha bajo el siguiente formato YYYY/MM/DD: ").strip()
        fecha = datetime.strptime(fecha_input, "%Y/%m/%d").date()
    else:
        fecha, respuesta = obtener_fecha_actualizada()
        print(respuesta if respuesta else "")

    cursor.execute(f"SELECT COUNT(*) AS TotalResultados FROM (SELECT Clientes.ID, Nombre, Apellido, telefono, TipoPago, Servicios.TipoServicio, Contratos.FechaPago, Contratos.MontoMensualidad, Contratos.SaldoAbonado FROM Clientes INNER JOIN Contratos ON Clientes.ID = Contratos.ID INNER JOIN Servicios ON Contratos.ID = Servicios.ID WHERE Contratos.EstadoServicio = 'Activo' AND Contratos.MontoMensualidad>=Servicios.Monto and Contratos.FechaPago>='{fecha}') as Resultado;")
    result = cursor.fetchone()

    cursor.execute(f"SELECT Clientes.ID, Nombre, Apellido, telefono, TipoPago, Servicios.TipoServicio, Contratos.FechaPago, Contratos.MontoMensualidad, Contratos.SaldoAbonado FROM Clientes INNER JOIN Contratos ON Clientes.ID = Contratos.ID INNER JOIN Servicios ON Contratos.ID = Servicios.ID WHERE Contratos.EstadoServicio = 'Activo' AND Contratos.MontoMensualidad>=Servicios.Monto and Contratos.FechaPago>='{fecha}'")
    resultados = cursor.fetchall()

    print(f"* EL total de clientes que HAN PAGADO hasta la fecha {fecha} es de {result[0]} persona(s)\n")    
    if resultados:
        encabezados = ["ID", "Nombre", "Apellido", "Teléfono", "TipoPago", "Tipo de Servicio", "Fecha de Pago", "Monto Mensualidad", "SaldoAbonado"]
        tabla = formatear_datos_tabla(resultados, encabezados)
        print("-"*100)
        print(f"Clientes que han pagado para la fecha {fecha}: \n")
        print(tabla)
    else:
        print("-"*100)
        print("No hay clientes que hayan pagado.")
        print("-"*100)

# (LISTO) --- Función para obtener los clientes que no han pagado
def obtener_clientes_no_pagados():
    # condicion = input("¿Desea ingresar una fecha personalizada para la colsunta de los clientes que no han pagado? [Si - No]: ").strip().capitalize()
    # if condicion == "Si":
    #     fecha_input =input("Ingrese una fecha bajo el siguiente formato YYYY/MM/DD: ").strip()
    #     fecha = datetime.strptime(fecha_input, "%Y/%m/%d").date()
    # else:
    #     fecha, respuesta = obtener_fecha_actualizada()
    #     print(respuesta)
    
    fecha, respuesta = obtener_fecha_actualizada()
    print(respuesta)   
    print("\nLa fecha utilizada para referenciar a los clientes que NO han pagado es (YYYY/MM/DD): ",fecha,"\n")
    
    cursor.execute(f"SELECT COUNT(*) AS TotalResultados FROM (SELECT C.ID, Clientes.Nombre, Clientes.Apellido, Clientes.Cedula, Clientes.Telefono,C.FechaPago,C.MontoMensualidad, C.SaldoAbonado FROM Contratos AS C INNER JOIN Clientes ON C.ID= Clientes.ID WHERE C.ID NOT IN (SELECT ID FROM (SELECT ID, MAX(FechaPago) AS UltimaFechaPago FROM Contratos WHERE MontoMensualidad <> 0.00 GROUP BY ID) T WHERE T.UltimaFechaPago >= '{fecha}') AND C.FechaPago = (SELECT MAX(FechaPago) FROM Contratos WHERE ID = C.ID)) AS Resultados;")
    result = cursor.fetchone()

    
    cursor.execute(f"SELECT C.ID, Clientes.Nombre, Clientes.Apellido, Clientes.Cedula, Clientes.Telefono,C.FechaPago,C.MontoMensualidad, C.SaldoAbonado FROM Contratos AS C INNER JOIN Clientes ON C.ID= Clientes.ID WHERE C.ID NOT IN (SELECT ID FROM (SELECT ID, MAX(FechaPago) AS UltimaFechaPago FROM Contratos WHERE MontoMensualidad <> 0.00 GROUP BY ID) T WHERE T.UltimaFechaPago >= '{fecha}') AND C.FechaPago = (SELECT MAX(FechaPago) FROM Contratos WHERE ID = C.ID)")
    resultados = cursor.fetchall()

    print(f"* EL total de clientes que no han pagado hasta la fecha {fecha} es de {result[0]} persona(s)\n")
    if resultados:
        print("*"*36+" CLIENTES QUE NO HAN PAGADO "+"*"*36+"\n")
        encabezados = ["ID", "Nombre", "Apellido", "Cédula","telefono", "FechaPago", "MontoMensualidad","SaldoAbonado"]
        
        tabla_formateada = formatear_datos_tabla(resultados,encabezados )
        print(tabla_formateada)
        conexion.commit()
    else:
        print("Todos los clientes han pagado.")

# (LISTO) --- Funcion parra agregar clintes que estan pagando la mensualidad 
def ingresar_pago():
    ''' Este código cumple con los siguientes requisitos:
    Si el cliente no tiene SaldoAbonado, el valor de MontoMensualidad se establece como el valor total de servicios.Monto.
    Si el cliente paga más que el valor de servicios.Monto, el excedente se añade al SaldoAbonado del siguiente mes.
    Si el cliente paga y aún no ha alcanzado el costo de servicios.Monto, el valor de MontoMensualidad es cero y el sobrante se añade a SaldoAbonado.
    Si el cliente ha pagado el costo total de servicios.Monto, el valor de MontoMensualidad es el valor completo de servicios.Monto y el SaldoAbonado sería cero para ese mes pagado'''

    fecha_pago_siguiente_mes = 0
    cedula_cliente = input("Ingrese la cédula del cliente: ").strip()
    # resp = input("Desea ingresar una fecha personalizada? [Si - No]: ").strip().capitalize()
    
    # if resp == "Si":
    #     fecha = input("Ingrese la fecha en el formato YYYY/MM/DD: ").strip().capitalize()
    # else:
    #     fecha, alerta = obtener_fecha_actualizada()
    #     print(alerta)




    # Descuento de dinero al cliente
    def FUNexcedente(excedente):
        return excedente-monto_servicio
    # Gestion de fechas
    def fechaGestion(fecha):
        if fecha.month == 12:
            fecha = fecha.replace(day=1, month = 1, year= fecha.year+1)
        else:
            fecha = fecha.replace(day=1, month = fecha.month+1)
        return fecha

    # Obtener el cliente por su cédula
    cursor.execute(f"SELECT ID, Nombre, Apellido, Cedula FROM Clientes WHERE Cedula = '{cedula_cliente}'")
    cliente = cursor.fetchone()
    

    if cliente:
        cliente_id = cliente[0]
        nombre_cliente = cliente[1]
        apellido_cliente = cliente[2]

        # Obtener los contratos activos del cliente
        cursor.execute(f"SELECT c.ID, c.MontoMensualidad, c.SaldoAbonado, c.TipoPago, s.Monto, c.FechaPago FROM Contratos as c INNER JOIN Servicios as s ON c.ID = s.ID INNER JOIN (SELECT ID, MAX(FechaPago) AS FechaMasReciente FROM Contratos GROUP BY ID) c2 ON c.ID = c2.ID AND c.FechaPago = c2.FechaMasReciente WHERE c.ID = {cliente_id} AND c.EstadoServicio = 'Activo';")
        
        contratos = cursor.fetchall()

        if contratos:
            encabezados = ["Cédula", "Nombre", "Apellido", "Monto Mensualidad", "SaldoAbonado", "TipoPago", "Monto de Servicio", "Fecha de Pago"]
            datos_cliente = []
            
            for contrato in contratos:
                contrato_id = contrato[0]
                monto_mensualidad = contrato[1]
                saldo_abonado = contrato[2]
                tipo_pago = contrato[3]
                
                monto_servicio = contrato[4]
                fecha_pago = contrato[5]
                fecha_pago_str = fecha_pago.strftime('%Y-%m-%d')  # Convertir la fecha a una cadena

                datos_cliente.append((cedula_cliente, nombre_cliente, apellido_cliente, str(monto_mensualidad), str(saldo_abonado), tipo_pago, str(monto_servicio), fecha_pago_str))

            tabla_cliente = formatear_datos_tabla(datos_cliente, encabezados)
            print("-" * 100)
            print("Información del cliente:")
            print(tabla_cliente)



            # Solicitar el monto a agregar
            monto_ingresado = float(input("\n"+"Ingrese el monto a pagar: ").strip())
            TipoPago = input("Tipo de pago a recibir (Bolivares o Dolares): ").strip().capitalize()

            # Validar y transformar el input
            while TipoPago.strip().lower() not in ['bolivares', 'dolares']:
                print("Tipo de pago inválido. Por favor, ingrese 'Bolivares' o 'Dolares'.")
                TipoPago = input("Tipo de pago a recibir (Bolivares o Dolares): ").strip().capitalize()

            print("*"*50)
            
            # Obtener la fecha de pago actual y calcular la fecha de pago del siguiente mes
            fecha_pago_actual_str = str(contrato[5])  # Obtener la cadena de texto de la fechaPago
            # print("Contrato[5]: ", type(contrato[5]))

            fecha_pago_actual = datetime.strptime(fecha_pago_actual_str, '%Y-%m-%d').date()  # Convertir a objeto de fecha
            
            monto_servicio = float(contrato[4])
            excedente = float(monto_ingresado) + float(saldo_abonado)
            

            MontoServicioLocal = monto_servicio
            if excedente > monto_servicio: #En caso de que tenga mas dinero que el montoServicio
                # Actualizo el mes Pagado
                if saldo_abonado != 0.00 and monto_mensualidad!=monto_servicio: 
                    cursor.execute("UPDATE Contratos SET SaldoAbonado = 0.00, MontoMensualidad = ?, TipoPago = ? WHERE ID = ? AND FechaPago = ?", ( monto_servicio, TipoPago ,contrato_id, fecha_pago_actual_str))
                    conexion.commit()
                    
                    excedente = FUNexcedente(excedente)                        
                
                if excedente > 0 and excedente > monto_servicio:
                    saldo = 0.00
                    condicional = False
                    fecha_pago_siguiente_mes = fechaGestion(fecha_pago_actual)
                    # fecha_pago_actual.replace(day=1, month=fecha_pago_actual.month+1)

                    while True:
                        if excedente < monto_servicio:
                            saldo = excedente
                            MontoServicioLocal = 0.00
                            condicional = True
                        elif excedente == monto_servicio:
                            # saldo = 0.00
                            # MontoServicioLocal = monto_servicio
                            condicional = True
                        cursor.execute("INSERT INTO Contratos (SaldoAbonado, ID, FechaPago, EstadoServicio, MontoMensualidad, TipoPago) VALUES (?, ?, ?, 'Activo', ?,?)", (saldo, contrato_id, fecha_pago_siguiente_mes, MontoServicioLocal, TipoPago))
                        conexion.commit()

                        excedente = FUNexcedente(excedente) #Descuento del cliente con monto del servicio
                        fecha_pago_siguiente_mes = fechaGestion(fecha_pago_siguiente_mes)
                        # fecha_pago_siguiente_mes.replace(month=fecha_pago_siguiente_mes.month+1)

                        if condicional:
                            break
                        

                elif excedente >0 and excedente < monto_servicio:
                    
                    fecha_pago_siguiente_mes = fechaGestion(fecha_pago_actual)
                    # fecha_pago_actual.replace(day=1, month=fecha_pago_actual.month+1)
                    cursor.execute("INSERT INTO Contratos (SaldoAbonado, ID, FechaPago, EstadoServicio, MontoMensualidad,TipoPago) VALUES (?, ?, ?, 'Activo', ?, ?)", (excedente, contrato_id, fecha_pago_siguiente_mes, 0.00,TipoPago))
                    conexion.commit()
                elif excedente==monto_servicio:
                    
                    fecha_pago_siguiente_mes = fechaGestion(fecha_pago_actual) 
                    # fecha_pago_actual.replace(day=1, month=fecha_pago_actual.month+1)
                    cursor.execute("INSERT INTO Contratos (SaldoAbonado, ID, FechaPago, EstadoServicio, MontoMensualidad,TipoPago) VALUES (?, ?, ?, 'Activo', ?,?)", (0.00, contrato_id, fecha_pago_siguiente_mes, monto_servicio,TipoPago))
                    conexion.commit()
 
                
                # saldo_abonado = excedente 

            elif excedente==monto_servicio: #En caso de que mi dinero total sea igual al costo servicio
                # Actualizar el SaldoAbonado del contrato actual
                cursor.execute("UPDATE Contratos SET SaldoAbonado = 0.00, MontoMensualidad = ?, TipoPago = ? WHERE ID = ? AND FechaPago = ?", ( monto_servicio,TipoPago ,contrato_id, fecha_pago_actual_str))
                conexion.commit()
            elif excedente<monto_servicio: #Mi dinero total es menor al costo de servicio (DINERO ABONADO)
                # Actualizar el SaldoAbonado del contrato actual
                if monto_mensualidad != 0.00:
                    fecha_pago_siguiente_mes = fechaGestion(fecha_pago_actual)
                    # fecha_pago_actual.replace(day=1, month=fecha_pago_actual.month+1)
                    cursor.execute("INSERT INTO Contratos (SaldoAbonado, ID, FechaPago, EstadoServicio, MontoMensualidad,TipoPago) VALUES (?, ?, ?, 'Activo', ?,?)", (excedente, contrato_id, fecha_pago_siguiente_mes, 0.00,TipoPago))
                    conexion.commit()
                else:
                    cursor.execute("UPDATE Contratos SET SaldoAbonado = ?, MontoMensualidad = ?, TipoPago= ? WHERE ID = ? AND FechaPago = ?", ( excedente,0.00, TipoPago,contrato_id, fecha_pago_actual_str))
                    conexion.commit()

            # MOSTRAMOS AL USUARIO LOS ULTIMOS DATOS ACTUALIZADO O AÑADIDOS DESPUES DE QUE EL CLIENTE PAGASE
            print("\n"+"La información del cliente ha sido añadida. Recuerda que la fecha tiene un formato AÑO/MES/DIA"+"\n")  
            cursor.execute(f"SELECT Clientes.Cedula, Clientes.Nombre, Clientes.Apellido, c.MontoMensualidad, c.SaldoAbonado, c.TipoPago, s.Monto, c.FechaPago FROM Contratos AS c INNER JOIN Servicios AS s ON c.ID = s.ID INNER JOIN Clientes ON Clientes.ID = s.ID WHERE c.ID = 6 AND c.FechaPago = (SELECT MAX(FechaPago) FROM Contratos WHERE ID = {cliente_id})")
            resultados = cursor.fetchall()
            encabezados = ["Cédula", "Nombre", "Apellido", "Monto Mensualidad", "SaldoAbonado", "TipoPago",  "Monto de Servicio", "Fecha de Pago"]
            
            tabla_formateada = formatear_datos_tabla(resultados,encabezados )
            print(tabla_formateada)
            conexion.commit()

        else:
            print("El cliente no tiene contratos activos.")
    else:
        print("No se encontró un cliente con la cédula ingresada.")

# Buscar Cliente
def buscar_cliente():
    cliente = input("Ingrese el numero de cedula de identidad del cliente que desea buscar: ").strip()

    cursor.execute(f"SELECT * FROM Clientes WHERE Cedula= '{cliente}'")
    resultado1 = cursor.fetchall()

    cursor.execute(f"SELECT top 10 Contratos.ID, Contratos.EstadoServicio, Contratos.FechaPago, Contratos.MontoMensualidad, Contratos.SaldoAbonado FROM Clientes INNER JOIN Contratos ON Clientes.ID = Contratos.ID WHERE Clientes.Cedula='{cliente}'")
    resultado2 = cursor.fetchall()

    cursor.execute(f"SELECT Servicios.ID, Servicios.FechaInicio, Servicios.Pland, Servicios.Monto, Servicios.TipoContrato, Servicios.TipoServicio FROM Clientes INNER JOIN Servicios on Clientes.ID = Servicios.ID WHERE Clientes.Cedula = '{cliente}'")
    resultado3 = cursor.fetchall()

    if resultado1:
        print("\nInformacion de la tabla CLIENTE")
        encabezado1 = ["ID","Nombre","Apellido","Cedula","Direccion","Telefono","Correo"]
        tabla = formatear_datos_tabla(resultado1, encabezado1)
        print("-"*100)
        print(tabla)
    else:
        print(f"No se encontro informacion del cliente {cliente} en la tabla CLIENTE")

    if resultado2:
        print("Informacion de la tabla CONTRATO")
        encabezado2 = ["ID","EstadoServicio","FechaPago", "MontoMensualidad", "SaldoAbonado"]
        tabla = formatear_datos_tabla(resultado2, encabezado2)
        print("-"*100)
        print(tabla)
    else:
        print(f"No se encontro informacion del cliente {cliente} en la tabla CONTRATO")
    

    if resultado3:
        print("Informacion de la tabla SERVICIOS")
        encabezado3 = ["ID","FechaInicio", "Pland", "Monto","TipoContrato","TipoServicio"]
        tabla = formatear_datos_tabla(resultado3, encabezado3)
        print("-"*100)
        print(tabla)
    else:
        print(f"No se encontro informacion del cliente {cliente} en la tabla SERVICIOS")

# Menú principal
while True:
    print("\n--- Menú ---")
    print("1. Agregar nuevo cliente")
    print("2. Eliminar cliente")
    print("3. Obtener clientes que han pagado")
    print("4. Obtener clientes que no han pagado")
    print("5. Ingresar pago")
    print("6. Buscar un CLiente")
    print("7. Salir")
    print("\n"+"*"*50)
    opcion = input("Seleccione una opción: ").strip()
    print("*"*50+"\n")

    if opcion == "1":
        agregar_cliente()
    elif opcion == "2":
        while True:
            print("\n--- ¿Que desea realizar? ---")
            print("1. Borrar solo 1 registro del cliente")
            print("2. Borrar todos los registros del cliente")
            print("3. Salir")
            subOpcion = input("Selecciones una opción: ")
            if subOpcion == "1":
                eliminar_celda_cliente()
            elif subOpcion =="2":
                eliminar_cliente()
            else:
                break
    elif opcion == "3":
        obtener_clientes_pagados()
    elif opcion == "4":
        obtener_clientes_no_pagados()
    elif opcion == "5":
        ingresar_pago()
    elif opcion == "6":
        buscar_cliente()
    elif opcion == "7":
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")

# Cerrar la conexión a la base de datos
conexion.close()
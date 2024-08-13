import json
from datetime import datetime
from colorama import Fore, Style

def cargar_json(archivo):
    try:
        with open(archivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_json(archivo, datos):
    with open(archivo, 'w') as f:
        json.dump(datos, f, indent=4)

def mostrar_menu(menu, categoria):
    print(f"\n{Fore.YELLOW}Categoría: {categoria.capitalize()}{Style.RESET_ALL}")
    for item in menu:
        if item['categoria'].lower() == categoria.lower():
            print(f"{item['nombre']} - ${item['precio']}")

def crear_pedido(menu):
    cliente = input("Nombre del cliente: ")
    pedidos = cargar_json("pedidos.json")
    
    
    for pedido in pedidos:
        if pedido['cliente'] == cliente and pedido['estado'] not in ['cancelado', 'servido']:
            print(f"{Fore.RED}El cliente ya tiene un pedido activo.{Style.RESET_ALL}")
            return

    nuevo_pedido = {"cliente": cliente, "items": [], "estado": "creado"}
    
    while True:
        print("\n1. Añadir entrada")
        print("2. Añadir plato fuerte")
        print("3. Añadir bebida")
        print("4. Finalizar pedido")
        opcion = input("Seleccione una opción: ")

        if opcion == '4':
            break

        categorias = ['entrada', 'plato_fuerte', 'bebida']
        if opcion in ['1', '2', '3']:
            categoria = categorias[int(opcion) - 1]
            mostrar_menu(menu, categoria)
            plato = input("Seleccione un plato: ")
            for item in menu:
                if item['nombre'].lower() == plato.lower() and item['categoria'] == categoria:
                    nuevo_pedido['items'].append(item)
                    print(f"{Fore.GREEN}Plato añadido al pedido.{Style.RESET_ALL}")
                    break
            else:
                print(f"{Fore.RED}Plato no encontrado en la categoría seleccionada.{Style.RESET_ALL}")

    print("\nResumen del pedido:")
    for item in nuevo_pedido['items']:
        print(f"{item['nombre']} - ${item['precio']}")
    
    confirmacion = input("¿Confirmar pedido? (s/n): ")
    if confirmacion.lower() == 's':
        pedidos.append(nuevo_pedido)
        guardar_json("pedidos.json", pedidos)
        print(f"{Fore.GREEN}Pedido guardado con éxito.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Pedido cancelado.{Style.RESET_ALL}")

def registrar_pago():
    cliente = input("Nombre del cliente: ")
    pedidos = cargar_json("pedidos.json")
    pagos = cargar_json("pagos.json")
    
    for pedido in pedidos:
        if pedido['cliente'] == cliente and pedido['estado'] != 'cancelado':
            total = sum(item['precio'] for item in pedido['items'])
            confirmacion = input(f"El total a pagar es ${total}. ¿Confirmar pago? (s/n): ")
            if confirmacion.lower() == 's':
                pago = {
                    "cliente": cliente,
                    "total": total,
                    "fecha_pago": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                pagos.append(pago)
                guardar_json("pagos.json", pagos)
                pedido['estado'] = 'pagado'
                guardar_json("pedidos.json", pedidos)
                print(f"{Fore.GREEN}Pago registrado con éxito.{Style.RESET_ALL}")
                return
    
    print(f"{Fore.RED}No se encontró un pedido activo para este cliente.{Style.RESET_ALL}")

def cambiar_estado_pedido():
    cliente = input("Nombre del cliente: ")
    pedidos = cargar_json("pedidos.json")
    
    for pedido in pedidos:
        if pedido['cliente'] == cliente:
            print(f"Estado actual: {pedido['estado']}")
            nuevo_estado = input("Nuevo estado (preparacion/servido/cancelado): ")
            
            if nuevo_estado == 'cancelado' and pedido['estado'] != 'creado':
                print(f"{Fore.RED}Solo se puede cancelar un pedido en estado 'creado'.{Style.RESET_ALL}")
                return
            
            if nuevo_estado == 'servido' and pedido['estado'] != 'pagado':
                print(f"{Fore.RED}Solo se puede servir un pedido pagado.{Style.RESET_ALL}")
                return
            
            estados_validos = ['creado', 'preparacion', 'servido', 'cancelado']
            if estados_validos.index(nuevo_estado) <= estados_validos.index(pedido['estado']):
                print(f"{Fore.RED}No se puede cambiar a un estado anterior o igual.{Style.RESET_ALL}")
                return
            
            pedido['estado'] = nuevo_estado
            guardar_json("pedidos.json", pedidos)
            print(f"{Fore.GREEN}Estado actualizado con éxito.{Style.RESET_ALL}")
            return
    
    print(f"{Fore.RED}No se encontró un pedido para este cliente.{Style.RESET_ALL}")

def modificar_pedido():
    cliente = input("Nombre del cliente: ")
    pedidos = cargar_json("pedidos.json")
    menu = cargar_json("menu.json")
    
    for pedido in pedidos:
        if pedido['cliente'] == cliente and pedido['estado'] == 'creado':
            while True:
                print("\n1. Añadir plato")
                print("2. Eliminar plato")
                print("3. Finalizar modificación")
                opcion = input("Seleccione una opción: ")
                
                if opcion == '1':
                    crear_pedido(menu)  
                elif opcion == '2':
                    for i, item in enumerate(pedido['items']):
                        print(f"{i+1}. {item['nombre']} - ${item['precio']}")
                    indice = int(input("Seleccione el número del plato a eliminar: ")) - 1
                    if 0 <= indice < len(pedido['items']):
                        del pedido['items'][indice]
                        print(f"{Fore.GREEN}Plato eliminado del pedido.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Índice inválido.{Style.RESET_ALL}")
                elif opcion == '3':
                    break
            
            guardar_json("pedidos.json", pedidos)
            print(f"{Fore.GREEN}Pedido modificado con éxito.{Style.RESET_ALL}")
            return
    
    print(f"{Fore.RED}No se encontró un pedido en estado 'creado' para este cliente.{Style.RESET_ALL}")

def consultar_pedidos():
    pedidos = cargar_json("pedidos.json")
    
    while True:
        print("\n1. Mostrar todos los pedidos")
        print("2. Mostrar un pedido particular")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            for pedido in pedidos:
                mostrar_pedido(pedido)
        elif opcion == '2':
            cliente = input("Nombre del cliente: ")
            for pedido in pedidos:
                if pedido['cliente'] == cliente:
                    mostrar_pedido(pedido)
                    break
            else:
                print(f"{Fore.RED}No se encontró un pedido para este cliente.{Style.RESET_ALL}")
        elif opcion == '3':
            break

def mostrar_pedido(pedido):
    print(f"\n{Fore.YELLOW}Cliente: {pedido['cliente']}{Style.RESET_ALL}")
    print(f"Estado: {pedido['estado']}")
    print("Items:")
    for item in pedido['items']:
        print(f"- {item['nombre']} (${item['precio']})")
    print(f"Total: ${sum(item['precio'] for item in pedido['items'])}")

def menu_principal():
    menu = cargar_json("menu.json")
    
    while True:
        print(f"\n{Fore.GREEN}===== MoliPollito Sistema de Gestión ====={Style.RESET_ALL}")
        print("1. Crear pedido")
        print("2. Registrar pago")
        print("3. Cambiar estado de pedido")
        print("4. Modificar pedido")
        print("5. Consultar pedidos")
        print("0. Salir")
        
        try:
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                crear_pedido(menu)
            elif opcion == '2':
                registrar_pago()
            elif opcion == '3':
                cambiar_estado_pedido()
            elif opcion == '4':
                modificar_pedido()
            elif opcion == '5':
                consultar_pedidos()
            elif opcion == '0':
                confirmacion = input("¿Está seguro que desea salir? (s/n): ")
                if confirmacion.lower() == 's':
                    print(f"{Fore.YELLOW}Gracias por usar MoliPollito Sistema de Gestión.{Style.RESET_ALL}")
                    break
            else:
                print(f"{Fore.RED}Opción no válida. Por favor, intente de nuevo.{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Ocurrió un error: {str(e)}{Style.RESET_ALL}")

menu_principal()
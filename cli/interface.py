from core.dispatcher import Dispatcher

def run_cli():
    dispatcher = Dispatcher()

    while True:
        print("\n--- Simulador de Gestión de Incidentes ---")
        print("1. Registrar incidente")
        print("2. Ver incidentes pendientes")
        print("3. Asignar incidente")
        print("4. Resolver incidente")
        print("5. Ver historial")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tipo = input("Tipo (infraestructura, seguridad, aplicativo): ")
            prioridad = input("Prioridad (alta, media, baja): ")
            descripcion = input("Descripción: ")
            dispatcher.register_incident(tipo, prioridad, descripcion)

        elif opcion == "2":
            dispatcher.show_pending_incidents()

        elif opcion == "3":
            try:
                id_incidente = int(input("ID del incidente: "))
                dispatcher.assign_incident(id_incidente) 
            except ValueError:
                print("⚠ Debe ingresar un número válido de ID.")

        elif opcion == "4":
            try:
                id_incidente = int(input("ID del incidente a resolver: "))
                dispatcher.resolve_incident(id_incidente)
            except ValueError:
                print("⚠ Debe ingresar un número válido de ID.")

        elif opcion == "5":
            dispatcher.show_history()

        elif opcion == "6":
            print("Saliendo del simulador...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")
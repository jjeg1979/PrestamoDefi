from prestamodefi import (
    alta_prestamista,
    alta_cliente,
    depositar_garantia,
    solicitar_prestamo,
    aprobar_prestamo,
    reembolsar_prestamo,
    liquidar_garantia,
    obtener_prestamos_por_prestatario,
    obtener_detalle_prestamo,
)


def menu_alta_prestamista():
    print("Has seleccionado dar de alta un prestamista.")
    prestamista = input("Ingresa la dirección del prestamista: ")
    alta_prestamista(prestamista)


def menu_alta_cliente():
    print("Has seleccionado dar de alta un cliente.")
    alta_cliente(
        input("Ingresa la dirección del cliente: "),
        input("Ingresa la dirección del prestamista: "),
        input("Ingresa la clave privada del prestamista: "),
    )


def menu_depositar_garantia():
    print("Has seleccionado depositar garantía.")
    depositar_garantia(
        input("Ingresa la dirección del cliente: "),
        int(input("Ingresa el valor de la garantía: ")),
        input("Ingresa la clave privada del cliente: "),
    )


def menu_solicitar_prestamo():
    print("Has seleccionado solicitar un préstamo.")
    solicitar_prestamo(
        input("Ingresa la dirección del cliente: "),
        input("Ingresa la dirección del prestamista: "),
        int(input("Ingresa el monto del préstamo: ")),
        int(input("Ingresa el plazo del préstamo: ")),
        input("Ingresa la clave privada del cliente: "),
    )


def menu_aprobar_prestamo():
    print("Has seleccionado aprobar un préstamo.")
    aprobar_prestamo(
        input("Ingresa la dirección del prestatario: "),
        int(input("Ingresa el ID del préstamo: ")),
        input("Ingresa la dirección del prestamista: "),
        input("Ingresa la clave privada del prestamista: "),
    )


def menu_reembolsar_prestamo():
    print("Has seleccionado reembolsar un préstamo.")
    reembolsar_prestamo(
        int(input("Ingresa el ID del préstamo: ")),
        input("Ingresa la dirección del cliente: "),
        input("Ingresa la clave privada del cliente: "),
    )


def menu_liquidar_garantia():
    print("Has seleccionado liquidar garantía.")
    liquidar_garantia(
        int(input("Ingresa el ID del préstamo: ")),
        input("Ingresa la dirección del cliente: "),
        input("Ingresa la dirección del prestamista: "),
        input("Ingresa la clave privada del prestamista: "),
    )


def menu_obtener_prestamos_por_prestatario():
    print("Has seleccionado obtener préstamos por prestatario.")
    obtener_prestamos_por_prestatario(input("Ingresa la dirección del prestatario: "))


def menu_obtener_detalle_prestamo():
    print("Has seleccionado obtener detalle de préstamo.")
    obtener_detalle_prestamo(
        input("Ingresa la dirección del prestatario: "),
        int(input("Ingresa el ID del préstamo: ")),
    )


def mostrar_menu() -> str:
    print("Menú de Interacción con el Contrato:")
    print("1. Dar de alta un prestamista")
    print("2. Dar de alta un cliente")
    print("3. Depositar garantía")
    print("4. Solicitar un préstamo")
    print("5. Aprobar un préstamo")
    print("6. Reembolsar un préstamo")
    print("7. Liquidar garantía")
    print("8. Obtener préstamos por prestatario")
    print("9. Obtener detalle de préstamo")
    print("0. Salir")
    opcion = input("Elige una opción: ")
    return opcion


def menu() -> None:
    while True:
        opcion = mostrar_menu()

        try:
            if opcion == "1":
                menu_alta_prestamista()
            elif opcion == "2":
                menu_alta_cliente()
            elif opcion == "3":
                menu_depositar_garantia()
            elif opcion == "4":
                menu_solicitar_prestamo()
            elif opcion == "5":
                menu_aprobar_prestamo()
            elif opcion == "6":
                menu_reembolsar_prestamo()
            elif opcion == "7":
                menu_liquidar_garantia()
            elif opcion == "8":
                menu_obtener_prestamos_por_prestatario()
            elif opcion == "9":
                menu_obtener_detalle_prestamo()
            elif opcion == "0":
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Por favor, elige una opción válida.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()

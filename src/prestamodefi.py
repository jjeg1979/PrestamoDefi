from math import ceil
from conexion import (
    conect,
    enviar_transacion,
    cliente_registrado,
    es_cliente_prestatario_del_prestamo,
    get_garantia_cliente,
    prestamo_aprobado_y_no_reembolsado,
    prestamo_valido,
    vencido_plazo_prestamos,
)  # type: ignore
from accounts import account1, account1_pk
from web3 import Web3


# Lógica para dar de alta un prestamista
def alta_prestamista(nuevo_prestamista_address: str):
    print(f"Dando de alta al prestamista con id: {nuevo_prestamista_address}.")

    try:
        # PASO 1. Conectamos con el contrato y solicitamos la dirección del prestamista
        web3, contrato = conect()  # type: ignore

        # PASO 2. Construimos la transacción para dar de alta el prestamista
        nonce = web3.eth.get_transaction_count(account1)  # type: ignore
        tx = contrato.functions.altaPrestamista(
            nuevo_prestamista_address
        ).build_transaction({"from": account1, "nonce": nonce})

        # PASO 3. Firmamos la transacción
        # signed_tx = web3.eth.account.sign_transaction(tx, private_key=account1_pk)  # type: ignore

        # PASO 4. Enviamos la transacción firmada
        # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)  # type: ignore
        tx_receipt = enviar_transacion(web3, tx, account1_pk)  # type: ignore

        # PASO 5. Esperamos a que la transacción sea minada
        # web3.eth.wait_for_transaction_receipt(tx_hash)  # type: ignore

        # PASO 6. Verificamos que el prestamista fue dado de alta exitosamente
        print(f"Prestamista dado de alta exitosamente {tx_receipt['transactionHash']}.")

    except Exception as e:
        print(f"Error al dar de alta el prestamista: {e}")


# Lógica para dar de alta un cliente
def alta_cliente(
    nuevo_cliente_address: str, prestamista_address: str, prestamista_pk: str
):
    print(
        f"Prestamista {prestamista_address} dando de alta el cliente {nuevo_cliente_address}."
    )
    try:
        web3, contrato = conect()  # type: ignore
        if not (cliente_registrado(contrato, nuevo_cliente_address)):
            nonce = web3.eth.get_transaction_count(prestamista_address)
            tx = contrato.functions.altaCliente(
                nuevo_cliente_address
            ).build_transaction({"from": prestamista_address, "nonce": nonce})
            tx_receipt = enviar_transacion(web3, tx, prestamista_pk)  # type: ignore
            print(f"Cliente dado de alta exitosamente {tx_receipt['transactionHash']}.")

        elif cliente_registrado(contrato, nuevo_cliente_address):
            print(f"El cliente {nuevo_cliente_address} ya está dado de alta.")
    except Exception as e:
        print(f"Error al dar de alta el cliente: {e}")


def depositar_garantia(direccion_cliente: str, valor: int, clave_privada_cliente: str):
    print(
        f"Cliente {direccion_cliente} depositando garantía por un valor totao de {valor}."
    )
    try:
        web3, contrato = conect()  # type: ignore
        nonce = web3.eth.get_transaction_count(direccion_cliente)
        tx = contrato.functions.depositarGarantia().build_transaction(
            {"from": direccion_cliente, "value": valor, "nonce": nonce}
        )
        tx_receipt = enviar_transacion(web3, tx, clave_privada_cliente)  # type: ignore
        print(f"Garantía depositada exitosamente {tx_receipt['transactionHash']}.")
    except Exception as e:
        print(f"Error al depositar garantía: {e}")


def solicitar_prestamo(
    direccion_cliente: str,
    direccion_prestatario: str,
    monto: int,
    plazo: int,
    clave_privada_cliente: str,
):
    print(
        f"Cliente {direccion_cliente} solicita un préstamo a {direccion_prestatario} por una cantidad total de {monto} para devolver en {ceil(plazo/(24*3600)):.0f} días."
    )
    if monto < 0 or plazo < 0:
        print("El monto y el plazo deben ser mayores a 0.")
        return
    try:
        web3, contrato = conect()  # type: ignore
        if not (get_garantia_cliente(contrato, direccion_cliente) >= monto):
            print(
                "La garantía del cliente no es suficiente para solicitar el préstamo."
            )
            return
        nonce = web3.eth.get_transaction_count(direccion_cliente)
        tx = contrato.functions.solicitarPrestamos(monto, plazo).build_transaction(
            {"from": direccion_cliente, "nonce": nonce}
        )
        tx_receipt = enviar_transacion(web3, tx, clave_privada_cliente)  # type: ignore
        print(
            f"Solicitud de préstamo enviada exitosamente {Web3.to_hex(tx_receipt['transactionHash'])}."
        )
    except Exception as e:
        print(f"Error al solicitar préstamo: {e}")


def aprobar_prestamo(
    prestatario_address: str,
    id_prestamo: int,
    prestamista_address: str,
    prestamista_pk: str,
):
    print(f"Aprobando el préstamo {id_prestamo} del cliente {prestamista_address}.")
    try:
        web3, contrato = conect()  # type: ignore
        if not prestamo_valido(contrato, prestatario_address, id_prestamo):
            print("El préstamo no es válido.")
            return
        nonce = web3.eth.get_transaction_count(prestamista_address)
        tx = contrato.functions.aprobarPrestamo(
            prestatario_address, id_prestamo
        ).build_transaction({"from": prestamista_address, "nonce": nonce})
        tx_receipt = enviar_transacion(web3, tx, prestamista_pk)  # type: ignore
        print(
            f"Préstamo aprobado exitosamente {Web3.to_hex(tx_receipt['transactionHash'])}."
        )
    except Exception as e:
        print(f"Error al aprobar préstamo: {e}")


def reembolsar_prestamo(prestamo_id: int, cliente_address: str, clave_privada: str):
    print(f"Reembolsando el préstamo {prestamo_id} del cliente {cliente_address}.")
    try:
        web3, contrato = conect()  # type: ignore
        if not (prestamo_valido(contrato, cliente_address, prestamo_id)):
            print("El préstamo no es válido.")
            return
        if not es_cliente_prestatario_del_prestamo(
            prestamo_id, contrato, cliente_address
        ):
            print("El cliente no es el prestatario del préstamo.")
            return
        nonce = web3.eth.get_transaction_count(cliente_address)
        tx = contrato.functions.reembolsarPrestamo(prestamo_id).build_transaction(
            {"from": cliente_address, "nonce": nonce}
        )
        tx_receipt = enviar_transacion(web3, tx, clave_privada)  # type: ignore
        print(
            f"Préstamo reembolsado exitosamente {Web3.to_hex(tx_receipt['transactionHash'])}."
        )
    except Exception as e:
        print(f"Error al reembolsar préstamo: {e}")


def liquidar_garantia(
    prestamo_id: int,
    prestatario_address: str,
    prestamista_address: str,
    prestamista_pk: str,
):
    print(f"Liquitando la garantía del préstamos {prestamo_id}.")
    try:
        web3, contrato = conect()  # type: ignore
        if prestamo_aprobado_y_no_reembolsado(
            contrato, prestatario_address, prestamo_id
        ):
            print("El préstamo no ha sido aprobado o ya fue reembolsado.")
            return
        if vencido_plazo_prestamos(
            prestamo_id, contrato, prestatario_address=prestatario_address
        ):
            print("El plazo del préstamo ha vencido.")
            return
        nonce = web3.eth.get_transaction_count(prestamista_address)
        tx = contrato.functions.liquidarGarantia(
            prestatario_address, prestamo_id
        ).build_transaction({"from": prestamista_address, "nonce": nonce})
        tx_receipt = enviar_transacion(web3, tx, prestamista_pk)  # type: ignore
        print(
            f"Garantía liquidada exitosamente {Web3.to_hex(tx_receipt['transactionHash'])}."
        )
    except Exception as e:
        print(f"Error al liquidar garantía: {e}")


def obtener_prestamos_por_prestatario(prestario_address: str):
    print(f"Obteniendo los préstamos del cliente {prestario_address}.")
    try:
        _, contrato = conect()  # type: ignore
        prestamos = contrato.functions.obtenerPrestamosPorPrestatario(
            prestario_address
        ).call()
        print(f"Préstamos del cliente {prestario_address}: {prestamos}")
    except Exception as e:
        print(f"Error al obtener préstamos por prestatario: {e}")


def obtener_detalle_prestamo(prestatario_address: str, id_prestamo: int):
    print(
        f"Obteniendo detalle de préstamo {id_prestamo} del cliente {prestatario_address}."
    )
    try:
        _, contrato = conect()  # type: ignore
        detalle_prestamo = contrato.functions.obtenerDetallesDePrestamo(
            prestatario_address, id_prestamo
        ).call()
        print(f"Detalle del préstamo {id_prestamo}: {detalle_prestamo}")
    except Exception as e:
        print(f"Error al obtener detalle de préstamo: {e}")

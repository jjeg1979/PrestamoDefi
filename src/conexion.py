import json
from typing import Any, Dict, Iterable, Tuple, Union
from web3 import Web3
from web3.exceptions import Web3Exception


# Conexión a Ganache
def conect() -> Tuple[Any, Any]:
    try:
        ganache_url: str = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))

        # Conectar a Ganache
        if not web3.is_connected():
            print("No se pudo conectar a Ganache")
            exit()
        else:
            print("Conexión exitosa a Ganache")
    except Web3Exception as e:
        print(f"Error al conectar a Ganache: {e}")
        exit()

    abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"GarantiaLiquidada","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoAprobado","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoReembolsado","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"plazo","type":"uint256"}],"name":"SolicitudPrestamo","type":"event"},{"inputs":[{"internalType":"address","name":"nuevoCliente","type":"address"}],"name":"altaCliente","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"nuevoPrestamista","type":"address"}],"name":"altaPrestamista","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"aprobarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"clientes","outputs":[{"internalType":"bool","name":"activado","type":"bool"},{"internalType":"uint256","name":"saldoGarantia","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"depositarGarantia","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"empleadosPrestamista","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"liquidarGarantia","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"obtenerDetallesDePrestamo","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"prestatario","type":"address"},{"internalType":"uint256","name":"monto","type":"uint256"},{"internalType":"uint256","name":"plazo","type":"uint256"},{"internalType":"uint256","name":"tiempoSolicitud","type":"uint256"},{"internalType":"uint256","name":"tiempoLimite","type":"uint256"},{"internalType":"bool","name":"aprobado","type":"bool"},{"internalType":"bool","name":"reembolsado","type":"bool"},{"internalType":"bool","name":"liquidado","type":"bool"}],"internalType":"struct PrestamoDefi.Prestamo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"}],"name":"obtenerPrestamosPorPrestatario","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"reembolsarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"socioPrincipal","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"monto_","type":"uint256"},{"internalType":"uint256","name":"plazo_","type":"uint256"}],"name":"solicitarPrestamos","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]'
    )

    address = web3.to_checksum_address("0x6195C4Fd3aEB7d60C943026FBf870AFE3b3c102C")

    contract = web3.eth.contract(address=address, abi=abi)

    # print(contract.functions.socioPrincipal().call())
    return web3, contract


def enviar_transacion(
    w3: Any, txn_dict: Dict[Any, Any], private_key: str
) -> Union[None, Any]:
    try:
        signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)  # type: ignore
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)  # type: ignore
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)  # type: ignore
        return txn_receipt  # type: ignore
    except Exception as e:
        print(f"Error al enviar transacción: {e}")
        return None


def cliente_registrado(contrato: str, address: str) -> bool:
    try:
        return contrato.functions.clientes(address).call()[0]  # type: ignore
    except Exception as e:
        print(f"Error al verificar si el cliente está registrado: {e}")
        return False


def get_garantia_cliente(contrato: str, address: str) -> int:
    try:
        garantia: int = contrato.functions.clientes(address).call()[1]  # type: ignore
        return garantia  # type: ignore
    except Exception as e:
        print(f"Error al obtener la garantía del cliente: {e}")
        return 0


def prestamo_valido(contrato: str, address: str, prestamo_id: int) -> bool:
    try:
        return (
            contrato.functions.obtenerDetallesDePrestamo(address, prestamo_id).call()[0]  # type: ignore
            != 0
        )
    except Exception as e:
        print(f"Error al verificar si el préstamo es válido: {e}")
        return False


def es_cliente_prestatario_del_prestamo(
    prestamo_id: int, contrato: str, address: str
) -> bool:
    try:
        prestamos_id: Iterable[int] = contrato.functions.obtenerPrestamosPorPrestatario(  # type: ignore
            address
        ).call()  # type: ignore
        if prestamo_id in prestamos_id:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al verificar si el cliente es prestatario: {e}")
        return False


def prestamo_aprobado_y_no_reembolsado(
    contrato: str, address: str, prestamo_id: int
) -> bool:
    try:
        prestamo = contrato.functions.obtenerDetallesDePrestamo(  # type: ignore
            address, prestamo_id
        ).call()
        return prestamo[6] and not prestamo[7]  # type: ignore
    except Exception as e:
        print(f"Error al verificar si el préstamo es aprobado y no reembolsado: {e}")
        return False


def vencido_plazo_prestamos(
    prestamo_id: int, contrato: str, prestatario_address: str
) -> bool:
    try:
        prestamo = contrato.functions.obtenerDetallesDePrestamo(  # type: ignore
            prestatario_address, prestamo_id
        ).call()
        return prestamo[5] < prestamo[4]  # type: ignore
    except Exception as e:
        print(f"Error al verificar si el préstamo está vencido: {e}")
        return False


if __name__ == "__main__":
    conect()

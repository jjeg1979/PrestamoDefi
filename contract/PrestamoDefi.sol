// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PrestamoDefi{
    address public socioPrincipal;

    struct Prestamo{
        uint256 id;
        address prestatario;
        uint256 monto;
        uint256 plazo;
        uint256 tiempoSolicitud;
        uint256 tiempoLimite;
        bool aprobado;
        bool reembolsado;
        bool liquidado;
    }

    struct Cliente{
        bool activado;
        uint256 saldoGarantia;
        mapping(uint256 => Prestamo) prestamos;
        uint256[] prestamoIds;
    }

    mapping(address => Cliente) public clientes;
    mapping(address => bool) public empleadosPrestamista;

    event SolicitudPrestamo(address prestatario, uint256 monto, uint256 plazo);
    event PrestamoAprobado(address prestatario, uint256 monto);
    event PrestamoReembolsado(address prestatario, uint256 monto);
    event GarantiaLiquidada(address prestatario, uint256 monto);

    modifier soloSocioPrincipal(){
        require(msg.sender == socioPrincipal, "Solo el socio principal puede ejecutar esta funcion");
        _;
    }

    modifier soloEmpleadoPrestamista(){
        require(empleadosPrestamista[msg.sender], "Solo los empleados prestamistas pueden ejecutar esta funcion");
        _;
    }

    modifier soloClienteRegistrado(){
        require(clientes[msg.sender].activado, "El cliente no esta registrado");
        _;
    }

    constructor(){
        socioPrincipal = msg.sender;
        empleadosPrestamista[socioPrincipal] = true;
    }

    function altaPrestamista(address nuevoPrestamista) public soloSocioPrincipal{
        require(!empleadosPrestamista[nuevoPrestamista], "El empleado ya es prestamista");
        empleadosPrestamista[nuevoPrestamista] = true;
    }

    function altaCliente(address nuevoCliente) public soloEmpleadoPrestamista{
        require(!clientes[nuevoCliente].activado, "El cliente ya esta registrado");
        Cliente storage structNuevoCliente = clientes[nuevoCliente];
        structNuevoCliente.saldoGarantia = 0;
        structNuevoCliente.activado = true;
    }

    function depositarGarantia() public payable soloClienteRegistrado{
        clientes[msg.sender].saldoGarantia += msg.value;
    }

    function solicitarPrestamos(
        uint256 monto_,
        uint256 plazo_
    ) public soloClienteRegistrado returns (uint256) {
        require(clientes[msg.sender].saldoGarantia >= monto_, "Saldo insuficiente");
        uint256 nuevoId = clientes[msg.sender].prestamoIds.length + 1;
        Prestamo storage nuevoPrestamo = clientes[msg.sender].prestamos[nuevoId];
        nuevoPrestamo.id = nuevoId;
        nuevoPrestamo.prestatario = msg.sender;
        nuevoPrestamo.monto = monto_;
        nuevoPrestamo.plazo = plazo_;
        nuevoPrestamo.tiempoSolicitud = block.timestamp;
        nuevoPrestamo.tiempoLimite = 0;
        nuevoPrestamo.aprobado = false;
        nuevoPrestamo.reembolsado = false;
        nuevoPrestamo.liquidado = false;
        clientes[msg.sender].prestamoIds.push(nuevoId);
        emit SolicitudPrestamo(msg.sender, monto_, plazo_);
        return nuevoId;
    }

    function aprobarPrestamo(address prestatario_, uint256 id_) public soloEmpleadoPrestamista{
        Cliente storage prestatario = clientes[prestatario_];
        require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "El prestamo no existe");
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(!prestamo.aprobado, "El prestamo ya fue aprobado");
        require(!prestamo.reembolsado, "El prestamo ya fue reembolsado");
        require(!prestamo.liquidado, "El prestamo ya fue liquidado");
        prestamo.aprobado = true;
        prestamo.tiempoLimite = block.timestamp + prestamo.plazo;
        emit PrestamoAprobado(prestatario_, prestamo.monto);
    }

    function reembolsarPrestamo(uint256 id_) public soloClienteRegistrado{
        Cliente storage prestatario = clientes[msg.sender];
        require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "El prestamo no existe");
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(msg.sender == prestamo.prestatario, "El prestamo no pertenece al cliente");
        require(prestamo.aprobado, "El prestamo no fue aprobado");
        require(!prestamo.reembolsado, "El prestamo ya fue reembolsado");
        require(!prestamo.liquidado, "El prestamo ya fue liquidado");
        require(block.timestamp <= prestamo.tiempoLimite, "El prestamo esta vencido");
        payable(socioPrincipal).transfer(prestamo.monto);
        prestatario.saldoGarantia -= prestamo.monto;
        prestamo.reembolsado = true;
        emit PrestamoReembolsado(msg.sender, prestamo.monto);
    }

    function liquidarGarantia(address prestatario_, uint256 id_) public soloEmpleadoPrestamista{
        Cliente storage prestatario = clientes[prestatario_];
        require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "El prestamo no existe");
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(prestamo.aprobado, "El prestamo no fue aprobado");
        require(prestamo.reembolsado, "El prestamo no fue reembolsado");
        require(!prestamo.liquidado, "El prestamo ya fue liquidado");
        require(block.timestamp > prestamo.tiempoLimite, "El prestamo no esta vencido");
        payable(socioPrincipal).transfer(prestamo.monto);
        prestatario.saldoGarantia += prestamo.monto;
        prestamo.liquidado = true;
        emit GarantiaLiquidada(prestatario_, prestamo.monto);
    }

    function obtenerPrestamosPorPrestatario(address prestatario_) public view returns(uint256[] memory){
        return clientes[prestatario_].prestamoIds;
    }

    function obtenerDetallesDePrestamo(address prestatario_, uint256 id_) public view returns(Prestamo memory){
        return clientes[prestatario_].prestamos[id_];
    }
}
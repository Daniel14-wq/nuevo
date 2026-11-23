
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_fifo(dut):

    dut._log.info("INICIANDO PRUEBA FIFO 4x4")

    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reloj de 50 MHz
    # Periodo = 20 ns
    async def ciclo(entrada):
        dut.clk.value = 0
        dut.ui_in.value = entrada
        await Timer(10, unit="ns")

        dut.clk.value = 1
        await Timer(10, unit="ns")

    def verificar_estado(cantidad, valido, dato):
        salida = int(dut.uo_out.value)
        uio = int(dut.uio_out.value)

        contador = ((uio & 0x03) << 1) | (
            (salida >> 7) & 1
        )

        assert contador == cantidad, (
            f"Contador incorrecto: {contador}"
        )

        assert ((salida >> 4) & 1) == (cantidad == 4), (
            "Error en FULL"
        )

        assert ((salida >> 5) & 1) == (cantidad == 0), (
            "Error en EMPTY"
        )

        assert ((salida >> 6) & 1) == valido, (
            "Error en READ_VALID"
        )

        assert (salida & 0x0F) == dato, (
            f"Dato incorrecto: {salida & 0x0F}"
        )

    # RESET
    await ciclo(0x00)
    verificar_estado(0, 0, 0)

    dut.rst_n.value = 1
    dut._log.info("RESET CORRECTO")

    # ESCRITURA
    datos = [0xA, 0x3, 0xC, 0x5]

    for cantidad, dato in enumerate(datos, 1):
        await ciclo(0x10 | dato)
        verificar_estado(cantidad, 0, 0)

        dut._log.info(
            f"ESCRITURA: {dato:X}"
        )

    # FIFO LLENA
    await ciclo(0x1F)
    verificar_estado(4, 0, 0)

    dut._log.info("FIFO LLENA")

    # LECTURA
    for indice, dato in enumerate(datos):
        await ciclo(0x20)

        verificar_estado(
            3 - indice,
            1,
            dato
        )

        dut._log.info(
            f"LECTURA: {dato:X}"
        )

    # LECTURA EN VACIO
    await ciclo(0x20)
    verificar_estado(0, 0, 0x5)

    assert int(dut.uio_oe.value) == 0x03

    dut._log.info("TODAS LAS PRUEBAS PASARON")


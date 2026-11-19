# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_fifo(dut):
    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    async def ciclo(entrada):
        # Aplicar la entrada antes del flanco de subida.
        dut.clk.value = 0
        dut.ui_in.value = entrada
        await Timer(500, unit="ns")
        dut.clk.value = 1
        await Timer(500, unit="ns")

    def verificar_estado(cantidad, lectura_valida, dato):
        salida = int(dut.uo_out.value)
        uio = int(dut.uio_out.value)

        # count[0] está en uo[7] y count[2:1] en uio[1:0].
        contador = ((uio & 0b11) << 1) | ((salida >> 7) & 1)

        assert contador == cantidad, f"Esperaba {cantidad} datos, hay {contador}"
        assert ((salida >> 4) & 1) == (cantidad == 4), "Bandera full incorrecta"
        assert ((salida >> 5) & 1) == (cantidad == 0), "Bandera empty incorrecta"
        assert ((salida >> 6) & 1) == lectura_valida, "read_valid incorrecto"
        assert (salida & 0x0F) == dato, f"Esperaba el dato {dato:X}, salida {salida:02X}"

    # El reset de tu FIFO necesita un flanco de subida.
    await ciclo(0x00)
    verificar_estado(0, 0, 0)
    assert int(dut.uio_oe.value) == 0x03, "UIO 0 y 1 deben ser salidas"
    dut.rst_n.value = 1

    # Escribir cuatro datos. El bit 4 habilita la escritura.
    datos = [0xA, 0x3, 0xC, 0x5]
    for cantidad, dato in enumerate(datos, start=1):
        await ciclo(0x10 | dato)
        verificar_estado(cantidad, 0, 0)

    # Intentar una quinta escritura con la FIFO llena.
    await ciclo(0x1F)
    verificar_estado(4, 0, 0)

    # Leer los cuatro datos. El bit 5 habilita la lectura.
    for indice, dato in enumerate(datos):
        await ciclo(0x20)
        verificar_estado(3 - indice, 1, dato)

    # Una lectura adicional en vacío conserva el último dato
    # y desactiva read_valid, tal como hace tu código Verilog.
    await ciclo(0x20)
    verificar_estado(0, 0, 0x5)

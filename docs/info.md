<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

La FIFO almacena hasta cuatro datos de 4 bits y los entrega en el orden
en que se escribieron. En cada flanco ascendente de clk, ui[4] solicita
guardar el dato de ui[3:0] y ui[5] solicita leer el dato más antiguo.
La bandera full indica que la FIFO está llena y empty indica que está vacía.

## How to test

1. Coloca ui_in = 0x00 y rst_n = 0 durante un flanco ascendente de clk.
   Comprueba que uo[5] (empty) vale 1. Después coloca rst_n = 1.
2. Coloca ui_in = 0x1A durante un flanco ascendente. Se guarda el dato
   hexadecimal A. Comprueba que uo[5] (empty) baja a 0.
3. Coloca ui_in = 0x20 durante el siguiente flanco ascendente. Comprueba
   que uo[3:0] entrega A, uo[6] (read_valid) vale 1 y uo[5] (empty)
   vuelve a 1 porque se leyó el único dato almacenado.
4. Coloca ui_in = 0x00. Después del siguiente flanco ascendente,
   comprueba que uo[6] (read_valid) vuelve a 0.

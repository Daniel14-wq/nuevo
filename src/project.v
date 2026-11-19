`timescale 1ns/1ps
`default_nettype none

module tt_um_fifo_silicluster (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire [3:0] data_out;
    wire [2:0] count;
    wire full;
    wire empty;
    wire read_valid;

    fifo_core fifo (
        .clk        (clk),
        .rst        (~rst_n),
        .data_in    (ui_in[3:0]),
        .write_en   (ui_in[4]),
        .read_en    (ui_in[5]),
        .data_out   (data_out),
        .full       (full),
        .empty      (empty),
        .count      (count),
        .read_valid (read_valid)
    );

    assign uo_out[3:0] = data_out;
    assign uo_out[4]   = full;
    assign uo_out[5]   = empty;
    assign uo_out[6]   = read_valid;
    assign uo_out[7]   = count[0];

    assign uio_out = {6'b000000, count[2:1]};
    assign uio_oe  = 8'b00000011;  // UIO 0 y 1 funcionan como salidas

    wire _unused = &{ena, ui_in[7:6], uio_in, 1'b0};

endmodule

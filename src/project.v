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

    // FIFO de 4 posiciones, cada una de 4 bits.
    reg [3:0] mem [0:3];
    reg [1:0] wr_ptr;
    reg [1:0] rd_ptr;
    reg [2:0] used;
    reg [3:0] data_out;
    reg       read_valid;

    wire [3:0] data_in;
    wire write_en;
    wire read_en;
    wire full;
    wire empty;
    wire do_write;
    wire do_read;

    // Entradas de Tiny Tapeout.
    assign data_in  = ui_in[3:0];
    assign write_en = ui_in[4];
    assign read_en  = ui_in[5];

    assign full     = (used == 3'd4);
    assign empty    = (used == 3'd0);
    assign do_write = write_en && !full;
    assign do_read  = read_en  && !empty;

    always @(posedge clk) begin
        if (!rst_n) begin
            wr_ptr     <= 2'd0;
            rd_ptr     <= 2'd0;
            used       <= 3'd0;
            data_out   <= 4'd0;
            read_valid <= 1'b0;
        end else begin
            read_valid <= do_read;

            if (do_write) begin
                mem[wr_ptr] <= data_in;
                wr_ptr      <= wr_ptr + 2'd1;
            end

            if (do_read) begin
                data_out <= mem[rd_ptr];
                rd_ptr   <= rd_ptr + 2'd1;
            end

            case ({do_write, do_read})
                2'b10:   used <= used + 3'd1;
                2'b01:   used <= used - 3'd1;
                default: used <= used;
            endcase
        end
    end

    // Salidas conforme al pinout que configuraste en info.yaml.
    assign uo_out[3:0] = data_out;
    assign uo_out[4]   = full;
    assign uo_out[5]   = empty;
    assign uo_out[6]   = read_valid;
    assign uo_out[7]   = used[0];

    assign uio_out = {6'b000000, used[2:1]};
    assign uio_oe  = 8'b00000011;

    wire _unused = &{ena, ui_in[7:6], uio_in, 1'b0};

endmodule
